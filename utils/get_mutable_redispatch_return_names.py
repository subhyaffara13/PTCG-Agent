
def get_mutable_redispatch_return_names(
    f: NativeFunction, inner_return_var: str
) -> tuple[list[str], list[str]]:
    aliased_returns = []
    non_aliased_returns = []
    for i, name in enumerate(f.func.aliased_return_names()):
        if name is not None:
            aliased_returns.append(name)
        else:
            non_aliased_returns.append(
                inner_return_var
                if len(f.func.returns) == 1
                else f"std::get<{i}>({inner_return_var})"
            )
    return aliased_returns, non_aliased_returns

