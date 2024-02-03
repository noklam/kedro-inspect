from kedro.framework.hooks import hook_impl
import logging
logger = logging.getLogger(__name__)

class TraceHook:
    @hook_impl
    def after_catalog_created(self, catalog):
        logger.info("Reached after_catalog_created hook")

    @hook_impl
    def before_dataset_loaded(self, dataset_name):
        logger.info("Reached before_dataset_loaded hook")


trace_hook = TraceHook()