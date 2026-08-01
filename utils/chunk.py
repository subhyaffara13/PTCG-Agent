
def chunk(a: TensorLikeType, chunks: int, dim: int = 0) -> tuple[TensorLikeType, ...]:
    if chunks <= 0:
        msg = f"Expected at least one chunk, but got {chunks}!"
        raise ValueError(msg)

    dim = utils.canonicalize_dim(a.ndim, dim)
    length = a.shape[dim]
    chunk_size = math.ceil(length / chunks)
    full_chunks = math.floor(length / chunk_size)
    tail_chunk_size = length % chunk_size

    result = [narrow(a, dim, i * chunk_size, chunk_size) for i in range(full_chunks)]

    if tail_chunk_size != 0:
        result.append(narrow(a, dim, full_chunks * chunk_size, tail_chunk_size))

    return tuple(result)


def chunk(gm: GraphModule) -> GraphModule:
    """
    Chunk input tensors for operations that amplify the tensor size significantly.
    The chunking operation is propagated thru the fx graph until a point we should
    re-generate non-chunked tensors.

    Only chunk across the batch dimension of the tensor for now.
    """
    graph = gm.graph

    if torch._inductor.config.cpp_wrapper:
        raise CantChunk("cpp wrapper does not support codegening invoke_subgraph")

    if gm.meta.get("produced_by_chunker", False):
        # Don't chunk a graph produced by the chunker
        return gm

    if len(get_tangent_nodes(gm.graph)) == 0:
        # no tangents. Can be the optimizer graph. Skip chunking
        return gm

    if log.isEnabledFor(logging.DEBUG):
        log.debug("Joint graph before chunking:\n%s", gm.print_readable(False))

    amplifier_node = find_amplifier_node(graph)
    if amplifier_node is None:
        raise CantChunk("Skip chunking due to no amplifier node found")

    if amplifier_node.meta["val"]._has_symbolic_sizes_strides:
        raise CantChunk("Can't chunk due to dynamic shape")

    propagate(amplifier_node)
    if not tangent_has_chunking_meta(gm):
        raise CantChunk(
            "Skip chunking either because the graph is for inference only or "
            "because the chunking metadata does not propagate to the backward "
            "(e.g. due to too trivial loss function)"
        )

    num_chunks = config.auto_chunker.num_chunk or decide_num_chunks(gm)
    out_gm = ChunkingApplier(gm, num_chunks).apply()
    metrics.num_auto_chunking += 1
    log.debug("AutoChunker being applied with %s chunks", num_chunks)
    return out_gm


def chunk(g: jit_utils.GraphContext, self, chunks, dim):
    # Calculate chunk size for dynamic chunk
    dim_size = g.op("Gather", g.op("Shape", self), dim, axis_i=0)
    chunk_size_s = g.op(
        "Sub", chunks, g.op("Constant", value_t=torch.tensor([1], dtype=torch.long))
    )
    chunk_size = g.op("Div", g.op("Add", dim_size, chunk_size_s), chunks)
    # Create splits vector
    chunk_vec = [
        opset9.expand(g, chunk_size, chunk_size_s, None),
        g.op("Sub", dim_size, g.op("Mul", chunk_size, chunk_size_s)),
    ]
    chunk_vec = g.op("Concat", *chunk_vec, axis_i=0)
    return split(g, self, chunk_vec, dim)

