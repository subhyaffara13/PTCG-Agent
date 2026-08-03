import copy
from typing import Any

def _build_env(game_string: str) -> dict[str, Any]:
    game = pyspiel.load_game(game_string)
    short_name = game.get_type().short_name

    proxy_path = GAMES_DIR / short_name / f"{short_name}_proxy.py"
    if proxy_path.is_file():
        game = pyspiel.load_game(short_name + "_proxy", game.get_parameters())

    game_type = game.get_type()
    if game_type.provides_observation_string:
        observation_type = "observation"
    elif game_type.provides_information_state_string:
        observation_type = "information_state"
    else:
        raise ValueError(f"No observation or information state string for game: {game_string}")

    env_spec = copy.deepcopy(ENV_SPEC_TEMPLATE)
    env_spec["name"] = f"open_spiel_{short_name}"
    env_spec["title"] = f"Open Spiel: {short_name}"
    env_spec["agents"] = [game.num_players()]

    env_config = env_spec["configuration"]
    env_config["episodeSteps"] = game.max_history_length() + DEFAULT_STEP_BUFFER
    env_config["openSpielGameString"]["default"] = str(game)
    env_config["openSpielGameName"]["default"] = short_name
    env_config["openSpielGameParameters"]["default"] = game.get_parameters()
    env_config["observationType"]["default"] = observation_type

    env_obs = env_spec["observation"]
    env_obs["properties"]["openSpielGameString"]["default"] = str(game)
    env_obs["properties"]["openSpielGameName"]["default"] = short_name

    # Building html_renderer_callable is a bit convoluted but other approaches
    # fail for a variety of reasons. Returning a simple lambda function
    # doesn't work because of late-binding -- the last env registered will
    # overwrite all previous renderers.
    js_string_content = _get_html_renderer_content(
        open_spiel_short_name=short_name,
        base_path_for_custom_renderers=GAMES_DIR,
        default_renderer_func=_default_html_renderer,
    )

    def create_html_renderer_closure(captured_content):
        def html_renderer_callable_no_args():
            return captured_content

        return html_renderer_callable_no_args

    html_renderer_callable = create_html_renderer_closure(js_string_content)

    return {
        "specification": env_spec,
        "interpreter": interpreter,
        "renderer": renderer,
        "html_renderer": html_renderer_callable,
        "agents": AGENT_REGISTRY,
    }

