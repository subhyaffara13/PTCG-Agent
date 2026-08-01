
def unwrap_optional_tensor(name: str, cur_level_var: str) -> list[str]:
    result = f"""\
    std::optional<Tensor> {name}_value;
    std::optional<int64_t> {name}_bdim;
    if ({name}) {{
        std::tie({name}_value, {name}_bdim) = unwrapTensorAtLevel({name}.value(), {cur_level_var});
    }}"""
    return textwrap.dedent(result).split("\n")

