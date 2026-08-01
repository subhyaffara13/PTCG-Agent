
def assign_epilogue_copy_streams(gm: torch.fx.GraphModule) -> None:
    for epi_copy in gm.graph.find_nodes(op="call_function", target=aten.copy_.default):
        arg_stream = get_stream(epi_copy.args[1])
        copy_stream = get_stream(epi_copy)
        if arg_stream != copy_stream:
            set_stream(epi_copy, get_stream_or_current_stream(epi_copy.args[1]))

