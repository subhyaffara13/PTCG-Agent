
def _get_fsdp_states_with_modules(
    module: nn.Module,
) -> tuple[list[_FSDPState], list[nn.Module]]:
    """
    Returns a tuple containing:
    1. A list of the ``_FSDPState`` instances in the module tree rooted at
    ``module`` without any duplicates and following the ``module.modules()``
    traversal order (which is assumed to be depth-first).
    2. A corresponding list of the modules owning the states in the first list.

    For the wrapper code path, both returned lists are the same, each
    containing all ``FullyShardedDataParallel`` instances. For the composable
    code path, this returns a list of all composable state instances and a list
    of the corresponding fully sharded modules. See [Note: Fully Sharded
    Module].

    NOTE: The traversal does not proceed into any module annotated by an
    incompatible API (e.g. ``replicate``).
    """
    fsdp_states: list[_FSDPState] = []
    fsdp_modules: list[nn.Module] = []
    # Track the visited FSDP states since multiple modules may share the same
    # one and we want to return a de-duplicated list
    visited_fsdp_states: set[_FSDPState] = set()
    # Track the visited modules in case of shared modules, which implies the
    # module graph is no longer a tree
    visited_modules: set[nn.Module] = set()

    # Perform depth-first search from `module` to ensure that we do not
    # traverse into an incompatible API's subtree (use DFS instead of BFS to
    # match `.modules()` order)
    deque: collections.deque[nn.Module] = collections.deque([module])
    while deque:
        submodule = deque.popleft()
        visited_modules.add(submodule)
        if not _composable(submodule):
            continue
        for child_module in reversed(list(submodule.children())):
            if child_module not in visited_modules:
                deque.appendleft(child_module)
        optional_state = _get_module_fsdp_state(submodule)
        if optional_state is not None and optional_state not in visited_fsdp_states:
            visited_fsdp_states.add(optional_state)
            fsdp_states.append(optional_state)
            fsdp_modules.append(submodule)
    return fsdp_states, fsdp_modules

