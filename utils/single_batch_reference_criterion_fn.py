
def single_batch_reference_criterion_fn(*args):
    """Reference function for criterion supporting no batch dimensions.

    The criterion is passed the input and target in batched form with a single item.
    The output is squeezed to compare with the no-batch input.
    """
    criterion = args[-1]

    def unsqueeze_inp(inp):
        if isinstance(inp, (list, tuple)):
            return [t.unsqueeze(0) for t in inp]
        return inp.unsqueeze(0)

    def flatten(xs):
        result = []
        if isinstance(xs, (list, tuple)):
            for x in xs:
                result.extend(flatten(x))
        else:
            result.append(xs)
        return result

    single_batch_input_args = flatten([unsqueeze_inp(input) for input in args[:-1]])

    output = criterion(*single_batch_input_args)
    reduction = get_reduction(criterion)

    if reduction == 'none':
        return output.squeeze(0)
    # reduction is 'sum' or 'mean' which results in a scalar
    return output

