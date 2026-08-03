from typing import Any

def convert_symbol_table(self: SymbolTable, cfg: Config) -> Json:
    data: dict[str, Any] = {".class": "SymbolTable"}
    for key, value in self.items():
        # Skip __builtins__: it's a reference to the builtins
        # module that gets added to every module by
        # SemanticAnalyzerPass2.visit_file(), but it shouldn't be
        # accessed by users of the module.
        if key == "__builtins__" or value.no_serialize:
            continue
        if not cfg.implicit_names and key in {
            "__spec__",
            "__package__",
            "__file__",
            "__doc__",
            "__annotations__",
            "__name__",
        }:
            continue
        data[key] = convert_symbol_table_node(value, cfg)
    return data

