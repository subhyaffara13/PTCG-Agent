
def _update_mcts_module(ptcg_core_module):
    """Helper to dynamically patch mcts_engine with C++ simulator module."""
    import sys
    for name, mod in list(sys.modules.items()):
        if name == "cb_agents.mcts_engine" or name.endswith("mcts_engine"):
            setattr(mod, "ptcg_core", ptcg_core_module)
            setattr(mod, "HAS_CPP", True)


def _update_mcts_module(ptcg_core_module):
    """Helper to dynamically patch mcts_engine with C++ simulator module."""
    import sys
    for name, mod in list(sys.modules.items()):
        if name == "cb_agents.mcts_engine" or name.endswith("mcts_engine"):
            setattr(mod, "ptcg_core", ptcg_core_module)
            setattr(mod, "HAS_CPP", True)


def _update_mcts_module(ptcg_core_module):
    """Helper to dynamically patch mcts_engine with C++ simulator module."""
    import sys
    for name, mod in list(sys.modules.items()):
        if name == "cb_agents.mcts_engine" or name.endswith("mcts_engine"):
            setattr(mod, "ptcg_core", ptcg_core_module)
            setattr(mod, "HAS_CPP", True)


def _update_mcts_module(ptcg_core_module):
    """Helper to dynamically patch mcts_engine with C++ simulator module."""
    import sys
    for name, mod in list(sys.modules.items()):
        if name == "cb_agents.mcts_engine" or name.endswith("mcts_engine"):
            setattr(mod, "ptcg_core", ptcg_core_module)
            setattr(mod, "HAS_CPP", True)

