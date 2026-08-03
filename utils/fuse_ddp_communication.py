from typing import Callable

def fuse_ddp_communication(
    graph: fx.Graph, passes: list[Callable[..., None] | str], bucket_size_mb: int
) -> None:
    for i, pa in enumerate(passes):
        with GraphTransformObserver(
            graph.owning_module, f"fuse_ddp_communication_pass_{i}"
        ):
            if isinstance(pa, str):
                func = globals()[pa]
            else:
                func = pa
            if "bucket_size_mb" in OrderedSet(
                v.name for v in inspect.signature(func).parameters.values()
            ):
                func(graph, bucket_size_mb=bucket_size_mb)
            else:
                func(graph)

