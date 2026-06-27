import logging
from typing import Dict, List, Optional, Tuple
from cb_agents.heuristic_pipeline_check import check_lethal as _check_lethal_impl, mask_illegal as _mask_illegal_impl, _calc_sig as _calc_sig_impl
from cb_agents.heuristic_pipeline_eval import score_action as _score_action_impl, score_state as _score_state_impl
from cb_agents.heuristic_pipeline_search import thinning_value as _thinning_value_impl, pick_best_search as _pick_best_search_impl, dead_weight as _dead_weight_impl

logger = logging.getLogger(__name__)

_SEARCH_KEYWORDS = {"ultra", "nest", "level", "heavy", "quick", "pokeball", "signal", "secret box", "petrel", "earthen vessel"}
_ABILITY_DRAW_KEYWORDS = {"colress", "concealed", "flower selecting", "shining arcana"}
_DRAW_SUPPORTERS = {"research", "iono", "judge", "concealed cards", "flower selecting", "shining arcana", "colress"}


class HeuristicPipeline:
    check_lethal = staticmethod(_check_lethal_impl)
    score_action = staticmethod(_score_action_impl)
    score_state = staticmethod(_score_state_impl)
    thinning_value = staticmethod(_thinning_value_impl)
    pick_best_search = staticmethod(_pick_best_search_impl)
    dead_weight = staticmethod(_dead_weight_impl)
    mask_illegal = staticmethod(_mask_illegal_impl)
    _calc_sig = staticmethod(_calc_sig_impl)

    def check_bypass(self, candidates: list, gs: dict, rules: dict) -> Optional[str]:
        try:
            dc = gs.get("my_deck_count", 60)
            hand = gs.get("my_hand", [])
            hd = self.dead_weight(candidates, gs)
            if isinstance(hand, list):
                hs = "strong" if len(hand) >= 7 else ("medium" if len(hand) >= 4 else "weak")
            else:
                hs = "weak"
            if dc > 5:
                if hs == "weak" and not hd:
                    bs = self.pick_best_search(candidates)
                    if bs: logger.debug(f"Bypass: {bs} (search - weak)"); return bs
                    for ca in candidates:
                        if ca.startswith("ability:"):
                            t = ca.split(":", 1)[1].lower()
                            if any(d in t for d in _ABILITY_DRAW_KEYWORDS):
                                logger.debug(f"Bypass: {ca} (ability draw - weak)"); return ca
                    for ca in candidates:
                        if ca.startswith("play_trainer:"):
                            t = ca.split(":", 1)[1].lower()
                            if any(d in t for d in _DRAW_SUPPORTERS):
                                logger.debug(f"Bypass: {ca} (supporter draw - weak)"); return ca
                elif hd:
                    bs = self.pick_best_search(candidates)
                    if bs: logger.debug(f"Bypass: {bs} (search - dead={hd})"); return bs
                    for ca in candidates:
                        if ca.startswith("ability:"):
                            t = ca.split(":", 1)[1].lower()
                            if any(d in t for d in _ABILITY_DRAW_KEYWORDS):
                                logger.debug(f"Bypass: {ca} (ability - dead={hd})"); return ca
                    for ca in candidates:
                        if ca.startswith("play_trainer:"):
                            t = ca.split(":", 1)[1].lower()
                            if any(d in t for d in _DRAW_SUPPORTERS):
                                logger.debug(f"Bypass: {ca} (supporter - dead={hd})"); return ca
            if hs == "medium":
                hp = gs.get("supporter_played_this_turn", False)
                if not hp:
                    for ca in candidates:
                        if ca.startswith("ability:"):
                            t = ca.split(":", 1)[1].lower()
                            if any(d in t for d in _ABILITY_DRAW_KEYWORDS):
                                logger.debug(f"Bypass: {ca} (medium hand, ability draw)"); return ca
        except Exception as e:
            logger.error(f"check_bypass failed: {e}", exc_info=True)
        return None

    def mask_actions(self, actions: list, game_state: dict) -> Tuple[list, Dict[str, list]]:
        filtered = self.mask_illegal(actions, game_state)
        bench = game_state.get("my_bench", [])
        bench_sigs = {}
        for i, poke in enumerate(bench):
            if isinstance(poke, dict):
                bench_sigs[i] = f"{poke.get('id', '?')}_{poke.get('hp', '?')}_{len(poke.get('attached', []))}"
            else:
                bench_sigs[i] = f"unknown_{i}"
        groups = {}
        for action in filtered:
            sig = self._calc_sig(action, bench_sigs, game_state)
            groups.setdefault(sig, []).append(action)
        canon = {g[0]: g for sig, g in groups.items()}
        return list(canon.keys()), canon


pipeline = HeuristicPipeline()

_action_score = pipeline.score_action
_state_heuristics = pipeline.score_state
_thinning_value = pipeline.thinning_value
_pick_best_search = pipeline.pick_best_search
_dead_weight_heuristic = pipeline.dead_weight
check_mcts_bypass = pipeline.check_bypass
