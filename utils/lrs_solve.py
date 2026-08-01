
def lrs_solve(row_payoffs, col_payoffs, lrsnash_max_denom, lrsnash_path):
  """Find all Nash equilibria using the lrsnash solver.

  `lrsnash` uses reverse search vertex enumeration on rational polytopes.
  For more info, see: http://cgm.cs.mcgill.ca/~avis/C/lrslib/USERGUIDE.html#nash

  Args:
    row_payoffs: payoffs for row player
    col_payoffs: payoffs for column player
    lrsnash_max_denom: maximum denominator
    lrsnash_path: path for temporary files

  Yields:
    (row_mixture, col_mixture), numpy vectors of float64s.
  """
  num_rows, num_cols = row_payoffs.shape
  game_file, game_file_path = tempfile.mkstemp()
  try:
    game_file = os.fdopen(game_file, "w")

    # write dimensions
    game_file.write("%d %d\n\n" % (num_rows, num_cols))

    # write row-player payoff matrix as fractions
    for row in range(num_rows):
      game_file.write(
          " ".join(to_fraction_str(row_payoffs[row], lrsnash_max_denom)) + "\n")
    game_file.write("\n")

    # write col-player payoff matrix as fractions
    for row in range(num_rows):
      game_file.write(
          " ".join(to_fraction_str(col_payoffs[row], lrsnash_max_denom)) + "\n")
    game_file.write("\n")
    game_file.close()
    lrs = subprocess.Popen([lrsnash_path or "lrsnash", "-s", game_file_path],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    col_mixtures = []
    for line in lrs.stdout:
      if len(line) <= 1 or line[:1] == b"*":
        continue
      line = np.asarray(
          [fractions.Fraction(x) for x in line.decode().split()],
          dtype=np.float64,
      )
      if line[0] == 2:  # col-player
        col_mixtures.append(line[1:-1])
      else:  # row-player
        row_mixture = line[1:-1]
        # row-mixture forms a Nash with every col-mixture listed directly above
        for col_mixture in col_mixtures:
          yield (row_mixture, col_mixture)
        col_mixtures = []
  finally:
    os.remove(game_file_path)

