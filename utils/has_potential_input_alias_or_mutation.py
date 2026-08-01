
def has_potential_input_alias_or_mutation(gm, inputs, pre_dispatch=False):
    (
        (
            inp_inp_alias_map,
            inp_out_alias_map,
            out_out_alias_map,
        ),
        inp_mutation,
    ) = potential_input_alias_or_mutation(gm, inputs, pre_dispatch)
    return (
        any(
            (
                len(inp_inp_alias_map) > 0,
                len(inp_out_alias_map) > 0,
                len(out_out_alias_map) > 0,
            )
        ),
        len(inp_mutation) > 0,
    )

