
def check_for_type_equality(g1, g2):
    """
    A check equality to be used in fixed points.
    We do not use graph equality but instead type
    equality.
    """
    for n, m in zip(g1.nodes, g2.nodes):
        if n.type != m.type:
            return False
    return True

