
def construct_groups(
    sources: list[BuildSource],
    separate: bool | list[tuple[list[str], str | None]],
    use_shared_lib: bool,
    group_name_override: str | None,
) -> emitmodule.Groups:
    """Compute Groups given the input source list and separate configs.

    separate is the user-specified configuration for how to assign
    modules to compilation groups (see mypycify docstring for details).

    This takes that and expands it into our internal representation of
    group configuration, documented in mypyc.emitmodule's definition
    of Group.
    """

    if separate is True:
        groups: emitmodule.Groups = [([source], None) for source in sources]
    elif isinstance(separate, list):
        groups = []
        used_sources = set()
        for files, name in separate:
            normalized_files = {os.path.normpath(f) for f in files}
            group_sources = [
                src
                for src in sources
                if src.path is not None and os.path.normpath(src.path) in normalized_files
            ]
            groups.append((group_sources, name))
            used_sources.update(group_sources)
        unused_sources = [src for src in sources if src not in used_sources]
        if unused_sources:
            groups.extend([([source], None) for source in unused_sources])
    else:
        groups = [(sources, None)]

    # Generate missing names.
    # Sort the modules to make the compilation results consistent regardless of
    # the source file order passed to mypycify.
    for i, (group, name) in enumerate(groups):
        group = sorted(group, key=lambda source: source.module)
        if use_shared_lib and not name:
            if group_name_override is not None:
                name = group_name_override
            else:
                name = group_name([source.module for source in group])
        groups[i] = (group, name)

    groups = sorted(groups, key=lambda g: (g[1] or "", [s.module for s in g[0]]))
    return groups

