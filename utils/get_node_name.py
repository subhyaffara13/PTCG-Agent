from typing import Union

def getNodeName(node):
    # Returns node.id, or node.name, or None
    if hasattr(node, 'id'):     # One of the many nodes with an id
        return node.id
    if hasattr(node, 'name'):   # an ExceptHandler node
        return node.name
    if hasattr(node, 'rest'):   # a MatchMapping node
        return node.rest


def get_node_name(host: str, port: Union[str, int]) -> str:
    return f"{host}:{port}"

