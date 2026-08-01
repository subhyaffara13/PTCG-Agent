
def mark_invalid(agent, message):
    agent.status = "INVALID"
    agent.reward = -100
    agent.info.debug_info = message

