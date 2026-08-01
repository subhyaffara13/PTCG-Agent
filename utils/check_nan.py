
def check_nan(buffer: IndentedBuffer, var: CSEVariableType) -> None:
    backend = get_current_backend()
    if backend == "triton":
        msg = "NaN or Inf found"
        buffer.writeline(
            f"tl.device_assert(({var} == {var}) & ({var} != float('inf')) & ({var} != float('-inf')), '{msg}')"
        )

