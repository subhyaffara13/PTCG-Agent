
def skipping_module(
    manager: BuildManager, line: int, caller_state: State | None, id: str, path: str
) -> None:
    """Produce an error for an import ignored due to --follow_imports=error"""
    assert caller_state, (id, path)
    save_import_context = manager.errors.import_context()
    manager.errors.set_import_context(caller_state.import_context)
    manager.errors.set_file(caller_state.xpath, caller_state.id, manager.options)
    manager.error(line, f'Import of "{id}" ignored')
    manager.note(
        line, "(Using --follow-imports=error, module not passed on command line)", only_once=True
    )
    manager.errors.set_import_context(save_import_context)

