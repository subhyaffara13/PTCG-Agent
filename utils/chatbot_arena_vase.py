
def chatbot_arena_vase(model_names, dataset):
  """Run VasE over Chatbot Arena data set."""

  alternatives = model_names[:]
  profile = base.PreferenceProfile(alternatives=alternatives)
  for datapoint in dataset:
    alt_a, alt_b, outcome = datapoint
    if outcome == 0:
      pass
    elif outcome == -1:
      profile.add_vote([alt_a, alt_b])
    elif outcome == 1:
      profile.add_vote([alt_b, alt_a])

  margin_matrix = profile.margin_matrix()
  strong_cond_winners = profile.condorcet_winner(True, margin_matrix)
  weak_cond_winners = profile.condorcet_winner(False, margin_matrix)
  print(f"Strong Condorcet winner? {strong_cond_winners}")
  print(f"Weak Condorcet winner(s)? {weak_cond_winners}")

  voting_methods = [
      # approval.ApprovalVoting(k=8),
      # borda.BordaVoting(),
      copeland.CopelandVoting(),
      # kemeny_young.KemenyYoungVoting(),
      # Use verbose=True to get more information about the levels
      maximal_lotteries.MaximalLotteriesVoting(iterative=True),
      # maximal_lotteries.MaximalLotteriesVoting(iterative=True, verbose=True),
      # plurality.PluralityVoting(),
      ranked_pairs.RankedPairsVoting(),
      # stv.STVVoting(num_winners=8)
      schulze.SchulzeVoting(),
  ]
  for method in voting_methods:
    print("")
    print(method.name())
    outcome = method.run_election(profile)
    print(outcome.pretty_table_string())

