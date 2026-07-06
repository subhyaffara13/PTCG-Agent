import logging
from pathlib import Path
from factory.game_adapter_helpers import get_mapped_indices, get_card_id

logger = logging.getLogger(__name__)

def make_smart_choice(select: dict, observation: dict, fallback_action: list[int], skills_dir: str) -> list[int]:
    try:
        options = select.get("option", [])
        if not options:
            return fallback_action
            
        max_count = select.get("maxCount", 1)
        sel_type = select.get("type")
        
        # Load CardRegistry
        try:
            from agents.card_registry import CardRegistry
            registry = CardRegistry(skills_dir=skills_dir)
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        is_discard = False
        if sel_type == 2:
            try:
                current = observation.get("current")
                if current is not None:
                    my_idx = current.get("yourIndex", 0)
                    players = current.get("players", [])
                    if len(players) > my_idx and players[my_idx] is not None:
                        my_hand = [c.get("id") for c in players[my_idx].get("hand", []) if c and c.get("id") is not None]
                        option_ids = [opt.get("id") for opt in options]
                        if option_ids and all(oid in my_hand for oid in option_ids if oid is not None):
                            is_discard = True
            except Exception:
                pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = opt.get("id")
            card_name = opt.get("name", "")
            
            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)

            scored_options.append((idx, score))

        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        logger.error(f"[smart_choice] Exception during choice: {e}")
        return fallback_action

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
            return make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action
