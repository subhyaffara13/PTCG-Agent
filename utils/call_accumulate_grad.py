
def call_accumulate_grad(
    variable: torch.Tensor, grad: torch.Tensor, has_post_hooks: bool
) -> None:
    updated_grad = torch._dynamo.compiled_autograd.ops.AccumulateGrad(  # type: ignore[attr-defined]
        [grad], variable, variable.grad, has_post_hooks
    )
    variable.grad = updated_grad[0]

