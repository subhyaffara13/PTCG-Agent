
def _register_triton_kernels():
    @_WrappedTritonKernel
    def kernel_impl(*args, **kwargs):
        from torch.sparse._triton_ops import bsr_dense_mm

        # pyrefly: ignore [not-callable]
        return bsr_dense_mm(*args, skip_checks=True, **kwargs)

    @_WrappedTritonKernel
    def addmm_kernel_impl(*args, **kwargs):
        from torch.sparse._triton_ops import bsr_dense_addmm

        return bsr_dense_addmm(*args, skip_checks=True, **kwargs)

    has_triton = importlib.util.find_spec("triton") is not None
    if has_triton:
        torch._TritonLibrary.registerOp(
            "_triton_bsr_dense_mm_out",
            "_triton_bsr_dense_mm_out(Tensor bsr, Tensor dense, *, Tensor(a!) out) -> Tensor(a!)",
            kernel_impl,
            "SparseCsrCUDA",
        )

        torch._TritonLibrary.registerOp(
            "_triton_bsr_dense_addmm_out",
            (
                "_triton_bsr_dense_addmm_out(Tensor input, Tensor bsr, Tensor dense,"
                " *, Scalar beta, Scalar alpha, Tensor(a!) out) -> Tensor(a!)"
            ),
            addmm_kernel_impl,
            "SparseCsrCUDA",
        )

