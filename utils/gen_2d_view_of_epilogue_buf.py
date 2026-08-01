
def gen_2d_view_of_epilogue_buf(
    Y: ir.Buffer,
    template_buffer: ir.Buffer,
    epilogue_nodes: list[ir.IRNode],
    reindexers: list[Callable[[list[Any]], list[Any]] | None],
    default_reindexers: list[Callable[[list[Any]], list[Any]] | None],
) -> tuple[
    ir.Buffer | ir.ReinterpretView,
    list[Callable[[list[Any]], list[Any]] | None],
]:
    """
    The dimension and the indexing could be different between the GEMM output, i.e. `template_buffer`, which is
    2D with MxN) and the output from the template after epilogues, i.e. `Y`. In the GEMM template code,
    we are not aware of the dimension and the indexing of the epilogues and always work on 2D tiles according to
    the indexing of the GEMM output.
    In this function, we return a 2D buffer (`Y_2d`) according to GEMM output (reinterpreted from `Y` if needed) and
    build a reindexer that converts the indexing of `Y` into `Y_2d`.
    """
    Y_2d: ir.Buffer | ir.ReinterpretView = Y
    if (
        Y.get_size() == template_buffer.get_size()
        and Y.get_stride() == template_buffer.get_stride()
    ):
        reindexers.extend(default_reindexers)
        Y_2d = Y
    else:

        def get_reindexer(epilogue_node, default_reindexer=None):
            # From template_buffer to epilogue_node_ordered (ordered by stride decreasingly, in dense format), for example:
            #   template_buffer:
            #       size (324, 512), stride (512, 1)
            #   epilogue_node_ordered (ordered by stride decreasingly, in dense format):
            #       size (1, 18, 18, 512), stride (165888, 9216, 512, 1)
            stride_order = list(
                ir.get_stride_order(
                    V.graph.sizevars.guarding_hints_or_throw(epilogue_node.get_stride())
                )
            )
            fill_order = ir.stride_order2fill_order(stride_order)
            reversed_fill_order = list(reversed(fill_order))
            size_with_stride_ordered_decreasingly = [
                epilogue_node.get_size()[i] for i in reversed_fill_order
            ]
            reshape_reindex = ir.View.dynamic_reshape_indexer(
                size_with_stride_ordered_decreasingly,
                template_buffer.get_size(),
            )
            if default_reindexer:
                reshape_reindex = ir.fuse_reindexing(reshape_reindex, default_reindexer)

            # From epilogue_node_ordered (ordered by stride decreasingly, in dense format) to epilogue_node, for example:
            #   epilogue_node_ordered (ordered by stride decreasingly, in dense format):
            #       size (1, 18, 18, 512), stride (165888, 9216, 512, 1)
            #   epilogue_node:
            #       size (1, 18, 18, 512), stride (165888, 1, 9216, 512)
            from_stride_ordered_decreasingly_to_epilogue_node_order = [
                (len(stride_order) - 1) - stride_order[i]
                for i in range(len(stride_order))
            ]
            stride_reindex = ir.same_reorder(
                from_stride_ordered_decreasingly_to_epilogue_node_order
            )

            reindexer = ir.fuse_reindexing(stride_reindex, reshape_reindex)  # type: ignore[var-annotated]
            return reindexer

        if default_reindexers is None:
            default_reindexers = [None] * len(epilogue_nodes)
        new_reindexers = [
            get_reindexer(epilogue_node, default_reindexer)
            for epilogue_node, default_reindexer in zip(
                epilogue_nodes, default_reindexers
            )
        ]
        reindexers.extend(new_reindexers)
        if isinstance(Y, ir.BaseView):
            storage = ir.StorageBox(Y.unwrap_view())
        else:
            assert isinstance(Y, ir.Buffer)
            storage = ir.StorageBox(Y)
        Y_2d = ir.ReinterpretView(data=storage, layout=template_buffer.get_layout())
    return Y_2d, reindexers

