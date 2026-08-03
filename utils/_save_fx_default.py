import copy
import logging
import os
from typing import Any

def _save_fx_default(
    current_name: str,
    folder_name: str,
    dump_example_input: bool,
    gm: torch.fx.GraphModule,
    example_inputs: list[torch.Tensor],
) -> nn.Module:
    """
    The forward, backward, and joint computation graph will be stored in
    {folder_name}/{current_name}/{current_name}_forward_{graph_index},
    {folder_name}/{current_name}/{current_name}_backward_{graph_index}, and
    {folder_name}/{current_name}/{current_name}_joint_{graph_index} respectively.
    The input shape of the graphs will be stored in the .input files.
    These files can be loaded with pickle,
    and is a list of format (type, shape, stride, dtype, device).
    In the case of type = int or float, it is just (type,).
    For joint graph input, it is a nested list [[],[]]
    where the two inner lists have the same format.
    If dump_example_input is True, example_inputs will be stored in .pt file.
    Since each function might produce multiple graphs,
    the graph_index is used to distinguish difference graphs
    """
    from functorch.compile import aot_module_simplified

    def get_input_meta(args: Any) -> list[Any]:
        input_meta = []
        if len(args) > 0 and isinstance(args[0], tuple):  # joint input
            input_meta += get_input_meta(args[0])
            input_meta += get_input_meta(args[1])
            return input_meta
        for arg in args:
            if type(arg) is int or type(arg) is float:
                input_meta.append((type(arg),))
            else:
                input_meta.append(
                    (type(arg), arg.shape, arg.stride(), arg.dtype, arg.device)
                )
        return input_meta

    def graph_saver_helper(
        gm_to_save: fx.GraphModule, args: Any, type_name: str
    ) -> None:
        global graph_index
        if len(gm_to_save.graph.nodes) == 0:
            log.log(
                logging.WARNING,
                "No nodes in graph {%s}_{%s}_{%s}.",
                current_name,
                type_name,
                graph_index,
            )
            return

        gm = copy.deepcopy(gm_to_save)
        gm.graph.set_codegen(torch.fx.graph.CodeGen())  # remove codegen
        gm.recompile()

        input_meta = get_input_meta(args)

        os.makedirs(f"{folder_name}/{current_name}", exist_ok=True)
        gm.to_folder(
            f"{folder_name}/{current_name}/{current_name}_{type_name}_{graph_index}"
        )
        with open(
            f"{folder_name}/{current_name}/{current_name}_{type_name}_{graph_index}/{current_name}_{type_name}_{graph_index}.input",
            "wb",
        ) as f:
            pickle.dump(input_meta, f)
        if dump_example_input:
            torch.save(
                args,
                f"{folder_name}/{current_name}/{current_name}_{type_name}_{graph_index}/{current_name}_{type_name}_{graph_index}.pt",  # noqa: B950
            )  # noqa: E501

    def graph_saver_forward(
        gm: fx.GraphModule, example_inputs: list[torch.Tensor]
    ) -> fx.GraphModule:
        graph_saver_helper(gm, example_inputs, "forward")
        return gm

    def graph_saver_backward(
        gm: fx.GraphModule, example_inputs: list[torch.Tensor]
    ) -> fx.GraphModule:
        graph_saver_helper(gm, example_inputs, "backward")
        global graph_index
        graph_index += 1
        return gm

    def graph_saver_joint(
        gm: fx.GraphModule, joint_args: list[torch.Tensor]
    ) -> tuple[fx.GraphModule, fx.GraphModule]:
        graph_saver_helper(gm, joint_args, "joint")
        return default_partition(gm, joint_args)  # pyrefly: ignore[missing-argument]

    # pyrefly: ignore[bad-return]
    return aot_module_simplified(
        gm,
        example_inputs,
        fw_compiler=graph_saver_forward,  # pyrefly: ignore[bad-argument-type]
        bw_compiler=graph_saver_backward,  # pyrefly: ignore[bad-argument-type]
        partition_fn=graph_saver_joint,
        decompositions=default_decompositions,  # pyrefly: ignore[bad-argument-type]
    )

