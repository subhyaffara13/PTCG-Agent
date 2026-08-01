
def tensor_parallel_transformation(
    exported_program: ExportedProgram,
    rank: int,
    world_size: int,
    device_type: str,
    parallel_strategies: dict[str, ParallelStyle],
) -> ExportedProgram:
    """
    The entry point function to perform graph transformations on an exported program
    to transform a single-device graph into a tensor parallel graph.

    .. warning::
        This API is experimental and subject to change.
    """

    gm = exported_program.graph_module
    sig = copy.deepcopy(exported_program.graph_signature)
    state_dict = copy.copy(exported_program.state_dict)

    with gm._set_replace_hook(sig.get_replace_hook()):
        res = _TensorParallelTransformPass(
            rank,
            world_size,
            device_type,
            state_dict,
            exported_program.graph_signature,
            parallel_strategies,
        )(gm)
        if res is None:
            raise AssertionError
        gm = res.graph_module

    return exported_program._update(gm, sig, state_dict=state_dict)

