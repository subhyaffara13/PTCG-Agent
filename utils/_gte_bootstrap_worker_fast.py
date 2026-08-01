
def _gte_bootstrap_worker_fast(matrix_tuple, agents, tasks):
    """Fast worker using pre-computed matrices."""
    mean_matrix, stddev_matrix = matrix_tuple

    # Regularization logic matches original
    if mean_matrix.size > 0:
        rnd = np.random.default_rng()
        for j in range(mean_matrix.shape[1]):
            # ptp fails on empty arrays, but we checked size > 0
            if np.ptp(mean_matrix[:, j]) < 1e-9:
                mean_matrix[:, j] += rnd.random(mean_matrix.shape[0]) * 1e-6
                stddev_matrix[:, j] += rnd.random(mean_matrix.shape[0]) * 1e-6

    # Solve Game using Polarix
    game_plx = plx.agent_vs_task_game(
        agents=agents, tasks=tasks, agent_vs_task=mean_matrix, agent_vs_task_stddev=stddev_matrix,
        task_player='metric', normalizer='winrate'
    )
    res = plx.solve(game_plx, plx.ce_maxent, disable_progress_bar=True)
    marginals = plx.marginals_from_joint(res.joint)
    r2m_contributions = plx.joint_payoffs_contribution(
        game_plx.payoffs, res.joint, rating_player=1, contrib_player=0
    )
    m2r_contributions = plx.joint_payoffs_contribution(
        game_plx.payoffs, res.joint, rating_player=0, contrib_player=1
    )

    ratings_np = [np.array(r) for r in res.ratings]
    joint_np = np.array(res.joint)
    marginals_np = [np.array(m) for m in marginals]
    r2m_contributions_np = np.array(r2m_contributions)
    m2r_contributions_np = np.array(m2r_contributions)

    game_meta = SimpleNamespace(actions=game_plx.actions)

    return ratings_np, joint_np, marginals_np, r2m_contributions_np, m2r_contributions_np, game_meta

