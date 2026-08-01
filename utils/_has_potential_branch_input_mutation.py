
def _has_potential_branch_input_mutation(gm, inputs, pre_dispatch=False):
    (
        (_, _, _),
        inp_mutation,
    ) = potential_input_alias_or_mutation(gm, inputs, pre_dispatch)

    return len(inp_mutation) > 0

