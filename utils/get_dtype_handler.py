
def get_dtype_handler() -> DtypePropagationOpsHandler:
    from torch._inductor.dtype_propagation import DtypePropagationOpsHandler

    return DtypePropagationOpsHandler()

