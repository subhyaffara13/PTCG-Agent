
def _openskill_bootstrap_worker_fast(games_data, num_agents, model):
    if model is None:
        return []
    ratings = GameSetEvaluator._compute_openskill_ratings_fast(games_data, num_agents, model)
    return [r.mu for r in ratings]

