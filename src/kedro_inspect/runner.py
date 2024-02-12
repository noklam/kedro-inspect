# in src/<package_name>/runner.py
from typing import Any

from pluggy import PluginManager

from kedro.framework.hooks.manager import _NullPluginManager
from kedro.io import DataCatalog, MemoryDataset
from kedro.pipeline import Pipeline
from kedro.runner.runner import AbstractRunner


class DryRunner(AbstractRunner):
    """``DryRunner`` is an ``AbstractRunner`` implementation. It can be used to list which
    nodes would be run without actually executing anything. It also checks if all the
    neccessary data exists.
    """

    def __init__(
        self,
        is_async,
        extra_dataset_patterns=None,
    ):
        default_dataset_pattern = {"{default}": {"type": "MemoryDataset"}}
        self._extra_dataset_patterns = extra_dataset_patterns or default_dataset_pattern
        super().__init__(
            is_async=is_async, extra_dataset_patterns=self._extra_dataset_patterns
        )

    def _run(
        self,
        pipeline: Pipeline,
        catalog: DataCatalog,
        hook_manager: PluginManager = None,
        session_id: str = None,
    ) -> None:
        """The method implementing dry pipeline running.
        Example logs output using this implementation:

            kedro.runner.dry_runner - INFO - Actual run would execute 3 nodes:
            node3: identity([A]) -> [B]
            node2: identity([C]) -> [D]
            node1: identity([D]) -> [E]

        Args:
            pipeline: The ``Pipeline`` to run.
            catalog: The ``DataCatalog`` from which to fetch data.
            session_id: The id of the session.

        """
        print("DEBUG**", catalog.list())
        nodes = pipeline.nodes
        self._logger.info(
            "Actual run would execute %d nodes:\n%s",
            len(nodes),
            pipeline.describe(),
        )
        self._logger.info("Checking inputs...")
        input_names = pipeline.inputs()
        missing_inputs = [
            input_name
            for input_name in input_names
            if not catalog._get_dataset(input_name).exists()
        ]
        if missing_inputs:
            raise KeyError(f"Datasets {missing_inputs} not found.")

    def run(
        self,
        pipeline: Pipeline,
        catalog: DataCatalog,
        hook_manager: PluginManager | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Run the ``Pipeline`` using the datasets provided by ``catalog``
        and save results back to the same objects.

        Args:
            pipeline: The ``Pipeline`` to run.
            catalog: The ``DataCatalog`` from which to fetch data.
            hook_manager: The ``PluginManager`` to activate hooks.
            session_id: The id of the session.

        Raises:
            ValueError: Raised when ``Pipeline`` inputs cannot be satisfied.

        Returns:
            Any node outputs that cannot be processed by the ``DataCatalog``.
            These are returned in a dictionary, where the keys are defined
            by the node outputs.

        """

        hook_or_null_manager = hook_manager or _NullPluginManager()
        catalog = catalog.shallow_copy()

        # Check which datasets used in the pipeline are in the catalog or match
        # a pattern in the catalog
        registered_ds = [ds for ds in pipeline.datasets() if ds in catalog]

        # Check if there are any input datasets that aren't in the catalog and
        # don't match a pattern in the catalog.
        unsatisfied = pipeline.inputs() - set(registered_ds)

        if unsatisfied:
            raise ValueError(
                f"Pipeline input(s) {unsatisfied} not found in the DataCatalog"
            )

        # Identify MemoryDataset in the catalog
        memory_datasets = {
            ds_name
            for ds_name, ds in catalog._datasets.items()
            if isinstance(ds, MemoryDataset)
        }

        # Check if there's any output datasets that aren't in the catalog and don't match a pattern
        # in the catalog and include MemoryDataset.
        free_outputs = pipeline.outputs() - (set(registered_ds) - memory_datasets)

        # Register the default dataset pattern with the catalog
        catalog = catalog.shallow_copy(
            extra_dataset_patterns=self._extra_dataset_patterns
        )

        if self._is_async:
            self._logger.info(
                "Asynchronous mode is enabled for loading and saving data"
            )
        self._run(pipeline, catalog, hook_or_null_manager, session_id)  # type: ignore[arg-type]

        self._logger.info("Pipeline execution completed successfully.")
        # This create an edge case when the return dict have a memory dataset which isn't saved yet
        # return {ds_name: catalog.load(ds_name) for ds_name in free_outputs}
