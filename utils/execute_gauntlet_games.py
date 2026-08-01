
def execute_gauntlet_games(runner, archetype, opp_deck, target_deck, num_games):
    total_wins = total_games = 0
    for i in range(num_games):
        res = runner.run_iteration(iteration_id=9999, version_n1="candidate", version_n2=f"gauntlet_{archetype}", deck_base=target_deck, deck_new=opp_deck, reasoning_base={}, reasoning_new={}, num_matchups=1)
        games = res.get("games", {})
        total_games += len(games)
        for game in games.values():
            if game.get("winner") == "player_a":
                total_wins += 1
    return total_wins, total_games

