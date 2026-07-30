import logging
from cb_agents.turn_planner_heuristics import _registry

logger = logging.getLogger(__name__)
_evo_cache = {}
_nn_instance = None

def _has_evolution_target(card_name: str, decklist: dict) -> bool:
    k = (card_name, frozenset(decklist.keys()))
    if k in _evo_cache: return _evo_cache[k]
    try:
        cn = card_name.split("(")[0].strip()
        for cid in decklist:
            c = _registry.get(int(cid))
            if c and c.previous_stage and cn in c.previous_stage.lower():
                _evo_cache[k] = True; return True
        _evo_cache[k] = False; return False
    except:
        return True

def _get_neural_network():
    global _nn_instance
    if _nn_instance is None:
        try:
            from cb_agents.value_network import NeuralValueNetwork
            _nn_instance = NeuralValueNetwork()
        except Exception as e:
            logger.warning(f"Failed to instantiate NeuralValueNetwork: {e}")
    return _nn_instance

