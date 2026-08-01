
def parse_dataset(filename):
  """Parse the Lewis et al. '17 data file."""
  # book, hat, ball
  # Example format
  # 1 0 4 2 1 2 YOU: i would like 4 hats and you can have the rest . <eos> THEM: deal <eos> YOU: <selection> item0=0 item1=4 item2=0 <eos> reward=8 agree 1 4 4 1 1 2
  # 1 4 4 1 1 2 THEM: i would like 4 hats and you can have the rest . <eos> YOU: deal <eos> THEM: <selection> item0=1 item1=0 item2=1 <eos> reward=6 agree 1 0 4 2 1 2
  # 1 6 3 0 2 2 YOU: you can have all the hats if i get the book and basketballs . <eos> THEM: <selection> item0=1 item1=3 item2=2 <eos> reward=10 disagree 1 2 3 2 2 1
  # 1 10 3 0 1 0 YOU: hi i would like the book and ball and you can have the hats <eos> THEM: i can give you either the book or the ball <eos> YOU: ill take the book <eos> THEM: ok i will take the hats and ball <eos> YOU: deal <eos> THEM: <selection> item0=1 item1=0 item2=0 <eos> reward=10 agree 1 2 3 2 1 2
  # 1 2 3 2 1 2 THEM: hi i would like the book and ball and you can have the hats <eos> YOU: i can give you either the book or the ball <eos> THEM: ill take the book <eos> YOU: ok i will take the hats and ball <eos> THEM: deal <eos> YOU: <selection> item0=0 item1=3 item2=1 <eos> reward=8 agree 1 10 3 0 1 0
  contents = pyspiel.read_contents_from_file(filename, "r")
  lines = contents.split("\n")
  cur_nego = None
  negotiations = []
  instances = []

  for line_no in range(len(lines)):
    line = lines[line_no]
    if line:
      parts = line.split(" ")
      # parse the line to add a new negotiation
      pool = [int(parts[0]), int(parts[2]), int(parts[4])]
      my_values = [int(parts[1]), int(parts[3]), int(parts[5])]
      pool2 = [int(parts[-6]), int(parts[-4]), int(parts[-2])]
      other_values = [int(parts[-5]), int(parts[-3]), int(parts[-1])]
      assert pool == pool2
      rewards = [0, 0]
      add_nego = False
      outcome_str = parts[-7]  # this will be "agree" or "disagree"
      if parts[6] == "YOU:":
        player_id = 0
        instance = Instance(pool, my_values, other_values)
      elif parts[6] == "THEM:":
        player_id = 1
        instance = Instance(pool, other_values, my_values)
      else:
        assert False, parts[6]
      outcome = False
      my_reward = 0
      instances.append(instance)
      if "disconnect" in line:
        continue
      # sometimes there is a "no agreement" in the rewards section
      if (outcome_str == "disagree" or
          (parts[-9] + " " + parts[-8]) == "reward=no agreement" or
          parts[-8] == "reward=disconnect"):
        # do not parse the reward, but must still parse the next line
        add_nego = False
      elif outcome_str == "agree":
        outcome = True
        reward_parts = parts[-8].split("=")
        assert len(reward_parts) == 2, f"reward parts str: {parts[-8]}"
        assert reward_parts[0] == "reward"
        my_reward = int(reward_parts[1])
      else:
        assert False, f"Bad outcome: {outcome_str}"
      if cur_nego is None:
        rewards[player_id] = my_reward
        if player_id == 0:
          cur_nego = Negotiation(instance, outcome, rewards)
        else:
          cur_nego = Negotiation(instance, outcome, rewards)
      else:
        # There are some in the data set that are incomplete (i.e. are missing the second perspective).
        # We should not count these.
        if dialogue_matches_prev_line(line, lines[line_no - 1]):
          assert list(cur_nego.instance.pool) == pool
          if player_id == 1:
            assert list(cur_nego.instance.p2values) == my_values
            assert list(cur_nego.instance.p1values) == other_values
          elif player_id == 0:
            assert list(cur_nego.instance.p1values) == my_values
            assert list(cur_nego.instance.p2values) == other_values
          cur_nego.rewards[player_id] = my_reward
          add_nego = True
        else:
          # not matching, treat as new negotiation
          rewards[player_id] = my_reward
          if player_id == 0:
            cur_nego = Negotiation(instance, outcome, rewards)
          else:
            cur_nego = Negotiation(instance, outcome, rewards)
          add_nego = False
      if add_nego or outcome_str == "disagree":
        negotiations.append(cur_nego)
        print(str(cur_nego))
        print(len(negotiations))
        cur_nego = None
        if outcome_str != "disagree":
          # same instance was added twice, so remove the last one
          instances.pop()
  return instances, negotiations

