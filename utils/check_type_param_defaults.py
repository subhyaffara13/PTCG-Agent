
def check_type_param_defaults(
    state: State, type_params: list[TypeParam], line: int, column: int
) -> None:
    if any(p.default is not None for p in type_params):
        state.check_min_version("Type parameter defaults", (3, 13), line, column)

