
def track_turn(observation, state):
    """Tracks clues and guesses during the game."""
    obs = observation
    
    # Detect new clue
    if obs.clue != obs._last_clue and obs.clue != "":
        # current_turn is updated by prod_interpreter to the NEXT player (guesser)
        team = "blue" if obs.current_turn in [0, 1] else "yellow"
        obs.current_game_turns.append({
            "team": team,
            "clue": obs.clue,
            "num": obs.clue_number,
            "guesses": [],
            "results": []
        })
        obs._last_clue = obs.clue
        
    # Detect new guesses
    revealed = obs.revealed
    words = obs.words
    
    for i in range(len(revealed)):
        if revealed[i] and not obs._last_revealed[i]:
            if obs.current_game_turns:
                last_turn = obs.current_game_turns[-1]
                last_turn["guesses"].append(words[i])
                # Read full roles from agent 0 (Cluemaster)
                full_roles = state[0].observation.roles
                last_turn["results"].append(full_roles[i])
            obs._last_revealed[i] = True

