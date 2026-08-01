
def delete_agent(dataset: DataSet, agent: str):
  idx = dataset.agent_names.index(agent)
  assert 0 <= idx < len(dataset.agent_names)
  del dataset.agent_names[idx]
  for key in dataset.table_data.keys():
    del dataset.table_data[key][idx]

