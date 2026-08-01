
def discard_graph_changes(tx: "InstructionTranslator") -> Generator[None, None, None]:
    ctx = tx.output.subtracer("subgraph_wrapper", None)
    try:
        ctx.__enter__()
        yield
    finally:
        ctx.__exit__(None, None, None)

