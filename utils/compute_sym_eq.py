
def compute_sym_eq(pt):
  game = nashpy.Game(pt[0], pt[1])
  p1_traj, p2_traj = game.asymmetric_replicator_dynamics()
  p1_strat = np.mean(p1_traj, axis=0)
  p2_strat = np.mean(p2_traj, axis=0)
  return 0.5 * p1_strat + 0.5 * p2_strat

