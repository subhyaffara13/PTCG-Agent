from typing import Callable, Union

def record_info_state_data(
    state: pyspiel.State,
    policy: pyspiel.Policy,
    observer: Union[None, chat_game_base.ChatGameObserverBase] = None,
    vectorize: Union[None, Callable[[str, int], np.ndarray]] = None,
) -> InfoStateRecord:
  """Return observation and equilibrium strategy for a given state+policy."""
  pi = policy.action_probabilities(state)
  action_list = list(pi.keys())
  prob_list = list(pi.values())
  if observer is not None:
    info_str = observer.string_from(state, player=state.current_player())
    if vectorize is not None:
      info = vectorize(info_str, 768)
    else:
      info = info_str
  else:
    info = info_str = str(state)
  prev_msg = ""
  prev_speaker = -1
  prev_action_strs = []
  if state.played_actions:
    prev_action = state.played_actions[-1]
    prev_msg = state.dialogue[-1]
    prev_speaker = state.speakers[-1]
    prev_speaker = int(prev_speaker)
    prev_action_dict = state.unravel_flat_action_to_dict(prev_speaker,
                                                         prev_action)
    action_keys = state.prompt_actions.keys()
    prev_action_strs = [prev_action_dict["action"][key] for key in action_keys]
  sample = InfoStateRecord(info, info_str, prob_list, action_list,
                           prev_msg, prev_speaker, prev_action_strs)
  return sample

