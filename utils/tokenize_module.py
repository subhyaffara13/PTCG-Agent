
def tokenize_module(node: nodes.Module) -> list[tokenize.TokenInfo]:
    with node.stream() as stream:
        readline = stream.readline
        return list(tokenize.tokenize(readline))

