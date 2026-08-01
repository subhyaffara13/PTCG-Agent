
def debug_triton_code(node: BaseSchedulerNode) -> list[str]:
    lines = []
    multi_template = node.get_template_node()
    assert multi_template is None or isinstance(multi_template, ir.MultiTemplateBuffer)
    if multi_template and multi_template.make_kernel_render is None:
        lines.append(f"{node.get_name()} Unfinalized multi template buffer")
    else:
        from torch._inductor.codegen.cuda_combined_scheduling import (
            CUDACombinedScheduling,
        )
        from torch._inductor.codegen.xpu.xpu_combined_scheduling import (
            XPUCombinedScheduling,
        )

        device = node.get_device()
        assert device is not None
        backend = node.scheduler.get_backend(device)
        assert isinstance(
            backend, (SIMDScheduling, CUDACombinedScheduling, XPUCombinedScheduling)
        ), (
            f"Scheduling backend should be SIMD or CUDACombined when generating debug Triton strings, got: {type(backend)}"
        )

        with V.graph.set_current_device(device):
            # Don't increment kernel count when generating debug string.
            # This will confuse some unit tests that check the number of
            # generated kernels.
            old_generated_kernel_count = metrics.generated_kernel_count
            triton_code = backend.generate_kernel_code_from_nodes(
                node.get_nodes()
            ).strip()
            metrics.generated_kernel_count = old_generated_kernel_count

        lines.append(f"{node.get_name()} Triton code:")
        lines.append(textwrap.indent(triton_code, "    "))
    return lines

