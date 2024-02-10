from functools import reduce
from operator import or_
from kedro.framework.project import pipelines
from rich import print
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project


class KedroProject:
    """
    The object to preload all necessary components at the startup time.
    """

    def __init__(self, project_path):
        bootstrap_project(project_path)
        self.session = KedroSession.create(project_path)
        self.context = self.session.load_context()
        self.catalog = self.context.catalog
        self.pipelines = pipelines
        self.config_loader = self.context.config_loader

    def find_unused_datasets(self):
        used_datasets = reduce(or_, (p.datasets() for p in self.pipelines.values()))
        unused_datasets = set(self.catalog.list()) - used_datasets

        print(unused_datasets)
        return unused_datasets

    def find_pipeline_used(self, dataset):
        raise NotImplementedError

    def find_config_source(self, config):
        # Where is the config from? cli/file/global/resolver etc
        raise NotImplementedError

    def find_unused_pattern(self):
        raise NotImplementedError

    def find_used_pattern(self, dataset):
        # Return list of dataset name/pipeline used maybe
        raise NotImplementedError


if __name__ == "__main__":
    project_path = "/Users/Nok_Lam_Chan/dev/kedro-inspect/demo-project"
    KedroProject(project_path)
