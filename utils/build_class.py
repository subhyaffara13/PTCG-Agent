
def build_class(
    name: str,
    parent: nodes.NodeNG,
    basenames: Iterable[str] = (),
    doc: str | None = None,
) -> nodes.ClassDef:
    """Create and initialize an astroid ClassDef node."""
    node = nodes.ClassDef(
        name,
        lineno=0,
        col_offset=0,
        end_lineno=0,
        end_col_offset=0,
        parent=parent,
    )
    node.postinit(
        bases=[
            nodes.Name(
                name=base,
                lineno=0,
                col_offset=0,
                parent=node,
                end_lineno=None,
                end_col_offset=None,
            )
            for base in basenames
        ],
        body=[],
        decorators=None,
        doc_node=nodes.Const(value=doc) if doc else None,
    )
    return node

