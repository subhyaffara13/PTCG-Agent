
def error_inputs_complex(op_info, device, is_ref=False, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float32, device=device)
    other_dtype = torch.float16 if device.startswith("mps") else torch.float64
    other_dtype_name = "Half" if device.startswith("mps") else "Double"

    if is_ref:
        error_float = "Expected both inputs to be Half, Float or Double tensors but got torch.float32 and torch.int32"
        error_dtype = "Expected object of scalar type torch.float32 but got scalar type torch.float64 for second argument"
        error_out = "Expected out tensor to have dtype torch.complex128 but got torch.complex64 instead"
    else:
        error_float = "Expected both inputs to be Half, Float or Double tensors but got Float and Int"
        error_dtype = f"Expected object of scalar type Float but got scalar type {other_dtype_name} for second argument"
        error_out = f"Expected object of scalar type Complex{other_dtype_name} but got scalar type ComplexFloat for argument 'out'"

    yield ErrorInput(SampleInput(make_arg(M, S), make_arg(M, S, dtype=torch.int)),
                     error_type=RuntimeError, error_regex=error_float)

    yield ErrorInput(SampleInput(make_arg(M, S), make_arg(M, S, dtype=other_dtype)),
                     error_type=RuntimeError, error_regex=error_dtype)

    yield ErrorInput(SampleInput(make_arg(M, S, dtype=other_dtype), make_arg(M, S, dtype=other_dtype),
                                 out=make_arg(M, S, dtype=torch.complex64)),
                     error_type=RuntimeError, error_regex=error_out)

