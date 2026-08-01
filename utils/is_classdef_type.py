
def is_classdef_type(node: nodes.ClassDef) -> bool:
    """Test if ClassDef node is Type."""
    if node.name == "type":
        return True
    return any(isinstance(b, nodes.Name) and b.name == "type" for b in node.bases)

