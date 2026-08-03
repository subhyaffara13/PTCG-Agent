import logging

def balance_profile(
    profile: base.PreferenceProfile,
    num_votes_per_matchup: int | None = None,
) -> base.PreferenceProfile:
  """Balances an uneven preference profile.

  Args:
    profile: the preference profile to balance.
    num_votes_per_matchup: the number of votes to cast for each matchup. If
      None, then the function will take the maximum count of any matchup in the
      profile and use that.

  Returns:
    A new preference profile with balanced pairwise counts.

  An uneven profile is one where the distribution over number of matchups
  between (i, j) is non-uniform. This function creates a new profile
  (of pairwise preferences) where the number of votes per (i, j) matchup is
  uniform, while (in expectation) maintaining the true data's win rates per
  matchup.
  """
  m = profile.num_alternatives()
  new_profile = base.PreferenceProfile(alternatives=profile.alternatives)

  profile_counts = profile.pairwise_count_matrix()
  pref_matrix = profile.pref_matrix().astype(float)

  if num_votes_per_matchup is None:
    num_votes_per_matchup = profile.pairwise_count_matrix().max()

  assert num_votes_per_matchup is not None
  assert num_votes_per_matchup > 0
  assert profile.alternatives == new_profile.alternatives

  for i in range(m):
    for j in range(i+1, m):
      if profile_counts[i, j] == 0:
        logging.warning("Skipping (i, j) with no votes: (%d, %d)", i, j)
        continue
      winrate_i_j = float(pref_matrix[i, j]) / profile_counts[i, j]
      alt_i = new_profile.alternatives[i]
      alt_j = new_profile.alternatives[j]
      num_wins = int(round(winrate_i_j * num_votes_per_matchup))
      num_losses = max(0, num_votes_per_matchup - num_wins)
      for _ in range(num_wins):
        new_profile.add_vote([alt_i, alt_j])
      for _ in range(num_losses):
        new_profile.add_vote([alt_j, alt_i])

  return new_profile

