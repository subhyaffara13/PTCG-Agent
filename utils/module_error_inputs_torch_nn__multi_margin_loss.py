
def module_error_inputs_torch_nn_MultiMarginLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    """
    Error inputs for MultiMarginLoss that test the improved error message
    for inconsistent target size.
    Regression test for issue #106251.
    """
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        # Test: target size doesn't match batch size (5 vs 3)
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(),
                forward_input=FunctionInput(
                    make_input((5, 10)),  # input: batch_size=5, num_classes=10
                    torch.tensor([0, 1, 2], device=device, dtype=torch.long),  # target: wrong size (3)
                ),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"target tensor should be 1-D with size equal to.*Expected target size \[5\].*but got \[3\]"
        ),
    ]

