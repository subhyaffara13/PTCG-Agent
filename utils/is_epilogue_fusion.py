
def is_epilogue_fusion(node1: BaseSchedulerNode, node2: BaseSchedulerNode):
    return (
        node1.is_template()
        and not node2.is_template()
        and _is_epilogue_fusion_enabled(node1)
    )

