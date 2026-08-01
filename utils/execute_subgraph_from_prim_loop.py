
def execute_subgraph_from_prim_loop(
    subgraph, iter_idx, len_loop_local_arguments, *args, **kwargs
):
    """
    subgraph: GraphModule from sub-block.
    iter_idx: The index of interaction.
    len_loop_local_arguments: The number of loop local arguments in args.
    """

    # Loop local variables. TS graph create those as inputs because their values
    # are updated inside the loop.
    loop_local_args = args[:len_loop_local_arguments]
    # Global variables that are not passed in as inputs to the loop sub-blocks
    # but are directly used. Most of time, their values are not updated, but
    # the only exception is when there are some operations that perform inplace
    # updates.
    global_args = args[len_loop_local_arguments:]
    return subgraph(*global_args, iter_idx, *loop_local_args, **kwargs)

