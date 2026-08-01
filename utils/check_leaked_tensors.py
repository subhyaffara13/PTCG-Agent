
def check_leaked_tensors(limit=1, matched_type=torch.Tensor):
    """Wrap around operations you want to ensure are not leaking tensor memory.

    This code intentionally ignores other reference cycles, which can be benign and which we have plenty
    of in pytorch code.  It focuses on any reference cycles that directly or indirectly result holding a Tensor alive,
    since this is likely a more serious leak than typical python refcycles.

    limit specifies how many tensors to dump debug graphs for (default=1)
    """
    def match_obj(obj):
        return isinstance(obj, matched_type)

    try:
        gc.collect()
        gc.set_debug(gc.DEBUG_SAVEALL)
        garbage_objs = []  # type: ignore[var-annotated]

        # run the user code, after cleaning any existing refcycles, and then check for new ones
        # also allow usercode to check the garbage objs (e.g. for assertion) after exiting ctxmgr
        yield garbage_objs

        gc.collect()
        garbage_objs.extend(filter(match_obj, gc.garbage))
        num_garbage_objs = len(garbage_objs)
        if num_garbage_objs > 0:
            warnings.warn(
                f"{num_garbage_objs} tensors were found in the garbage. Did you introduce a reference cycle?", stacklevel=2
            )
            try:
                import objgraph  # type: ignore[import-not-found,import-untyped]
                warnings.warn(
                    f"Dumping first {limit} objgraphs of leaked {matched_type}s rendered to png", stacklevel=2
                )
                for g in garbage_objs[:limit]:
                    objgraph.show_backrefs([g], max_depth=10)
            except ImportError:
                warnings.warn("`pip install objgraph` to enable memory leak debugging", stacklevel=2)

    finally:
        gc.set_debug(0)

