
def import_globals_id_and_name(module_id: str, as_name: str | None) -> tuple[str, str]:
    """Compute names for updating the globals dict with the appropriate module.

    * For 'import foo.bar as baz' we add 'foo.bar' with the name 'baz'
    * For 'import foo.bar' we add 'foo' with the name 'foo'

    Typically we then ignore these entries and access things directly
    via the module static, but we will use the globals version for
    modules that mypy couldn't find, since it doesn't analyze module
    references from those properly."""
    if as_name:
        globals_id = module_id
        globals_name = as_name
    else:
        globals_id = globals_name = module_id.split(".")[0]

    return globals_id, globals_name

