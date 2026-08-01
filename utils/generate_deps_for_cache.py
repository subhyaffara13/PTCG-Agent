
def generate_deps_for_cache(manager: BuildManager, graph: Graph) -> dict[str, dict[str, set[str]]]:
    """Generate fine-grained dependencies into a form suitable for serializing.

    This does a couple things:
    1. Splits fine-grained deps based on the module of the trigger
    2. For each module we generated fine-grained deps for, load any previous
       deps and merge them in.

    Returns a dictionary from module ids to all dependencies on that
    module. Dependencies not associated with a module in the build will be
    associated with the nearest parent module that is in the build, or the
    fake module FAKE_ROOT_MODULE if none are.
    """
    from mypy.server.deps import merge_dependencies  # Lazy import to speed up startup

    # Split the dependencies out into based on the module that is depended on.
    rdeps = invert_deps(manager.fg_deps, graph)

    # We can't just clobber existing dependency information, so we
    # load the deps for every module we've generated new dependencies
    # to and merge the new deps into them.
    for module, mdeps in rdeps.items():
        old_deps = manager.load_fine_grained_deps(module)
        merge_dependencies(old_deps, mdeps)

    return rdeps

