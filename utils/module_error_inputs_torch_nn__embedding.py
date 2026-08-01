
def module_error_inputs_torch_nn_Embedding(module_info, device, dtype, requires_grad, training, **kwargs):
    """
    Error inputs for Embedding that test error messages for invalid inputs.
    """
    samples = []

    # Out of range indices: index exceeds num_embeddings
    # Only test on CPU - CUDA triggers kernel assertion instead of Python exception
    if torch.device(device).type == 'cpu':
        samples.append(
            ErrorModuleInput(
                ModuleInput(
                    constructor_input=FunctionInput(num_embeddings=10, embedding_dim=3),
                    forward_input=FunctionInput(torch.tensor([0, 5, 15], device=device, dtype=torch.long)),
                ),
                error_on=ModuleErrorEnum.FORWARD_ERROR,
                error_type=IndexError,
                error_regex=r"index out of range in self"
            )
        )

    # Float indices: wrong dtype for indices (works on all devices)
    samples.append(
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(num_embeddings=10, embedding_dim=3),
                forward_input=FunctionInput(torch.tensor([1.5, 2.5], device=device, dtype=torch.float32)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"Expected tensor for argument.*indices.*to have.*scalar type.*Long.*Int"
        )
    )

    # Negative num_embeddings (construction error, device-independent)
    samples.append(
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(num_embeddings=-1, embedding_dim=3),
                forward_input=FunctionInput(),
            ),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=RuntimeError,
            error_regex=r"Trying to create tensor with negative dimension"
        )
    )

    return samples

