from factory.deck_synergy_graph import SynergyGraph
from utils.load_corpus import load_corpus

_GLOBAL_GRAPH = None


def get_global_synergy_graph() -> SynergyGraph:
    global _GLOBAL_GRAPH
    if _GLOBAL_GRAPH is None:
        _GLOBAL_GRAPH = SynergyGraph()
        corpus = load_corpus()
        if corpus:
            _GLOBAL_GRAPH.build_from_corpus(corpus)
    return _GLOBAL_GRAPH

