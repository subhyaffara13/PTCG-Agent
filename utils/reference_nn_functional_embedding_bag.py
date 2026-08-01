
def reference_nn_functional_embedding_bag(op, sample):
    # run reference on a single bag at a time
    new_kwargs = dict(sample.kwargs)
    new_kwargs.update(
        {"offsets": torch.tensor([0], dtype=torch.int64, device=sample.input.device)}
    )
    # flip input / weight back to what unbind_reference() expects
    sample = SampleInput(sample.args[0], args=(sample.input,), kwargs=new_kwargs)
    old_op = op.op
    op.op = torch.nn.functional.embedding_bag
    output = unbind_reference(op, sample, wrap_output_as_njt=False)
    op.op = old_op
    # concat bag outputs to get final output
    return torch.cat(output, dim=0)

