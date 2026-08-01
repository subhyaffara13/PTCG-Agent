
def module_error_inputs_torch_nn_CrossEntropyLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    return [
        # Non-floating-point target with same shape as input (soft-target path)
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    torch.zeros((2, 3), device=device, dtype=torch.long),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="Expected floating point type for target with class probabilities",
        ),
        # Non-long target with different shape from input (class-index path)
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    make_input((2,)),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="expected target dtype to be Long or Byte",
        ),
        # Batch size mismatch
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    torch.tensor([0, 1, 2], device=device, dtype=torch.long),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex="Expected input batch_size .* to match target batch_size",
        ),
        # Weight wrong shape
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(weight=make_weight((2,))),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    torch.tensor([0, 1], device=device, dtype=torch.long),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="weight tensor should be defined either for all .* classes or no classes",
        ),
        # Prob target with ignore_index
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(ignore_index=1),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    make_input((2, 3)).softmax(dim=1).detach(),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="ignore_index is not supported for floating point target",
        ),
        # label_smoothing out of range
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(label_smoothing=1.5),
                forward_input=FunctionInput(
                    make_input((2, 3)),
                    torch.tensor([0, 1], device=device, dtype=torch.long),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="label_smoothing must be between 0.0 and 1.0",
        ),
        # Target spatial size mismatch (3D input)
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(),
                forward_input=FunctionInput(
                    make_input((2, 3, 5)),
                    torch.zeros((2, 4), device=device, dtype=torch.long),
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="Expected target size",
        ),
    ]

