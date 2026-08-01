
def _format_import_statement(name: str, obj: Any, importer: Importer) -> str:
    if name in _custom_builtins:
        return _custom_builtins[name].import_str
    if _is_from_torch(name):
        return "import torch"
    module_name, attr_name = importer.get_name(obj)
    return f"from {module_name} import {attr_name} as {name}"

