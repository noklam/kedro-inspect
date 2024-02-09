# in src/<package_name>/runner.py
from kedro.io import AbstractDataset, DataCatalog, MemoryDataset
from kedro.pipeline import Pipeline
from kedro.runner.runner import AbstractRunner
from pluggy import PluginManager


class DryRunner(AbstractRunner):
    """``DryRunner`` is an ``AbstractRunner`` implementation. It can be used to list which
    nodes would be run without actually executing anything. It also checks if all the
    neccessary data exists.
    """

    def create_default_dataset(self, ds_name: str) -> AbstractDataset:
        """Factory method for creating the default data set for the runner.

        Args:
            ds_name: Name of the missing data set
        Returns:
            An instance of an implementation of AbstractDataset to be used
            for all unregistered data sets.

        """
        return MemoryDataset()

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