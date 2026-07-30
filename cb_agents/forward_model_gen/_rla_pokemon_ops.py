try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None
from cb_agents.card_utils import _get_prize_yield
import logging
logger = logging.getLogger(__name__)
from ._cache_legal_helpers import _count_high_prize_on_board

def _rla_add_pokemon_actions(gs, card, actions, valid_targets):
    is_energy = False
    is_trainer = False
    if CardRegistry is not None:
        try:
            c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
            if c:
                ct = getattr(c.card_type, "name", "")
                if ct == "ENERGY": is_energy = True
                elif ct == "TRAINER": is_trainer = True
        except Exception: pass
    if is_energy or is_trainer:
        return
    skip_bench = False
    if CardRegistry is not None:
        try:
            cc = CardRegistry().get(int(card) if not isinstance(card, int) else card)
            if cc and _get_prize_yield(cc.card_name) >= 2:
                boss_p = gs.get("boss_prob", 0.0)
                if boss_p > 0.3 and _count_high_prize_on_board(gs) >= 1:
                    skip_bench = True
        except Exception: pass
    bench_list = gs.get("my_bench", [])
    if isinstance(bench_list, list) and len(bench_list) < 5 and not skip_bench:
        actions.append(f"bench:{card}")
    if CardRegistry is not None:
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
        except Exception: pass
