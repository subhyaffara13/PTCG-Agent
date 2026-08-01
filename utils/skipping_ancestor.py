
def skipping_ancestor(manager: BuildManager, id: str, path: str, ancestor_for: State) -> None:
    """Produce an error for an ancestor ignored due to --follow_imports=error"""
    # TODO: Read the path (the __init__.py file) and return
    # immediately if it's empty or only contains comments.
    # But beware, some package may be the ancestor of many modules,
    # so we'd need to cache the decision.
    save_import_context = manager.errors.import_context()
    manager.errors.set_import_context([])
    manager.errors.set_file(ancestor_for.xpath, ancestor_for.id, manager.options)
    manager.error(None, f'Ancestor package "{id}" ignored', only_once=True)
    manager.note(
        None, "(Using --follow-imports=error, submodule passed on command line)", only_once=True
    )
    manager.errors.set_import_context(save_import_context)

