
def potential_input_alias_or_mutation(gm, inputs, pre_dispatch=False):
    try:
        gm = _maybe_fake_tracing(gm, inputs, pre_dispatch)
    except UnsupportedAliasMutationException:
        # this can happen when nested cond_op is
        # functionalized
        return True
    except Exception as e:
        raise e

    example_inputs = [
        ph.meta.get("val", None) for ph in gm.graph.find_nodes(op="placeholder")
    ]
    (
        inp_inp_alias_map,
        inp_out_alias_map,
        out_out_alias_map,
        inp_mutation,
    ) = check_input_alias_and_mutation(gm, example_inputs)
    return (inp_inp_alias_map, inp_out_alias_map, out_out_alias_map), inp_mutation

