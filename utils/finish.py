
def finish(state, env):
    if len(env.steps) > 0:
        vis = json.loads(visualize_data())
        for i in range(len(vis)):
            obs = ""
            action = None
            if len(env.steps) > i:
                index = 1
                if env.steps[i][0].status == 'ACTIVE':
                    index = 0
                obs = copy.copy(env.steps[i][index].observation)
                obs.pop("search_begin_input")
                if len(env.steps) > i + 1:
                    action = [env.steps[i + 1][0].action, env.steps[i + 1][1].action]
                else:
                    action = [state[0].action, state[1].action]
            vis[i]["obs"] = obs
            vis[i]["action"] = action
        env.steps[0][0]["visualize"] = vis
    battle_finish()

