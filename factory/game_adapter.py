import logging
from pathlib import Path
from factory.game_adapter_helpers import get_mapped_indices, get_card_id

logger = logging.getLogger(__name__)

def run_agent_turn(orchestrator, observation: dict, deck: list[int]) -> list[int]:
    """Interactions adapter mapping CABT observations to Orchestrator and actions back to options."""
    if not isinstance(observation, dict):
        return deck
    select = observation.get("select")
    if select is None: return deck

    options = select.get("option", [])
    max_count = select.get("maxCount", 1)
    fallback_action = list(range(min(max_count, len(options))))

    try:
        current = observation.get("current")
        if not current: return fallback_action

        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if len(players) <= my_idx: return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}


        from factory.game_adapter_state import build_game_state
        game_state = build_game_state(my_state, opp_state, current)

        # Parse legal candidates from options using their exact index in the array
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 13]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 9]
        game_state["legal_bench"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 8]
        game_state["legal_evolutions"] = [] # Handled by bench type 8 in CABT
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 7]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
        
        sel_type = select.get("type")
        sel_ctx = select.get("context")
        
        game_state["select_prize"] = True if sel_ctx in ("prize", "select_prize") or sel_type == 2 else False
        game_state["select_type"] = sel_type
        game_state["select_context"] = sel_ctx

        # Route ALL decision points through the brain, not just main turn (type=0, ctx=0)
        is_main_turn = (sel_type == 0 and sel_ctx == 0)
        is_target_select = (sel_type == 1)  # Target selection for trainer/ability effects
        is_energy_discard = (sel_type == 4)  # Energy discard for attack cost
        is_energy_attach = (sel_type == 7)   # Energy attachment target
        is_binary_choice = (sel_type == 9)   # Coin flip / binary

        if is_main_turn or game_state["select_prize"] or is_target_select or is_energy_discard or is_energy_attach or is_binary_choice:
            action_label = orchestrator.run_turn(game_state)
            if hasattr(action_label, 'primary_action'):
                action_label = action_label.primary_action

            if is_main_turn and getattr(orchestrator, "last_action", "") != action_label:
                orchestrator.last_action = action_label
                if isinstance(action_label, str) and action_label.startswith("attach_energy:"):
                    parts = action_label.split(":", 2)
                    if len(parts) > 2:
                        orchestrator.last_energy_target = parts[2]
                        
            if is_energy_attach and hasattr(orchestrator, "last_energy_target") and orchestrator.last_energy_target:
                mapped_indices = get_mapped_indices(f"target:{orchestrator.last_energy_target}", options, game_state)
            else:
                mapped_indices = get_mapped_indices(action_label, options, game_state)
                
            if not mapped_indices: mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count: break
            return selected
        else:
            return fallback_action
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action
