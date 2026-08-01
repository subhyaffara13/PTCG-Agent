
def checkLSTMBackwardSizes(grad_hy, grad_cy, cx, cy, workspace):
    defined_grad = grad_hy if grad_hy is not None else grad_cy
    torch._check(defined_grad.dim() == 2, lambda: "")
    exp_size = defined_grad.size()
    if grad_hy is not None:
        torch._check(grad_hy.size() == exp_size, lambda: "")
    if grad_cy is not None:
        torch._check(grad_cy.size() == exp_size, lambda: "")
    torch._check(cx.size() == exp_size, lambda: "")
    torch._check(cy.size() == exp_size, lambda: "")
    torch._check(workspace.dim() == 2, lambda: "")
    torch._check(workspace.numel() == exp_size[0] * exp_size[1] * 4, lambda: "")

