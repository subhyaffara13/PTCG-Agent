
def fixed_prompt_policy(rnd, state, prompt_action_dict):
  # all actions are legal for now
  action = [rnd.choice(a) for a in state.num_actions]
  for prompt_key, prompt_action in prompt_action_dict.items():
    prompt_key_idx = 1 + state.header.action_keys.index(prompt_key)
    prompt_val_idx = state.prompt_actions[prompt_key].index(prompt_action)
    action[prompt_key_idx] = prompt_val_idx
  action = tuple(action)
  return np.ravel_multi_index(action, state.num_actions)

