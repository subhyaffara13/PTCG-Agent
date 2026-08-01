
def construct_instruction(instruction_list_from_yaml: list[Any]) -> str:
    instruction_list_part = [
        ONE_INSTRUCTION.substitute(
            operator_name=instruction[0],
            X=instruction[1],
            N=instruction[2],
        )
        for instruction in instruction_list_from_yaml
    ]
    return INSTRUCTION_LIST.substitute(
        instruction_list="".join(instruction_list_part).lstrip("\n")
    )

