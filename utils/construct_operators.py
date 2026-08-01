
def construct_operators(operator_list_from_yaml: list[Any]) -> str:
    operator_list_part = [
        ONE_OPERATOTR_STRING.substitute(
            operator_name=operator[0],
            overload_name=operator[1],
            num_of_args=operator[2],
        )
        for operator in operator_list_from_yaml
    ]
    return OPERATOR_STRING_LIST.substitute(
        operator_string_list="".join(operator_list_part).lstrip("\n")
    )

