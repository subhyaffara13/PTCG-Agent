
def update_visibility(state):
    # Mask roles for guessers (agents 1 and 3)
    roles = state[0].observation.roles
    revealed = state[0].observation.revealed
    
    for i in range(4):
        if i in [1, 3]:  # Guessers
            # Guessers only see roles of revealed cards
            masked_roles = [roles[j] if revealed[j] else "Unknown" for j in range(BOARD_SIZE)]
            state[i].observation.roles = masked_roles
        else:
            state[i].observation.roles = roles[:]

