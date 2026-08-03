from typing import Any

def _format_import_block(globals: dict[str, Any], importer: Importer):
    import_strs: set[str] = {
        _format_import_statement(name, obj, importer) for name, obj in globals.items()
    }
    # Sort the imports so we have a stable import block that allows us to
    # hash the graph module and get a consistent key for use in a cache.
    return "\n".join(sorted(import_strs))

