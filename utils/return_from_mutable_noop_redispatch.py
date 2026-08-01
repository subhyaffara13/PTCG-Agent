
def return_from_mutable_noop_redispatch(
    f: NativeFunction, inner_return_var: str
) -> str:
    aliased, non_aliased = get_mutable_redispatch_return_names(f, inner_return_var)
    # Just get all of the return names, and immediately return them
    return return_str(f.func.returns, aliased + non_aliased)

