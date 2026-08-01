
def _test_bfloat16_ops(test_case, op, device, inp_dims=(), prec=1e-2, scale_factor=None):
    # fp32 compute
    input1 = torch.randn(inp_dims, dtype=torch.float32, device=device, requires_grad=True)
    if scale_factor is not None:
        input1 = (torch.rand(inp_dims, dtype=torch.bfloat16, device=device) * scale_factor).float().requires_grad_()
    out1 = op(input1)
    grad_input1 = torch.randn_like(out1, device=device)
    out1.backward(grad_input1)

    # bfloat16 compute
    op_bfp16 = op.bfloat16()
    input2 = input1.detach().bfloat16().requires_grad_()
    grad_input2 = grad_input1.bfloat16()
    out2 = op_bfp16(input2)
    out2.backward(grad_input2)

    test_case.assertEqual(out1, out2, atol=prec, rtol=prec, exact_dtype=False)
    test_case.assertEqual(input1.grad.data, input2.grad.data, atol=prec, rtol=prec, exact_dtype=False)

