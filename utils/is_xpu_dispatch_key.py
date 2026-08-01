
def is_xpu_dispatch_key(dk: DispatchKey) -> bool:
    return dk in {
        DispatchKey.XPU,
        DispatchKey.QuantizedXPU,
        DispatchKey.SparseXPU,
        DispatchKey.SparseCsrXPU,
        DispatchKey.NestedTensorXPU,
        DispatchKey.AutogradXPU,
    }

