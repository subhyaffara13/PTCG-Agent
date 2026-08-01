
def is_prologue_fusion(node1: BaseSchedulerNode, node2: BaseSchedulerNode):
    return (
        node2.is_template()
        and not node1.is_template()
        and _is_prologue_fusion_enabled(node2)
    )

