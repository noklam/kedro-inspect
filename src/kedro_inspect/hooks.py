from kedro.framework.hooks import hook_impl
from kedro.framework.cli.hooks import cli_hook_impl
import logging
from kedro.framework.startup import ProjectMetadata

logger = logging.getLogger(__name__)
print(__name__)


class TraceHook:
    def __init__(self):
        self.used_datasets = {}

    @cli_hook_impl
    def before_command_run(
        self, project_metadata: ProjectMetadata, command_args: list[str]
    ):
        print(project_metadata)
        print("before_command_run")

    @hook_impl
    def after_catalog_created(self, catalog):
        logger.info("kedro-inspect** Reached after_catalog_created hook")

    @hook_impl
    def before_dataset_loaded(self, dataset_name):
        self.used_datasets[dataset_name] = "used"
        # logger.info("Plugin INFO")
        # logger.debug("Plugin DEBUG")
        # logger.warn("Plugin WARN")

    def after_pipeline_run(self):
        logger.info("kedro-inspect** after_pipeline_run")
        print(self.used_datasets)


trace_hook = TraceHook()
