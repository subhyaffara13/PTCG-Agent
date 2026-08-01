
def template_fusion_with_epilogues_supported(
    template: BaseSchedulerNode, epilogues: list[BaseSchedulerNode]
) -> tuple[bool, bool]:
    def _get_indexes_of_template_buf_read(
        epilogue_node: ir.Operation, template_buf_names: list[str]
    ) -> list[sympy.Expr]:
        return [
            read.index
            for read in epilogue_node.get_reads()
            if read.name in template_buf_names
        ]

    def _check_supported_and_same_indexes(
        index_of_template_buf_read: Sequence[sympy.Expr],
        epilogue_writes: OrderedSet[Dep],
    ) -> tuple[bool, bool]:
        num_indexes = len(OrderedSet(index_of_template_buf_read))

        if num_indexes > 1:
            same_index = False
            supported = False  # Different read indexes not supported
        elif num_indexes == 0:
            same_index = True
            supported = True  # No reads, automatically supported
        elif num_indexes == 1:
            iotbr = index_of_template_buf_read[0]
            same_index = all(write.index == iotbr for write in epilogue_writes)
            # TODO: Add support of fusion when the read of template buffer and the write of epilogue output
            # in the epilogue node don't have the same index and change supported to True
            supported = same_index
        else:
            raise AssertionError("Should not reach here")

        return supported, same_index

    def _template_fusion_supported(
        template_outputs: Sequence[SchedulerBuffer], epilogue_nodes: list[ir.Operation]
    ) -> tuple[bool, bool]:
        template_buf_names = [x.get_name() for x in template_outputs]
        indexes_of_template_buf_reads = [
            _get_indexes_of_template_buf_read(epilogue_node, template_buf_names)
            for epilogue_node in epilogue_nodes
        ]
        epilogue_nodes_writes = [
            epilogue_node.get_read_writes().writes for epilogue_node in epilogue_nodes
        ]

        results = [
            _check_supported_and_same_indexes(reads, writes)
            for reads, writes in zip(
                indexes_of_template_buf_reads, epilogue_nodes_writes
            )
        ]
        supported, same_indexes = zip(*results)
        return all(supported), all(same_indexes)

    assert template.is_template()
    template_outputs = template.get_outputs()

    epilogue_nodes = [
        n.node
        for epilogue in epilogues
        for n in epilogue.get_nodes()
        if n.node is not None
    ]
    return _template_fusion_supported(template_outputs, epilogue_nodes)

