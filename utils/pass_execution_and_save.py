from typing import Any, Callable

def pass_execution_and_save(
    func: Callable[..., Any], gm: GraphModule, inp: Sequence[Any], msg: str
) -> None:
    from .pattern_matcher import stable_topological_sort

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
    ) as f:
        before_io = io.StringIO()
        after_io = io.StringIO()
        ShapeProp(gm=gm, fake_mode=detect_fake_mode(inp)).propagate(*inp)
        print(f"Before:\n{gm.graph}", file=f)
        print(gm.graph, file=before_io)
        start_time = datetime.now()
        with GraphTransformObserver(gm, msg):
            func(gm.graph)
        time_elapsed = datetime.now() - start_time
        # recompile graph
        stable_topological_sort(gm.graph)
        gm.graph.lint()
        gm.recompile()

        print(f"After:\n{gm.graph}", file=f)
        print(gm.graph, file=after_io)
        t = before_io.getvalue() == after_io.getvalue()
        log.info(
            "%s, save before/after graph to %s, graph before/after are the same = %s, time elapsed = %s",
            msg,
            f.name,
            t,
            time_elapsed,
        )

