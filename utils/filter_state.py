
def filter_state(
  state: State,
  first: filterlib.Filter,
  /,
) -> State: ...


def filter_state(game_state: dict) -> dict:
    return {k: v for k, v in game_state.items() if not k.startswith("_")}

