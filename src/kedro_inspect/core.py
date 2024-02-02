
#| hide
from functools import reduce
from operator import or_

from demo_project.pipeline_registry import register_pipelines

used_datasets = reduce(or_, (p.datasets() for p in register_pipelines().values()))

# Create a session
# https://docs.kedro.org/en/stable/kedro_project_setup/session.html#create-a-session
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path

bootstrap_project("../../demo-project")
with KedroSession.create() as session:
    context = session.load_context()
    catalog = context.catalog
    unused_datasets = set(catalog.list()) - used_datasets

print(unused_datasets)