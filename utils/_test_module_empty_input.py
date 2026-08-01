
def _test_module_empty_input(test_case, module, inp, check_size=True, inference=False):
    if not inference:
        inp.requires_grad_(True)
    out = module(inp)
    if not inference:
        gO = torch.rand_like(out)
        out.backward(gO)
    if check_size:
        test_case.assertEqual(out.size(), inp.size())
    if not inference:
        for p in module.parameters():
            if p.requires_grad:
                test_case.assertEqual(p.grad, torch.zeros_like(p.grad))
        test_case.assertEqual(inp.grad, torch.zeros_like(inp))

