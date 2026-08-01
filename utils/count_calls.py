
def count_calls(g: fx.Graph) -> int:
    c = 0
    for n in g.nodes:
        if "call" in n.op:
            c += 1
    return c

