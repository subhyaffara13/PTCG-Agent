
def template_fusion_pw_node(node1: BaseSchedulerNode, node2: BaseSchedulerNode):
    return node2 if is_epilogue_fusion(node1, node2) else node1

