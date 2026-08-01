
def _compute_hash(gm: torch.fx.GraphModule) -> int | None:
    """Compute a structural hash of the graph including tensor metadata.

    Uses FxGraphCachePickler(device_id_agnostic=True) to serialize
    (target, val) per call_function node, capturing op targets and
    FakeTensor metadata (dtype, shape, stride, etc.) with device indices
    normalized to 0.

    Returns None if the graph contains unpicklable objects.
    """
    from torch._inductor.codecache import BypassFxGraphCache, FxGraphCachePickler

    try:
        pickler = FxGraphCachePickler(gm, device_id_agnostic=True)
        data = pickler.dumps(
            tuple(
                (str(n.target), n.meta.get("val"))
                for n in gm.graph.nodes
                if n.op == "call_function"
            )
        )
        digest = hashlib.blake2b(data, digest_size=8).digest()
        return int.from_bytes(digest, "big", signed=True)
    except BypassFxGraphCache:
        # FxGraphCachePickler can't serialize certain objects:
        # mkldnn tensors, BackwardState, torchbind objects, or general
        # pickle failures. Skip the SPMD check gracefully.
        log.warning("SPMD check: skipping, unpicklable graph objects", exc_info=True)
        return None

