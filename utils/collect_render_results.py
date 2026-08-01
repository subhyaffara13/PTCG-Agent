
def collect_render_results(env):
    results = []

    env.reset()
    for i in range(5):
        if i > 0:
            for agent in env.agent_iter(env.num_agents // 2 + 1):
                obs, reward, terminated, truncated, info = env.last()
                if terminated or truncated:
                    action = None
                elif isinstance(obs, dict) and "action_mask" in obs:
                    action = env.action_space(agent).sample(obs["action_mask"])
                else:
                    action = env.action_space(agent).sample()
                env.step(action)
        render_result = env.render()
        results.append(render_result)

    return results

