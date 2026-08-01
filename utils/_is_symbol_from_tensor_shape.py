
def _is_symbol_from_tensor_shape(symbol: sympy.Symbol, shape_env: Any) -> bool:
    """Check if a symbol originates from a tensor size/stride (TensorPropertySource)."""
    from torch._dynamo.source import TensorPropertySource

    sources = shape_env.var_to_sources.get(symbol, [])
    return any(isinstance(s, TensorPropertySource) for s in sources)

