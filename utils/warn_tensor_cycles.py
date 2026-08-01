
def warn_tensor_cycles():
    """
    Install a warning that reports whenever a cycle that is holding CUDA memory is observed.

    The warning produces an .html file that visualizes the cycle,
    and links it to the stack frame that allocated the CUDA tensor.

    Reference cycles are freed by the cycle collector rather than being cleaned up
    when the objects in the cycle first become unreachable. If a cycle points to a tensor,
    the CUDA memory for that tensor will not be freed until garbage collection runs.
    Accumulation of CUDA allocations can lead to out of memory errors (OOMs), as well as
    non-deterministic allocation behavior which is harder to debug.
    """
    logger.info("Watching Python reference cycles for CUDA Tensors.")

    def write_and_log(html) -> None:
        with NamedTemporaryFile('w', suffix='.html') as f:
            f.write(html)
            logger.warning('Reference cycle includes a CUDA Tensor see visualization of cycle %s', f.name)
    return observe_tensor_cycles(write_and_log)

