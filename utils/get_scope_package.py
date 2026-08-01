
def get_scope_package(
    node: nodes.Item,
    fixturedef: FixtureDef[object],
) -> nodes.Node | None:
    from _pytest.python import Package

    for parent in node.iter_parents():
        if isinstance(parent, Package):
            if fixturedef.node is not None:
                if parent == fixturedef.node:
                    return parent
            else:
                if parent.nodeid == fixturedef.baseid:
                    return parent
    return node.session

