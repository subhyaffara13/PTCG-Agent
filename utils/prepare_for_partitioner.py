import copy
import itertools

def prepare_for_partitioner(
    mod: torch.fx.GraphModule, num_primals: int, num_fw_outputs: int
) -> torch.fx.GraphModule:
    # min-cut partitioner requires the placeholders to have primals and
    # tangents string in the node.name. The signature of the joint graph is
    # (*primals, *tangents)

    # We also have to update the output signature which is right now
    # (*grads, *fw_outs) and we have to change to (*fw_outs, *grads) for the
    # partitioner to work.
    new_graph = torch.fx.Graph()
    env = {}

    primals_counter = itertools.count(0)
    tangents_counter = itertools.count(0)

    for idx, node in enumerate(mod.graph.nodes):
        if node.op == "placeholder":
            if idx < num_primals:
                env[node] = new_graph.placeholder(f"primals_{next(primals_counter)}")
            else:
                env[node] = new_graph.placeholder(f"tangents_{next(tangents_counter)}")
            env[node].meta = copy.copy(node.meta)
        elif node.op == "output":
            # Reverse the (*grads, *fw_outs) to (*fw_outs, *grads)
            # The reason for having the reversed signature in the first
            # place is to simplify step 3.
            old_outputs = node.args[0]
            new_outputs = (
                *old_outputs[-num_fw_outputs:],
                *old_outputs[:-num_fw_outputs],
            )
            new_outputs = [env[n] if n else None for n in new_outputs]
            new_graph.output(tuple(new_outputs))
        else:
            env[node] = new_graph.node_copy(node, lambda n: env[n])
            env[node].meta = copy.copy(node.meta)

    new_graph.lint()

    out = torch.fx.GraphModule(mod, new_graph)
    return out

