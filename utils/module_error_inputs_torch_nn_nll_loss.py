
def module_error_inputs_torch_nn_NLLLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    """
    Error inputs for NLLLoss that test weight dtype must match input dtype.
    Regression test for device parity between CPU and CUDA with empty tensors.
    """
    input_t = torch.tensor([], device=device, dtype=dtype).reshape((0, 0))
    weight_dtype = torch.float32 if dtype == torch.float16 else torch.float16
    weight_t = torch.tensor([], device=device, dtype=weight_dtype)
    target_t = torch.tensor([], device=device, dtype=torch.long)

    return [
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(weight=weight_t),
                forward_input=FunctionInput(input_t, target_t),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"expected scalar type \w+ but found \w+"
        ),
    ]

