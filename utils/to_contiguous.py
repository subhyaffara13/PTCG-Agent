
def to_contiguous(input_tensors):
    if isinstance(input_tensors, list):
        out = []
        for tensor in input_tensors:
            if not tensor.is_contiguous():
                tensor = tensor.contiguous()
            out.append(tensor)
        return out
    else:
        if not input_tensors.is_contiguous():
            input_tensors = input_tensors.contiguous()
        return input_tensors

