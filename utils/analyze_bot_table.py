
def analyze_bot_table(filename):
  """Do some analysis on the payoff cross-table."""
  print(f"Opening bot table file: {filename}")
  bot_table_file = open(filename, "r")
  table = np.zeros(shape=(pyspiel.ROSHAMBO_NUM_BOTS,
                          pyspiel.ROSHAMBO_NUM_BOTS), dtype=np.float64)
  print("Parsing file...")
  values = {}
  bot_names_map = {}
  for line in bot_table_file:
    line = line.strip()
    # ('driftbot', 'driftbot', -0.571)
    myre = re.compile(r"\'(.*)\', \'(.*)\', (.*)\)")
    match_obj = myre.search(line)
    row_agent, col_agent, value = match_obj.groups()
    values[f"{row_agent},{col_agent}"] = value
    bot_names_map[row_agent] = True
  bot_names_list = list(bot_names_map.keys())
  bot_names_list.sort()
  print(len(bot_names_list))
  assert len(bot_names_list) == pyspiel.ROSHAMBO_NUM_BOTS
  print(bot_names_list)
  for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
    for j in range(pyspiel.ROSHAMBO_NUM_BOTS):
      key = f"{bot_names_list[i]},{bot_names_list[j]}"
      assert key in values
      table[i][j] = float(values[key])
  print("Population returns:")
  pop_returns = np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)
  pop_aggregate = np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)
  for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
    pop_eval = 0
    for j in range(pyspiel.ROSHAMBO_NUM_BOTS):
      pop_eval += table[i][j]
    pop_eval /= pyspiel.ROSHAMBO_NUM_BOTS
    # print(f"  {bot_names_list[i]}: {pop_eval}")
    pop_returns[i] = pop_eval
    pop_aggregate[i] += pop_eval
    print(f"  {pop_eval},")
  print("Population exploitabilities: ")
  pop_expls = np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)
  avg_pop_expl = 0
  for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
    pop_expl = -float(pyspiel.ROSHAMBO_NUM_THROWS)
    for j in range(pyspiel.ROSHAMBO_NUM_BOTS):
      pop_expl = max(pop_expl, -table[i][j])
    avg_pop_expl += pop_expl
    pop_expls[i] = pop_expl
    pop_aggregate[i] -= pop_expl
    print(f"  {pop_expl},")
  avg_pop_expl /= pyspiel.ROSHAMBO_NUM_BOTS
  print(f"Avg within-pop expl: {avg_pop_expl}")
  print("Aggregate: ")
  indices = np.argsort(pop_aggregate)
  for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
    idx = indices[pyspiel.ROSHAMBO_NUM_BOTS - i - 1]
    print(f"  {i+1} & \\textsc{{{bot_names_list[idx]}}} & " +
          f" ${pop_returns[idx]:0.3f}$ " +
          f"& ${pop_expls[idx]:0.3f}$ & ${pop_aggregate[idx]:0.3f}$ \\\\")
  print("Dominance:")
  for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
    for j in range(pyspiel.ROSHAMBO_NUM_BOTS):
      if np.all(np.greater(table[i], table[j])):
        print(f"{bot_names_list[i]} dominates {bot_names_list[j]}")

