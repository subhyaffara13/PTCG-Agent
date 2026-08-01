
def process_action(state, config):
    current_turn = state[0].observation.current_turn
    active_agent = state[current_turn]
    action = active_agent.action

    # core_harness wraps the real action inside {"submission": ...}.
    # Extract it so the rest of the interpreter sees the unwrapped value.
    if isinstance(action, dict) and "submission" in action:
        action = action["submission"]
    
    # helper to end game
    def end_game(winner=None):
        for i in range(4):
            if state[i].status != "INVALID":
                state[i].status = "DONE"
            if winner == "blue":
                if i in [0, 1]:
                    state[i].reward = (state[i].reward or 0) + 1
                else:
                    state[i].reward = state[i].reward or 0
            elif winner == "yellow":
                if i in [2, 3]:
                    state[i].reward = (state[i].reward or 0) + 1
                else:
                    state[i].reward = state[i].reward or 0
            else:
                state[i].reward = state[i].reward or 0

    # Handle Agent Failure / Invalid Action
    if action is None:
        active_agent.status = "INVALID"
        end_game(winner="yellow" if current_turn in [0, 1] else "blue")
        return

    # CLUEMASTER TURN
    if current_turn in [0, 2]:
        if not isinstance(action, dict) or "clue" not in action or "number" not in action:
            active_agent.status = "INVALID"
            end_game(winner="yellow" if current_turn == 0 else "blue")
            return
            
        # Clue validation
        normalized_clue = str(action["clue"]).strip().upper()
        words = state[0].observation.words
        revealed = state[0].observation.revealed
        roles = state[0].observation.roles
        opponent_team = "yellow" if current_turn == 0 else "blue"
        
        is_invalid_clue = False
        if " " in normalized_clue or "-" in normalized_clue:
            is_invalid_clue = True
            
        if not is_invalid_clue:
            for i in range(BOARD_SIZE):
                if not revealed[i]:
                    unrevealed_word = words[i].upper()
                    if unrevealed_word in normalized_clue or normalized_clue in unrevealed_word:
                        is_invalid_clue = True
                        break
                    
        if is_invalid_clue:
            # Penalty: Reveal a random opponent word and pass turn
            opponent_unrevealed = [i for i in range(BOARD_SIZE) if not revealed[i] and roles[i] == opponent_team]
            if opponent_unrevealed:
                to_reveal = random.choice(opponent_unrevealed)
                for s in state:
                    s.observation.revealed[to_reveal] = True
            
            for s in state:
                s.observation.clue = ""
                s.observation.guesses_remaining = 0
                s.observation.current_turn = 2 if current_turn == 0 else 0
                
            # Check if penalty won the game for opponent
            blue_left = sum(1 for i in range(BOARD_SIZE) if roles[i] == "blue" and not state[0].observation.revealed[i])
            yellow_left = sum(1 for i in range(BOARD_SIZE) if roles[i] == "yellow" and not state[0].observation.revealed[i])
            
            if blue_left == 0:
                end_game(winner="blue")
            elif yellow_left == 0:
                end_game(winner="yellow")
            else:
                for i in range(4):
                    state[i].status = "ACTIVE" if i == state[0].observation.current_turn else "INACTIVE"
            return
            
        # Update state normally
        for s in state:
            clue_num = int(action["number"])
            s.observation.clue = str(action["clue"])
            s.observation.clue_number = clue_num
            s.observation.guesses_remaining = BOARD_SIZE if clue_num <= 0 else clue_num + 1
            s.observation.current_turn = 1 if current_turn == 0 else 3
            
        # Set agent statuses
        for i in range(4):
            state[i].status = "ACTIVE" if i == state[0].observation.current_turn else "INACTIVE"
            
    # GUESSER TURN
    elif current_turn in [1, 3]:
        # action is an int (0-24) or -1 (pass) OR a dict with "guess": int
        guess_val = action.get("guess") if isinstance(action, dict) else action
        
        if not isinstance(guess_val, int) or guess_val < -1 or guess_val > BOARD_SIZE - 1:
            active_agent.status = "INVALID"
            end_game(winner="yellow" if current_turn == 1 else "blue")
            return
            
        # Pass
        if guess_val == -1:
            clue_num = state[0].observation.clue_number
            expected_remaining = BOARD_SIZE if clue_num <= 0 else clue_num + 1
            # 0 ("zero") and -1 ("infinity") clues both give unlimited guesses but STILL require at least 1 guess
            if state[0].observation.guesses_remaining == expected_remaining:
                active_agent.status = "INVALID"
                end_game(winner="yellow" if current_turn == 1 else "blue")
                return
                
            for s in state:
                s.observation.clue = ""
                s.observation.guesses_remaining = 0
                s.observation.current_turn = 2 if current_turn == 1 else 0
        else:
            # Check if already revealed
            if state[0].observation.revealed[guess_val]:
                active_agent.status = "INVALID"
                end_game(winner="yellow" if current_turn == 1 else "blue")
                return
                
            # Reveal
            for s in state:
                s.observation.revealed[guess_val] = True
            
            roles = state[0].observation.roles
            guessed_role = roles[guess_val]
            team_color = "blue" if current_turn == 1 else "yellow"
            
            # Trap check
            if guessed_role == "trap":
                end_game(winner="yellow" if team_color == "blue" else "blue")
                return
                
            # Neutral or Opponent word
            if guessed_role != team_color:
                for s in state:
                    s.observation.clue = ""
                    s.observation.guesses_remaining = 0
                    s.observation.current_turn = 2 if current_turn == 1 else 0
            else:
                # Correct guess
                for s in state:
                    s.observation.guesses_remaining -= 1
                    
                if state[0].observation.guesses_remaining <= 0:
                    for s in state:
                        s.observation.clue = ""
                        s.observation.guesses_remaining = 0
                        s.observation.current_turn = 2 if current_turn == 1 else 0

        # Win condition check
        revealed = state[0].observation.revealed
        roles = state[0].observation.roles
        blue_left = sum(1 for i in range(BOARD_SIZE) if roles[i] == "blue" and not revealed[i])
        yellow_left = sum(1 for i in range(BOARD_SIZE) if roles[i] == "yellow" and not revealed[i])
        
        if blue_left == 0:
            end_game(winner="blue")
            return
        elif yellow_left == 0:
            end_game(winner="yellow")
            return

        # Next turn setup if not done
        if state[0].status != "DONE":
            for i in range(4):
                state[i].status = "ACTIVE" if i == state[0].observation.current_turn else "INACTIVE"

