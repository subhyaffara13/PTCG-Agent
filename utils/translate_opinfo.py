
def translate_opinfo(op):
    new_op = copy(op)
    new_op.supports_njt = True
    # add some extra info for use in generating tests on the right subset of ops
    new_op._extra_op_data = extra_op_data.get(op.full_name, ExtraOpData())

    if op.full_name in njt_sample_inputs:
        new_op.sample_inputs_func = njt_sample_inputs[op.full_name]
        new_op.ref = njt_references.get(op.full_name, unbind_reference)
    elif isinstance(op, UnaryUfuncInfo):
        new_op.sample_inputs_func = partial(
            sample_inputs_elementwise_njt_unary, op_kwargs=None
        )
        new_op.ref = unbind_reference
    elif isinstance(op, BinaryUfuncInfo):
        new_op.sample_inputs_func = partial(
            sample_inputs_elementwise_njt_binary, op_kwargs=None
        )
        new_op.ref = unbind_reference
    elif isinstance(op, ReductionOpInfo):
        new_op.sample_inputs_func = partial(sample_inputs_njt_reduction, op_kwargs=None)
        new_op.ref = reduction_reference
    # TODO: Translate the rest of the OpInfos
    else:
        new_op.sample_inputs_func = unsupported_sample_inputs_func(op.full_name)
        new_op.ref = unsupported_reference(op.full_name)
        new_op.supports_njt = False

    return new_op

