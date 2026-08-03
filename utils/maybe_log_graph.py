from typing import Callable

def maybe_log_graph(
    gm: torch.fx.GraphModule,
    graph_name: str,
    aot_config: AOTConfig,
    structured_log_prefix_fn: Callable[[], str],
    out_structured_logs: list[str] | None = None,
) -> None:
    if not aot_config.enable_log:
        return
    aot_graphs_log.debug(
        "%s",
        lazy_format_graph_code(
            f"{graph_name}",
            gm,
            aot_config.aot_id,
            include_stride=True,
            include_device=True,
            colored=True,
        ),
    )

    def gm_str_fn() -> str:
        return gm.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            expanded_def=True,
        )

    if out_structured_logs is not None:
        out_structured_logs.append(f"{structured_log_prefix_fn()}:{gm_str_fn()}")
    else:
        trace_structured(
            f"{structured_log_prefix_fn()}",
            payload_fn=lambda: gm_str_fn(),
        )

