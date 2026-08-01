
def is_cuda_dispatch_key(dk: DispatchKey) -> bool:
    return dk in {
        DispatchKey.CUDA,
        DispatchKey.QuantizedCUDA,
        DispatchKey.SparseCUDA,
        DispatchKey.SparseCsrCUDA,
        DispatchKey.NestedTensorCUDA,
        DispatchKey.AutogradCUDA,
    }

