
def batchwise_reference_select(op, sample):
    # reference for select() over dim=0
    return sample.input.unbind()[sample.kwargs["index"]]

