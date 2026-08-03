import os

def _should_debug_node(node_name: str) -> bool:
    def _get_debug_nodes() -> bool | OrderedSet[str]:
        global _debug_nodes_cache, _debug_nodes_env_value_cache

        def parse_debug_env(env_value: str | None) -> bool | OrderedSet[str]:
            if not env_value:
                return False
            if env_value == "all":
                return True
            return OrderedSet(env_value.split(","))

        current_env = os.environ.get("TORCHINDUCTOR_PATTERN_MATCH_DEBUG")

        # Recompute only if env changed
        if current_env != _debug_nodes_env_value_cache or _debug_nodes_cache is None:
            _debug_nodes_cache = parse_debug_env(current_env)
            _debug_nodes_env_value_cache = current_env

        return _debug_nodes_cache

    debug_nodes = _get_debug_nodes()
    if isinstance(debug_nodes, bool):
        return debug_nodes
    return node_name in debug_nodes

