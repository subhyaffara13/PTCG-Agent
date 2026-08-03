from typing import Any

def convert_symbol_table_node(self: SymbolTableNode, cfg: Config) -> Json:
    data: dict[str, Any] = {".class": "SymbolTableNode", "kind": node_kinds[self.kind]}
    if self.module_hidden:
        data["module_hidden"] = True
    if not self.module_public:
        data["module_public"] = False
    if self.implicit:
        data["implicit"] = True
    if self.plugin_generated:
        data["plugin_generated"] = True
    if self.cross_ref:
        data["cross_ref"] = self.cross_ref
    else:
        # Read the raw node without cross-reference fixup, since exportjson reads
        # cache files in isolation and no node fixer is available.
        node = self.read_node_no_fixup()
        if node is not None:
            data["node"] = convert_symbol_node(node, cfg)
    return data

