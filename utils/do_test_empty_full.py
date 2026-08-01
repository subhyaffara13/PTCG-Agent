
def do_test_empty_full(self, dtypes, layout, device):
    shape = torch.Size([2, 3])

    def check_value(tensor, dtype, layout, device, value, requires_grad):
        self.assertEqual(shape, tensor.shape)
        self.assertIs(dtype, tensor.dtype)
        self.assertIs(layout, tensor.layout)
        self.assertEqual(tensor.requires_grad, requires_grad)
        if tensor.is_cuda and device is not None:
            self.assertEqual(device, tensor.device)
        if value is not None:
            fill = tensor.new(shape).fill_(value)
            self.assertEqual(tensor, fill)

    def get_int64_dtype(dtype):
        module = '.'.join(str(dtype).split('.')[1:-1])
        if not module:
            return torch.int64
        return operator.attrgetter(module)(torch).int64

    default_dtype = torch.get_default_dtype()
    check_value(torch.empty(shape), default_dtype, torch.strided, -1, None, False)
    check_value(torch.full(shape, -5.), default_dtype, torch.strided, -1, None, False)
    for dtype in dtypes:
        for rg in {dtype.is_floating_point, False}:
            int64_dtype = get_int64_dtype(dtype)
            v = torch.empty(shape, dtype=dtype, device=device, layout=layout, requires_grad=rg)
            check_value(v, dtype, layout, device, None, rg)
            out = v.new()
            check_value(torch.empty(shape, out=out, device=device, layout=layout, requires_grad=rg),
                        dtype, layout, device, None, rg)
            check_value(v.new_empty(shape), dtype, layout, device, None, False)
            check_value(v.new_empty(shape, dtype=int64_dtype, device=device, requires_grad=False),
                        int64_dtype, layout, device, None, False)
            check_value(torch.empty_like(v), dtype, layout, device, None, False)
            check_value(torch.empty_like(v, dtype=int64_dtype, layout=layout, device=device, requires_grad=False),
                        int64_dtype, layout, device, None, False)

            if dtype is not torch.float16 and layout != torch.sparse_coo:
                fv = 3
                v = torch.full(shape, fv, dtype=dtype, layout=layout, device=device, requires_grad=rg)
                check_value(v, dtype, layout, device, fv, rg)
                check_value(v.new_full(shape, fv + 1), dtype, layout, device, fv + 1, False)
                out = v.new()
                check_value(torch.full(shape, fv + 2, out=out, device=device, layout=layout, requires_grad=rg),
                            dtype, layout, device, fv + 2, rg)
                check_value(v.new_full(shape, fv + 3, dtype=int64_dtype, device=device, requires_grad=False),
                            int64_dtype, layout, device, fv + 3, False)
                check_value(torch.full_like(v, fv + 4), dtype, layout, device, fv + 4, False)
                check_value(torch.full_like(v, fv + 5,
                                            dtype=int64_dtype, layout=layout, device=device, requires_grad=False),
                            int64_dtype, layout, device, fv + 5, False)

