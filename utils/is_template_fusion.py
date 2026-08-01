
def is_template_fusion(node1: BaseSchedulerNode, node2: BaseSchedulerNode):
    return is_epilogue_fusion(node1, node2) or is_prologue_fusion(node1, node2)

