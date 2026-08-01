
def construct_register_size(register_size_from_yaml: int) -> str:
    if not isinstance(register_size_from_yaml, int):
        raise ValueError(
            f"Input register size is {register_size_from_yaml} and"
            "it's type is {type(register_size_from_yaml)}. An int type is expected."
        )
    return str(register_size_from_yaml)

