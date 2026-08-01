
def graph(model, args, verbose=False, use_strict_trace=True):
    """
    Process a PyTorch model and produces a `GraphDef` proto that can be logged to TensorBoard.

    Args:
      model (PyTorch module): The model to be parsed.
      args (tuple): input tensor[s] for the model.
      verbose (bool): Whether to print out verbose information while
        processing.
      use_strict_trace (bool): Whether to pass keyword argument `strict` to
        `torch.jit.trace`. Pass False when you want the tracer to
        record your mutable container types (list, dict)
    """
    with _set_model_to_eval(model):
        try:
            trace = torch.jit.trace(model, args, strict=use_strict_trace)
            graph = trace.graph
            torch._C._jit_pass_inline(graph)
        except RuntimeError as e:
            print(e)
            print("Error occurs, No graph saved")
            raise e

    if verbose:
        print(graph)
    list_of_nodes = parse(graph, trace, args)
    # We are hardcoding that this was run on CPU even though it might have actually
    # run on GPU. Note this is what is shown in TensorBoard and has no bearing
    # on actual execution.
    # TODO: See if we can extract GPU vs CPU information from the PyTorch model
    # and pass it correctly to TensorBoard.
    #
    # Definition of StepStats and DeviceStepStats can be found at
    # https://github.com/tensorflow/tensorboard/blob/master/tensorboard/plugins/graph/tf_graph_common/proto.ts
    # and
    # https://github.com/tensorflow/tensorboard/blob/master/tensorboard/compat/proto/step_stats.proto
    stepstats = RunMetadata(
        step_stats=StepStats(dev_stats=[DeviceStepStats(device="/device:CPU:0")])
    )
    return GraphDef(node=list_of_nodes, versions=VersionDef(producer=22)), stepstats

