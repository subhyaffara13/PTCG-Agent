
def _patch_uuid_class(node: nodes.ClassDef) -> None:
    # The .int member is patched using __dict__
    node.locals["int"] = [nodes.Const(0, parent=node)]

