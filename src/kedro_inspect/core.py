from functools import reduce
from operator import or_

from rich import print

from kedro.framework.project import pipelines, settings
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
        self.settings = settings

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

    def find_unused_patterns(self, pipeline_name="__default__"):
        pipeline = self.pipelines[pipeline_name]
        patterns = self.catalog._dataset_patterns
        explicit_datasets = set(self.catalog.list())
        pipeline_datasets = pipeline.datasets()
        pattern_datasets = [dataset for dataset in pipeline_datasets if dataset not in explicit_datasets and not dataset.startswith("params:")]
        used_patterns = set()
        for dataset in pattern_datasets:
            matched_pattern = self.catalog._match_pattern(patterns, dataset)
            if matched_pattern:
                used_patterns.add(matched_pattern)
        unused_patterns = set(patterns.keys()) - used_patterns
        return unused_patterns


    def find_used_pattern(self, dataset):
        patterns = self.catalog._dataset_patterns
        # if dataset is explicit just return the name
        if dataset in self.catalog.list():
            return dataset
        matched_pattern = self.catalog._match_pattern(patterns, dataset)
        # if dataset matches pattern return the pattern
        # can also check if the dataset name being checked is actually in pipeline.datasets()
        if matched_pattern:
                return matched_pattern
        return None


if __name__ == "__main__":
    project_path = "/Users/Nok_Lam_Chan/dev/kedro-inspect/demo-project"
    KedroProject(project_path)
