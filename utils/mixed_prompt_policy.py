
def mixed_prompt_policy(rnd, state, prompt_keys, mixture):
  # all actions are legal for now
  action = [rnd.choice(a) for a in state.num_actions]
  for prompt_key in prompt_keys:
    prompt_key_idx = 1 + state.header.action_keys.index(prompt_key)
    actions = state.prompt_actions[prompt_key]
    num_actions = len(actions)
    prompt_val_idx = rnd.choice(num_actions, p=mixture)
    action[prompt_key_idx] = prompt_val_idx
  action = tuple(action)
  return np.ravel_multi_index(action, state.num_actions)

