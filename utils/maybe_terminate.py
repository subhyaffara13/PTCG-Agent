
def maybe_terminate(env, state):
    if state[0].status != "ACTIVE" or state[1].status != "ACTIVE":
        if state[0].status == "ACTIVE":
            state[0].status = "DONE"
            state[0].reward = 100
            state[0].info.debug_info = "Opponent forfeited. You win."
        elif not state[0].reward:
            state[0].reward = -100
        if state[1].status == "ACTIVE":
            state[1].status = "DONE"
            state[1].reward = 100
            state[1].info.debug_info = "Opponent forfeited. You win."
        elif not state[1].reward:
            state[1].reward = -100
        try_get_video(env)
        return True
    return False

