
def returns_multi_tensor(fn: NativeFunction) -> bool:
    returns = fn.func.returns
    if len(returns) != 1:
        raise AssertionError(f"Expected 1 return, got {len(returns)}")
    returns_list_like = returns[0].type.is_list_like() is not None
    returns_tensor_like = returns[0].type.is_tensor_like()
    return returns_list_like and returns_tensor_like

