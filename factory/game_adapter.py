import logging
from pathlib import Path
from factory.game_adapter_helpers import get_mapped_indices, get_card_id

logger = logging.getLogger(__name__)

_registry = None

def make_smart_choice(select: dict, observation: dict, fallback_action: list[int], skills_dir: str) -> list[int]:
    global _registry
    try:
        options = select.get("option", [])
        if not options:
            return fallback_action
            
        max_count = select.get("maxCount", 1)
        sel_type = select.get("type")
        
        # Load CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(select.get("context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = observation.get("current")
                    if current is not None:
                        my_idx = current.get("yourIndex", 0)
                        players = current.get("players", [])
                        if len(players) > my_idx and players[my_idx] is not None:
                            my_hand_ids = [c.get("id") for c in players[my_idx].get("hand", []) if c and c.get("id") is not None]
                            
                            option_card_ids = []
                            for opt in options:
                                opt_id = opt.get("id")
                                if opt_id is None:
                                    # Resolve coordinate
                                    area = opt.get("area")
                                    index = opt.get("index")
                                    p_idx = opt.get("playerIndex", 0)
                                    if p_idx == my_idx and area == 2: # Hand
                                        hand = players[my_idx].get("hand", [])
                                        if len(hand) > index:
                                            opt_id = hand[index].get("id")
                                if opt_id is not None:
                                    option_card_ids.append(opt_id)
                            
                            if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                                is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = observation.get("current")
            if current is not None:
                my_idx = current.get("yourIndex", 0)
                players = current.get("players", [])
                if len(players) > my_idx and players[my_idx] is not None:
                    my_state = players[my_idx]
                    act = resolve_instance(my_state.get("active"))
                    if act:
                        # Try to resolve act card name
                        act_name = act.get("name")
                        if not act_name and act.get("card"):
                            act_name = act.get("card").get("name")
                        if act_name: board_pokemon_names.add(str(act_name).lower())
                    for b in my_state.get("bench", []):
                        b_resolved = resolve_instance(b)
                        if b_resolved:
                            b_name = b_resolved.get("name")
                            if not b_name and b_resolved.get("card"):
                                b_name = b_resolved.get("card").get("name")
                            if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = opt.get("id")
            card_name = opt.get("name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = opt.get("area")
                    index = opt.get("index")
                    p_idx = opt.get("playerIndex", 0)
                    current = observation.get("current")
                    if current is not None:
                        players = current.get("players", [])
                        if len(players) > p_idx and players[p_idx] is not None:
                            p_state = players[p_idx]
                            if area == 2: # Hand
                                hand = p_state.get("hand", [])
                                if len(hand) > index:
                                    card_id = hand[index].get("id")
                            elif area == 12: # Bench
                                bench = p_state.get("bench", [])
                                if len(bench) > index:
                                    bench_item = resolve_instance(bench[index])
                                    if bench_item is not None:
                                        card_id = bench_item.get("id")
                            elif area == 4: # Active
                                active = p_state.get("active", [])
                                if len(active) > index:
                                    active_item = resolve_instance(active[index])
                                    if active_item is not None:
                                        card_id = active_item.get("id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    if hasattr(registry, "learned_dos") and int(card_id_int) in registry.learned_dos:
                        score += 12.0
                    if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(select.get("context", "")).lower() in ("energy", "attach"):
                    try:
                        area = opt.get("area")
                        index = opt.get("index")
                        p_idx = opt.get("playerIndex", 0)
                        current = observation.get("current")
                        if current is not None:
                            my_idx = current.get("yourIndex", 0)
                            if p_idx == my_idx:
                                players = current.get("players", [])
                                my_state = players[my_idx]
                                instance = None
                                if area == 4: # Active
                                    instance = resolve_instance(my_state.get("active"))
                                elif area == 12: # Bench
                                    bench = my_state.get("bench", [])
                                    if len(bench) > index:
                                        instance = resolve_instance(bench[index])
                                if instance:
                                    attached = instance.get("attached", [])
                                    attached_count = len(attached) if isinstance(attached, list) else 0
                                    required = getattr(card, "energy_cost", 0)
                                    if attached_count < required:
                                        # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                        target_name = ""
                                        target_id = instance.get("id") if isinstance(instance, dict) else getattr(instance, "id", None)
                                        if target_id is not None and registry:
                                            target_card = registry.get_full_skill(target_id)
                                            if target_card:
                                                target_name = getattr(target_card, "card_name", "").lower()
                                        
                                        is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                        target_hp = instance.get("hp", 100) if isinstance(instance, dict) else getattr(instance, "hp", 100)
                                        target_max_hp = instance.get("maxHp", 100) if isinstance(instance, dict) else getattr(instance, "maxHp", 100)
                                        is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                        
                                        if is_passive_support or is_low_hp:
                                            boost = -15.0
                                        else:
                                            boost = 10.0 * (required - attached_count)
                                            if area == 4:
                                                boost += 5.0
                                        score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = observation.get("current")
                    if current is not None:
                        turn = current.get("turn", 1)
                        if turn <= 5:
                            support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                            card_name_lower = getattr(card, "card_name", "").lower()
                            if any(s in card_name_lower for s in support_names):
                                score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)

            scored_options.append((idx, score))

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        if is_discard:
            try:
                current = observation.get("current", {})
                my_idx = current.get("yourIndex", 0)
                players = current.get("players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(my_state.get("bench", []))
                active_poke = my_state.get("active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = my_state.get("hand", [])
                hand_ids = [c.get("id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = opt.get("id")
                    if cid is None:
                        area = opt.get("area")
                        index = opt.get("index")
                        if area == 2 and len(my_hand) > index:
                            cid = my_hand[index].get("id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(active_poke[0].get("attached", []))
                                for b in my_state.get("bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(b[0].get("attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
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
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (8, 9)]
        
        # Load registry for evolution checking
        global _registry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                _registry = CardRegistry(skills_dir=str(orchestrator.skills_dir))
            registry = _registry
        except Exception:
            registry = None

        legal_bench = []
        legal_evolutions = []
        my_hand = game_state.get("my_hand", [])
        for i, opt in enumerate(options):
            if opt.get("type") == 8:
                is_evo = False
                hand_idx = opt.get("index")
                if hand_idx is not None and 0 <= hand_idx < len(my_hand):
                    card_id = my_hand[hand_idx]
                    if registry and card_id:
                        try:
                            card = registry.get_full_skill(card_id)
                            if card:
                                from cb_agents.card_types import CardStage
                                if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                    is_evo = True
                        except Exception:
                            pass
                if is_evo:
                    legal_evolutions.append(str(i))
                else:
                    legal_bench.append(str(i))

        game_state["legal_bench"] = legal_bench
        game_state["legal_evolutions"] = legal_evolutions
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 7]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
        game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (11, 15)]
        game_state["legal_prize_options"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 2]
        
        sel_type = select.get("type")
        sel_ctx = select.get("context")
        
        game_state["select_prize"] = True if sel_ctx in ("prize", "select_prize") or sel_type == 2 else False
        game_state["select_type"] = sel_type
        game_state["select_context"] = sel_ctx

        # Route only main turn and prize selections to the MCTS engine
        is_main_turn = (sel_type == 0 and sel_ctx == 0)
        is_energy_attach = (sel_type == 7)

        if is_main_turn or game_state["select_prize"]:
            import time
            step_start_time = time.time()
            action_label = orchestrator.run_turn(game_state)
            if time.time() - step_start_time > 1.2:
                logger.warning(f"Step decision took {time.time() - step_start_time:.2f}s (exceeding 1.2s latency guard). Triggering fast fallback.")
                return make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
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
                
            if len(mapped_indices) > 1 or (not mapped_indices and action_label != "pass"):
                smart_cand = make_smart_choice(select, observation, fallback_action, str(orchestrator.skills_dir))
                if smart_cand:
                    if mapped_indices:
                        mapped_indices = [idx for idx in smart_cand if idx in mapped_indices] + [idx for idx in smart_cand if idx not in mapped_indices]
                    else:
                        mapped_indices = smart_cand

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
