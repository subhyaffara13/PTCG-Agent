from typing import List

def make_subset(dataset: DataSet, agent_subset: List[str]):
  for agent in dataset.agent_names:
    if agent not in agent_subset:
      delete_agent(dataset, agent)

