
def get_game(game_name):
  """Returns the game."""
  if game_name == "kuhn_poker_3p":
    game_name = "kuhn_poker"
    game_kwargs = {"players": int(3)}
  elif game_name == "trade_comm_2p_2i":
    game_name = "trade_comm"
    game_kwargs = {"num_items": int(2)}
  elif game_name == "sheriff_2p_gabriele":
    game_name = "sheriff"
    game_kwargs = {
        "item_penalty": float(1.0),
        "item_value": float(5.0),
        "max_bribe": int(2),
        "max_items": int(10),
        "num_rounds": int(2),
        "sheriff_penalty": float(1.0),
    }

  else:
    raise ValueError("Unrecognised game: %s" % game_name)
  return pyspiel.load_game_as_turn_based(game_name, game_kwargs)


def get_game(game_name):
  """Returns the game."""

  if game_name == "kuhn_poker_2p":
    game_name = "kuhn_poker"
    game_kwargs = {"players": int(2)}
  elif game_name == "kuhn_poker_3p":
    game_name = "kuhn_poker"
    game_kwargs = {"players": int(3)}
  elif game_name == "kuhn_poker_4p":
    game_name = "kuhn_poker"
    game_kwargs = {"players": int(4)}

  elif game_name == "leduc_poker_2p":
    game_name = "leduc_poker"
    game_kwargs = {"players": int(2)}
  elif game_name == "leduc_poker_3p":
    game_name = "leduc_poker"
    game_kwargs = {"players": int(3)}
  elif game_name == "leduc_poker_4p":
    game_name = "leduc_poker"
    game_kwargs = {"players": int(4)}

  elif game_name == "trade_comm_2p_2i":
    game_name = "trade_comm"
    game_kwargs = {"num_items": int(2)}
  elif game_name == "trade_comm_2p_3i":
    game_name = "trade_comm"
    game_kwargs = {"num_items": int(3)}
  elif game_name == "trade_comm_2p_4i":
    game_name = "trade_comm"
    game_kwargs = {"num_items": int(4)}
  elif game_name == "trade_comm_2p_5i":
    game_name = "trade_comm"
    game_kwargs = {"num_items": int(5)}

  elif game_name == "tiny_bridge_2p":
    game_name = "tiny_bridge_2p"
    game_kwargs = {}
  elif game_name == "tiny_bridge_4p":
    game_name = "tiny_bridge_4p"
    game_kwargs = {}  # Too big game.

  elif game_name == "sheriff_2p_1r":
    game_name = "sheriff"
    game_kwargs = {"num_rounds": int(1)}
  elif game_name == "sheriff_2p_2r":
    game_name = "sheriff"
    game_kwargs = {"num_rounds": int(2)}
  elif game_name == "sheriff_2p_3r":
    game_name = "sheriff"
    game_kwargs = {"num_rounds": int(3)}
  elif game_name == "sheriff_2p_gabriele":
    game_name = "sheriff"
    game_kwargs = {
        "item_penalty": float(1.0),
        "item_value": float(5.0),
        "max_bribe": int(2),
        "max_items": int(10),
        "num_rounds": int(2),
        "sheriff_penalty": float(1.0),
    }

  elif game_name == "goofspiel_2p_3c_total":
    game_name = "goofspiel"
    game_kwargs = {
        "players": int(2),
        "returns_type": "total_points",
        "num_cards": int(3)}
  elif game_name == "goofspiel_2p_4c_total":
    game_name = "goofspiel"
    game_kwargs = {
        "players": int(2),
        "returns_type": "total_points",
        "num_cards": int(4)}
  elif game_name == "goofspiel_2p_5c_total":
    game_name = "goofspiel"
    game_kwargs = {
        "imp_info": True,
        "egocentric": True,
        "players": int(2),
        "returns_type": "total_points",
        "num_cards": int(5)
    }
  elif game_name == "goofspiel_2p_5c_dsc_total":
    game_name = "goofspiel"
    game_kwargs = {
        "imp_info": True,
        "egocentric": True,
        "points_order": "descending",
        "players": int(2),
        "returns_type": "total_points",
        "num_cards": int(5)
    }
  elif game_name == "goofspiel_2p_5c_dsc_pt_diff":
    game_name = "goofspiel"
    game_kwargs = {
        "imp_info": True,
        "egocentric": True,
        "points_order": "descending",
        "players": int(2),
        "returns_type": "point_difference",
        "num_cards": int(5)
    }

  else:
    raise ValueError("Unrecognised game: %s" % game_name)

  return pyspiel.load_game_as_turn_based(game_name, game_kwargs)

