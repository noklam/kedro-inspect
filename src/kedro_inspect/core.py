from functools import reduce
from operator import or_
from kedro.framework.project import pipelines
from rich import print
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path



class KedroProject:
    def __init__(self, project_path):
        bootstrap_project(project_path)
        self.session = KedroSession.create(project_path)
        self.context = self.session.load_context()
        self.catalog = self.context.catalog
        self.pipelines = pipelines

    def find_unused_datasets(self):
        used_datasets = reduce(or_, (p.datasets() for p in self.pipelines.values()))
        unused_datasets = set(self.catalog.list()) - used_datasets

        print(unused_datasets)
        return unused_datasets

if __name__ == "__main__":
    project_path = "/Users/Nok_Lam_Chan/dev/kedro-inspect/demo-project"
    KedroProject(project_path)