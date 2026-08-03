from typing import Any

def log_runtime_and_tensor_meta(node_runtimes: Sequence[tuple[Any, float]]) -> None:
    """Log per-op runtime estimates and output tensor metadata for TLParse."""

    try:
        to_optimization_hints = V.graph.sizevars.optimization_hints

        def to_list(x: Sequence[Any] | None) -> list[Any]:
            return list(to_optimization_hints(x)) if x is not None else []

        def dtype_to_str(dtype: Any) -> str | None:
            if dtype is None:
                return None
            s = str(dtype)
            s = s.removeprefix("torch.")
            return s

        ops: list[dict[str, Any]] = []
        for s, runtime_ns in node_runtimes:
            name = getattr(s.node, "python_kernel_name", s.get_name())
            op_type = "collective" if utils.is_collective(s.node) else "compute"

            # Build outputs metadata if available
            outputs: list[dict[str, Any]] = []
            try:
                for buf in s.get_outputs():
                    irnode = buf.node
                    shape = irnode.maybe_get_size()
                    stride = (
                        irnode.get_stride()
                        if isinstance(irnode.layout, ir.Layout)
                        else None
                    )
                    dtype = irnode.maybe_get_dtype()
                    outputs.append(
                        {
                            "shape": to_list(shape),
                            "stride": to_list(stride),
                            "dtype": dtype_to_str(dtype),
                        }
                    )
            except Exception:
                pass

            ops.append(
                {
                    "name": name,
                    "type": op_type,
                    "estimated_runtime_ns": runtime_ns,
                    "outputs": outputs,
                }
            )

        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "inductor_runtime_and_tensor_meta",
                "encoding": "json",
            },
            payload_fn=lambda: {"ops": ops},
        )
    except Exception:
        log.debug("Failed to log inductor_runtime_and_tensor_meta", exc_info=True)

