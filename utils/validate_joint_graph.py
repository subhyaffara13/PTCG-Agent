
def validate_joint_graph(joint_graph: torch.fx.Graph):
    """We do some pre lowering graph checks in order to raise nicer error messages"""
    for node in joint_graph.nodes:
        if (
            node.op == "call_function"
            and node.target is torch.ops.flex_lib.zeros_and_scatter.default
        ):
            for user in node.users:
                if user.op != "output":
                    raise NotImplementedError(
                        "Using multiple indexing operations on the same tensor that requires gradients "
                        "in a score_mod function is not currently supported. "
                        "This typically happens when indexing the same tensor multiple times, like:\n\n"
                        "    def score_mod(score, b, h, q_idx, kv_idx):\n"
                        "        return score + bias[q_idx] + bias[kv_idx]  # bias used twice!\n\n"
                        "A valid workaround is to clone() the tensors that will be indexed multiple times. For example:\n\n"
                        "    bias1 = bias.clone()\n"
                        "    def score_mod(score, b, h, q_idx, kv_idx):\n"
                        "        return score + bias[q_idx] + bias1[kv_idx]\n\n"
                        "Note that this solution will use additional memory."
                    )
    return

