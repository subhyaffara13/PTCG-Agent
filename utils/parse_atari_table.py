
def parse_atari_table(filename: str) -> DataSet:
  """Parse an Atari data file.

  The files are created by copy/paste from the papers.

  Args:
    filename: the file that contains the dataset.

  Returns:
      a DataSet object referring to the Atari data.
  """
  with open(filename, "r") as f:
    string_data = f.read()

  # First line is a comment
  # Second line format is column descriptions, e.g.:
  # "# game <agent1 name> <agent2 name> ..."
  # Rest of the lines are copy/paste from the paper tables.
  lines = string_data.split("\n")
  assert lines[1].startswith("# game ")
  agent_names = lines[1].split()[2:]
  num_agents = len(agent_names)
  game_names = []
  table_data = {}
  for i in range(2, len(lines)):
    if lines[i].strip():
      parts = lines[i].split()
      game_name = parts[0]
      game_names.append(game_name)
      str_scores = parts[1:]
      assert len(str_scores) == num_agents, f"Error line: {lines[i]}"
      scores = parse_values(str_scores)
      table_data[game_name] = scores
  return DataSet(agent_names, game_names, table_data)

