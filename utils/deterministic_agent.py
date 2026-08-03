import random

def deterministic_agent(obs):
    raw_obs = get_raw_observation(obs)

    entries = raw_obs.new_player_event_views
    current_phase = DetailedPhase(raw_obs.detailed_phase)
    my_role = raw_obs.role
    my_id = raw_obs.player_id
    alive_players = raw_obs.alive_players
    day = raw_obs.day
    phase = raw_obs.game_state_phase
    common_args = {"day": day, "phase": phase, "actor_id": my_id}

    action = NoOpAction(**common_args, reasoning="There's nothing to be done.")  # Default action
    threat_level = random.choice(_PERCEIVED_THREAT_LEVELS)

    if current_phase == DetailedPhase.NIGHT_AWAIT_ACTIONS:
        if my_role == RoleConst.WEREWOLF:
            history_entry = get_last_action_request(entries, EventName.VOTE_REQUEST)
            if history_entry:
                valid_targets = history_entry.data.get("valid_targets")
                if valid_targets:
                    # always select first valid
                    target_id = valid_targets[0]
                    action = VoteAction(
                        **common_args,
                        target_id=target_id,
                        reasoning=FIXED_REASONING,
                        perceived_threat_level=threat_level,
                    )

        elif my_role == RoleConst.DOCTOR:
            history_entry = get_last_action_request(entries, EventName.HEAL_REQUEST)
            if history_entry:
                valid_targets = history_entry.data["valid_candidates"]
                if valid_targets:
                    target_id = valid_targets[0]
                    action = HealAction(
                        **common_args,
                        target_id=target_id,
                        reasoning=FIXED_REASONING,
                        perceived_threat_level=threat_level,
                    )

        elif my_role == RoleConst.SEER:
            history_entry = get_last_action_request(entries, EventName.INSPECT_REQUEST)
            if history_entry:
                valid_targets = history_entry.data["valid_candidates"]
                if valid_targets:
                    target_id = valid_targets[0]
                    action = InspectAction(
                        **common_args,
                        target_id=target_id,
                        reasoning=FIXED_REASONING,
                        perceived_threat_level=threat_level,
                    )

    elif current_phase in [DetailedPhase.DAY_BIDDING_AWAIT, DetailedPhase.DAY_CHAT_AWAIT]:
        if current_phase == DetailedPhase.DAY_BIDDING_AWAIT:
            if my_id in alive_players:
                action = BidAction(
                    **common_args,
                    amount=4,
                    reasoning=FIXED_REASONING,
                    perceived_threat_level=threat_level,
                )
        else:  # It's a chat turn (DAY_CHAT_AWAIT)
            if my_id in alive_players:
                action = ChatAction(
                    **common_args,
                    message=FIXED_MESSAGE,
                    reasoning=FIXED_REASONING,
                    perceived_threat_level=threat_level,
                )

    elif current_phase == DetailedPhase.DAY_VOTING_AWAIT:
        if my_id in alive_players:
            # A real agent would parse the prompt for valid targets
            valid_targets = [p_id for p_id in alive_players if p_id != my_id]
            if valid_targets:
                action = VoteAction(
                    **common_args,
                    target_id=valid_targets[0],
                    reasoning=FIXED_REASONING,
                    perceived_threat_level=threat_level,
                )

    return action.serialize()

