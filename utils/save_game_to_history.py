
def save_game_to_history(observation, winner, window_size):
    """
    Summarizes and categorizes the game, then appends to history.
    
    Example of a stored game in history:
    {
      "game": 0,
      "winner": "yellow",
      "yellow_team_moves": [
        {"clue": "FRUIT", "num": 2, "guesses": ["APPLE", "BANANA"], "results": ["yellow", "yellow"]}
      ],
      "blue_team_moves": [
        {"clue": "OCEAN", "num": 1, "guesses": ["SHIP"], "results": ["neutral"]}
      ]
    }
    """
    obs = observation
    
    # Separate turns by team
    yellow_moves = [t for t in obs.current_game_turns if t["team"] == "yellow"]
    blue_moves = [t for t in obs.current_game_turns if t["team"] == "blue"]
    
    # Remove the "team" key from the inner dictionaries to save space
    for t in yellow_moves: del t["team"]
    for t in blue_moves: del t["team"]
    
    # Append the categorized game log
    obs.history.append({
        "game": obs.current_game,
        "winner": winner,
        "yellow_team_moves": yellow_moves,
        "blue_team_moves": blue_moves
    })
    
    # Enforce sliding window if configured
    if window_size > 0:
        obs.history = obs.history[-window_size:]

