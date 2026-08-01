
def log_error(msg, *args, **kwargs):
    '''Log an error message. Arguments are the same as log().'''
    log('{0}{1}ERROR{2}: {3}'.format(BRIGHT, RED, RESET, msg), *args, **kwargs)


def log_error(status_code, state, env):
    invalid_action = any(player_state["status"] == status_code for player_state in state)
    if invalid_action:
        logger.error(f"{status_code} DETECTED")
        for i, player_state in enumerate(state):
            if player_state["status"] == status_code:
                player = env.game_state.players[i]
                logger.error(
                    f"player.id={player.id}, player.agent.agent_id={player.agent.agent_id} "
                    f"returns action with status code {status_code}."
                )
    return invalid_action

