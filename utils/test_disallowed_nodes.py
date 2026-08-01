
def test_disallowed_nodes(engine, parser):
    VisitorClass = _parsers[parser]
    inst = VisitorClass("x + 1", engine, parser)

    for ops in VisitorClass.unsupported_nodes:
        msg = "nodes are not implemented"
        with pytest.raises(NotImplementedError, match=msg):
            getattr(inst, ops)()

