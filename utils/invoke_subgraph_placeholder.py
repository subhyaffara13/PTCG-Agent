
def invoke_subgraph_placeholder(func, *args, **kwargs):
    if torch.compiler.is_dynamo_compiling():
        # This is just a placeholder for Dynamo to replace with invoke_subgraph
        raise RuntimeError("invoke_subgraph should not be called directly in Dynamo")

    if torch.compiler.is_compiling():
        # For non-strict export tracing, we still want to go through Dynamo

        def _invoke_subgraph_placeholder_wrapper(func, args):
            return invoke_subgraph_placeholder(func, *args)

        from torch._higher_order_ops.utils import _hop_compile_and_call

        return _hop_compile_and_call(_invoke_subgraph_placeholder_wrapper, (func, args))

    return func(*args, **kwargs)

