
def unwrap_tensor(name: str, cur_level_var: str) -> list[str]:
    result = f"""\
    auto [{name}_value, {name}_bdim] = unwrapTensorAtLevel({name}, {cur_level_var});"""
    return textwrap.dedent(result).split("\n")

