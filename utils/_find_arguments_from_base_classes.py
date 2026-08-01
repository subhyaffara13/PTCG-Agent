
def _find_arguments_from_base_classes(
    node: nodes.ClassDef,
) -> tuple[
    dict[str, tuple[str | None, str | None]], dict[str, tuple[str | None, str | None]]
]:
    """Iterate through all bases and get their typing and defaults."""
    pos_only_store: dict[str, tuple[str | None, str | None]] = {}
    kw_only_store: dict[str, tuple[str | None, str | None]] = {}
    # See TODO down below
    # all_have_defaults = True

    for base in reversed(node.mro()):
        if not base.is_dataclass:
            continue
        try:
            base_init: nodes.FunctionDef = base.locals["__init__"][0]
        except KeyError:
            continue

        pos_only, kw_only = base_init.args._get_arguments_data()
        for posarg, data in pos_only.items():
            # if data[1] is None:
            #     if all_have_defaults and pos_only_store:
            #         # TODO: This should return an Uninferable as this would raise
            #         # a TypeError at runtime. However, transforms can't return
            #         # Uninferables currently.
            #         pass
            #     all_have_defaults = False
            pos_only_store[posarg] = data

        for kwarg, data in kw_only.items():
            kw_only_store[kwarg] = data
    return pos_only_store, kw_only_store

