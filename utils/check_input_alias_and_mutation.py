
def check_input_alias_and_mutation(
    gm: torch.fx.GraphModule,
    fake_args: list[FakeTensor],
) -> tuple[dict[int, int], dict[int, int], dict[int, int], list[int]]:
    (
        inp_inp_alias_map,
        inp_out_alias_map,
        out_out_alias_map,
        mutated_inputs,
    ) = check_input_alias_and_mutation_return_outputs(gm)[:-1]
    # pyrefly: ignore [bad-return]
    return inp_inp_alias_map, inp_out_alias_map, out_out_alias_map, mutated_inputs

