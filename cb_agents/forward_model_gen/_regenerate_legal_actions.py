try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None
from cb_agents.card_utils import _get_prize_yield
from cb_agents.forward_model_gen._cache_legal_helpers import _legal_actions_cache
import logging
logger = logging.getLogger(__name__)
from ._cache_legal_helpers import _cache_legal, _count_high_prize_on_board, _legal_cache_key

def _regenerate_legal_actions(gs: dict) -> None:
    if gs.get("turn_ended"):
        gs["legal_actions"] = []
        return

    ck = _legal_cache_key(gs)
    cached = _legal_actions_cache.get(ck)
    if cached is not None:
        gs["legal_actions"] = list(cached)
        return

    # Prize selection phase: only take_prize actions are legal
    if gs.get("select_prize"):
        my_prizes = gs.get("my_prizes", [])
        if isinstance(my_prizes, list) and my_prizes:
            n = min(gs.get("prize_count", 1), len(my_prizes))
            actions = [f"take_prize:{i}" for i in range(n)]
        else:
            actions = [f"take_prize:{i}" for i in range(gs.get("prize_count", 1))]
        gs["legal_actions"] = actions
        _cache_legal(ck, actions)
        return
    
    actions = ["pass"]
    hand = gs.get("my_hand", [])
    if isinstance(hand, list) and len(hand) > 0:
        valid_targets = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs.get("my_active_pokemon"):
            valid_targets.append(str(gs["my_active_pokemon"].get("id", "")))
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            for p in bench:
                if isinstance(p, dict) and p.get("id"):
                    valid_targets.append(str(p["id"]))

        for card in hand:
            is_energy = False
            is_trainer = False
            c = None
            if CardRegistry is not None:
                try:
                    c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if c:
                        ct = getattr(c.card_type, "name", "")
                        if ct == "ENERGY":
                            is_energy = True
                        elif ct == "TRAINER":
                            is_trainer = True
                except Exception as e:
                    logger.debug(f"Action prior generator: card {card} resolution failed: {e}")
            if is_energy:
                if valid_targets:
                    for target in valid_targets:
                        if target: actions.append(f"attach_energy:{card}:{target}")
                else:
                    actions.append(f"attach_energy:{card}")
                continue
            if is_trainer:
                # Enforce one Supporter per turn in MCTS rollouts
                _skip = False
                if gs.get("supporter_played_this_turn") and CardRegistry is not None:
                    try:
                        _fc = CardRegistry().get_full_skill(int(card) if not isinstance(card, int) else card)
                        if _fc and getattr(_fc, 'trainer_subtype', None) and _fc.trainer_subtype.name == "SUPPORTER":
                            _skip = True
                    except Exception:
                        pass
                if not _skip and c is not None:
                    actions.append(f"play_trainer:{c.card_name}")
                continue
            # Boss-aware bench protection: skip benching high-prize if opponent has Boss and we already expose one
            _skip_bench = False
            if CardRegistry is not None:
                try:
                    _cc = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if _cc and _get_prize_yield(_cc.card_name) >= 2:
                        _boss_p = gs.get("boss_prob", 0.0)
                        if _boss_p > 0.3 and _count_high_prize_on_board(gs) >= 1:
                            _skip_bench = True
                except Exception:
                    pass
            # Card is a Pokemon (or unknown): bench it, never attach_energy
            bench_list = gs.get("my_bench", [])
            if isinstance(bench_list, list) and len(bench_list) < 5 and not _skip_bench:
                actions.append(f"bench:{card}")
            # Check if this card can evolve anything on the field
            if CardRegistry is not None and not is_energy and not is_trainer:
                try:
                    crd = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if crd and crd.previous_stage:
                        prev_id = crd.previous_stage
                        prev_id_str = prev_id
                        ap = gs.get("my_active_pokemon", {})
                        if isinstance(ap, dict) and str(ap.get("id", "")) == prev_id_str:
                            actions.append(f"evolve:{card}")
                        else:
                            for bp in gs.get("my_bench", []):
                                if isinstance(bp, dict) and str(bp.get("id", "")) == prev_id_str:
                                    actions.append(f"evolve:{card}")
                                    break
                except Exception:
                    pass
    bench = gs.get("my_bench", [])
    if isinstance(bench, list) and len(bench) > 0:
        for i in range(len(bench)):
            actions.append(f"retreat:{i}")
    opp_hp = gs.get("opponent_active_hp", 100)
    if opp_hp is not None and opp_hp > 0:
        my_active = gs.get("my_active_pokemon")
        can_attack = False
        if isinstance(my_active, dict):
            attached_count = len(my_active.get("attached", []))
            active_id = my_active.get("id")
            if active_id is not None and CardRegistry is not None:
                try:
                    min_cost = CardRegistry().get_min_energy_cost(active_id)
                    can_attack = attached_count >= min_cost
                except Exception:
                    can_attack = attached_count >= 1
            else:
                can_attack = attached_count >= 1
        else:
            can_attack = True
        if can_attack:
            actions.append("attack:strike")
    gs["legal_actions"] = list(dict.fromkeys(actions))
    _cache_legal(ck, gs["legal_actions"])

