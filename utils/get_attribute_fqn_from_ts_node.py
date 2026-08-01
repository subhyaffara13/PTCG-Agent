
def get_attribute_fqn_from_ts_node(
    name_to_attribute_fqn: dict[str, str], node: torch._C.Node
) -> str:
    def get_attr(name: str):
        if name in name_to_attribute_fqn:
            return name_to_attribute_fqn[name]
        else:
            raise ValueError(f"Attribute {name} not found")

    if node.kind() == "prim::SetAttr":
        input_name = next(node.inputs()).debugName()
    elif node.kind() == "prim::GetAttr":
        input_name = node.input().debugName()
    else:
        raise RuntimeError(
            f"Unexpected node kind when getting attribute fqn. node: {node} "
        )

    attr_name = node.s("name")
    root_attr_name = get_attr(input_name)
    attr_fqn = f"{root_attr_name}.{attr_name}" if root_attr_name else attr_name

    return attr_fqn

