
def sample_inputs_full(op, device, dtype, requires_grad, **kwargs):
    def get_val(dtype):
        return make_tensor([], dtype=dtype, device="cpu").item()

    sizes = (
        (M,),
        (S, S),
    )
    fill_values = [get_val(dtype), get_val(torch.int)]

    for size, fill_value in product(sizes, fill_values):
        yield SampleInput(size, fill_value, dtype=dtype, device=device)

