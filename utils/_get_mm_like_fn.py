
def _get_mm_like_fn(snode: BaseSchedulerNode) -> Callable[[Any], Any] | None:
    if not isinstance(snode, ExternKernelSchedulerNode):
        return None
    mms_fns = {
        "extern_kernels.mm": torch.ops.aten.mm,
        "extern_kernels.bmm": torch.ops.aten.bmm,
        "extern_kernels.addmm": torch.ops.aten.addmm,
    }
    python_kernel_name = getattr(snode.node, "python_kernel_name", "")
    if python_kernel_name not in mms_fns:
        return None
    if not isinstance(snode.node, ir.ExternKernel):
        return None
    return mms_fns[python_kernel_name]

