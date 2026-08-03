import json
from typing import Any, Callable

def create_agent_fn(
    game_harness: GameHarness,
    *,
    max_retries: int = 2,
    model_override: tuple[str, dict[str, Any]] | None = None,
) -> Callable[[Any, dict[str, Any]], dict[str, Any]]:
    """Create a Kaggle-compatible agent function from a ``GameHarness``.

    Args:
        game_harness: Game-specific harness implementing the three required
            methods.
        max_retries: Maximum number of prompt attempts (including the initial
            attempt).
        model_override: Optional ``(model_name, litellm_kwargs)`` pair. When
            provided, ``_setup_model`` is bypassed entirely -- useful for
            test harnesses or multi-agent runners (e.g. the ablation runner)
            that need per-agent model selection without polluting global env
            vars. The caller is responsible for any model-name prefixing
            (``openai/...``, ``gemini/...``) and litellm kwargs (api_base,
            api_key, reasoning_effort) the chosen model needs.

    Returns:
        ``agent_fn(obs, config) -> {"submission": <action>, ...}``
    """
    # --- closure state (per agent, not per module) ---
    setup_done = False
    model_name: str = ""
    litellm_kwargs: dict[str, Any] = {}
    move_history: list[str] = []

    def agent_fn(
        obs: dict[str, Any] | Any,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        nonlocal setup_done, model_name, litellm_kwargs

        # -- one-time setup --
        if not setup_done:
            if model_override is not None:
                model_name, litellm_kwargs = model_override
            else:
                model_name, litellm_kwargs = _setup_model()
            _TELEMETRY(
                setup_complete=True,
                model_name=model_name,
            )
            setup_done = True

        save_prompt = bool(config.get("savePrompt", True)) if config else True
        save_response = bool(config.get("saveResponse", True)) if config else True
        include_generate_returns = (
            bool(config.get("includeGenerateReturns", False)) if config else False
        )

        observation = obs if isinstance(obs, dict) else vars(obs)

        # -- inactive-call guard --
        # Runners may invoke the agent when it isn't actually our turn (game
        # over, opponent to move, or the very first probe before the env
        # interpreter has populated state). Return a no-op rather than crash.
        is_terminal = observation.get("isTerminal")
        player_id = observation.get("playerId")
        current_player = observation.get("currentPlayer")
        if is_terminal:
            _TELEMETRY(inactive_call="terminal")
            return {"submission": None, "status": "INACTIVE"}
        # Simultaneous-move games report ``currentPlayer == -2``
        # (pyspiel.PlayerId.SIMULTANEOUS): every player_id is "current" until
        # the round resolves, so skip the not-our-turn check in that case.
        SIMULTANEOUS_PLAYER_ID = -2
        if (
            player_id is not None
            and current_player is not None
            and current_player != SIMULTANEOUS_PLAYER_ID
            and player_id != current_player
        ):
            _TELEMETRY(inactive_call="not_our_turn")
            return {"submission": None, "status": "INACTIVE"}

        # -- legal moves --
        allow_free_form = bool(config.get("freeForm", False)) if config else False
        legal_moves = game_harness.get_legal_moves(observation)
        free_form = legal_moves is None and allow_free_form

        if not legal_moves:
            if free_form:
                legal_action_strings = None
            else:
                # Distinguish "obs not yet populated" (None signals) from
                # a real bug (it IS our turn but the game offers nothing).
                if player_id is None and current_player is None:
                    _log.warning(
                        "core_harness: agent invoked with empty observation "
                        "(keys=%s); returning no-op.",
                        sorted(observation.keys()),
                    )
                    _TELEMETRY(inactive_call="empty_obs")
                    return {"submission": None, "status": "INACTIVE"}
                _TELEMETRY(no_legal_actions=True)
                raise ValueError("No legal actions available.")
        else:
            legal_action_strings = list(legal_moves.values())
            legal_actions = list(legal_moves.keys())

        # -- prompt / parse / retry loop --
        previous_response: str | None = None
        previous_action: str | None = None
        last_content = ""
        all_responses: list[str] = []
        call_records: list[dict[str, Any]] = []
        last_exception: Exception | None = None

        for attempt in range(max_retries):
            if attempt == 0:
                _TELEMETRY(initial_attempt=True)
            else:
                _TELEMETRY(rethinking_attempt={"number": attempt})

            _TELEMETRY(calling_sampler=True)

            prompt = game_harness.make_prompt(
                observation,
                move_history,
                previous_response=previous_response,
                previous_action=previous_action,
            )

            try:
                content, call_details = _call_llm(
                    prompt, model_name, litellm_kwargs,
                )
                last_content = content
                all_responses.append(content)
                call_records.append({
                    "content": content,
                    "prompt": prompt,
                    "model": model_name,
                    **call_details,
                })
                result = game_harness.parse_response(
                    content, legal_action_strings, observation=observation,
                )
                last_exception = None
            except Exception as exc:
                last_exception = exc
                _log.warning(
                    "Attempt %d failed with exception: %s", attempt + 1, exc,
                )
                continue

            # -- check for a valid action --
            matched_submission: Any = None
            action_str: str | None = None

            if free_form and result.submission is not None:
                matched_submission = result.submission
                action_str = str(result.submission)
            elif not free_form and result.legal_action is not None:
                idx = legal_action_strings.index(result.legal_action)
                matched_submission = legal_actions[idx]
                action_str = result.legal_action

            if action_str is not None:
                move_history.append(action_str)
                _TELEMETRY(
                    action_is_legal=True,
                    legal_action={
                        "raw_action": result.raw_action,
                        "legal_action": action_str,
                    },
                )
                action: dict[str, Any] = {
                    "submission": matched_submission,
                    "actionString": action_str,
                    "thoughts": result.thoughts if result.thoughts is not None else last_content,
                    "status": "OK",
                    "call_details": [
                        _build_call_detail(r, save_prompt, save_response)
                        for r in call_records
                    ],
                }
                if include_generate_returns:
                    action["generate_returns"] = [
                        json.dumps(_build_generate_return(r))
                        for r in call_records
                    ]
                return action

            # -- parse failed → prepare rethink --
            # Categorize the failure so dashboards can tell apart:
            #   EMPTY      -> LLM returned no usable content at all
            #   UNPARSABLE -> content present, but parser couldn't extract
            #                 a structured answer (raw_action is None)
            #   ILLEGAL    -> parser extracted something, but it didn't
            #                 match a legal move
            if not (content or "").strip():
                failure_category = "EMPTY"
            elif result.raw_action is None:
                failure_category = "UNPARSABLE"
            else:
                failure_category = "ILLEGAL"
            _TELEMETRY(
                action_is_legal=False,
                parse_failure={
                    "attempt": attempt + 1,
                    "category": failure_category,
                    "raw_action": result.raw_action,
                    "response_preview": content[:200],
                },
            )
            previous_action = result.raw_action
            previous_response = content
            _log.warning(
                "Attempt %d: failed to parse a legal move.", attempt + 1,
            )

        # -- all attempts exhausted --
        # `failure_category` here reports the LAST attempt's failure
        # category (EMPTY / UNPARSABLE / ILLEGAL). Set defensively in
        # case max_retries was 0 and the variable was never assigned.
        _TELEMETRY(
            all_attempts_failed=True,
            total_attempts=max_retries,
            final_failure_category=locals().get("failure_category"),
        )
        if last_exception is not None:
            raise last_exception

        # Fallback is False: -1 as a forfeit signal is an OpenSpiel
        # convention (pyspiel.INVALID_ACTION), and the open_spiel_env spec
        # opts in by declaring `illegalMoveForfeit` with default True. Any
        # other environment can support the parameter by adding it to its
        # own spec and treating submission=-1 as an invalid action.
        illegal_move_forfeit = (
            bool(config.get("illegalMoveForfeit", False)) if config else False
        )
        if illegal_move_forfeit:
            # Mimic game_arena: submit pyspiel.INVALID_ACTION (-1) so the env
            # marks this player INVALID and forfeits them, rather than
            # raising and voiding the whole episode.
            _TELEMETRY(illegal_move_forfeit=True)
            action = {
                "submission": -1,
                "actionString": previous_action,
                "thoughts": last_content,
                "status": (
                    f"Failed to parse a legal move after {max_retries}"
                    " attempts; forfeiting."
                ),
                "call_details": [
                    _build_call_detail(r, save_prompt, save_response)
                    for r in call_records
                ],
            }
            if include_generate_returns:
                action["generate_returns"] = [
                    json.dumps(_build_generate_return(r)) for r in call_records
                ]
            return action

        raise ValueError(
            f"Failed to parse a legal move after {max_retries} attempts. "
            f"End of last response: {last_content[-200:]}"
        )

    return agent_fn

