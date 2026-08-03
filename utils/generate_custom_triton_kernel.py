from typing import Any

def generate_custom_triton_kernel(kernel: Any) -> str:
    res = ""
    if isinstance(kernel, Autotuner):
        # pyrefly: ignore [missing-attribute]
        if isinstance(kernel.fn, Heuristics):
            res += "ERROR: Repro will not work as intended, "
            res += "triton.runtime.autotuner.Heuristics is not currently supported\n"
            return res

        config_strs = []
        # pyrefly: ignore [missing-attribute]
        for kernel_config in kernel.configs:
            config_strs.append(f"""triton.Config(
                    {str(kernel_config.kwargs)},
                    num_warps={kernel_config.num_warps},
                    num_stages={kernel_config.num_stages},
                )""")

        config_str = ",".join(config_strs)
        res += textwrap.dedent(f"""
        @triton.autotune(
            configs=[
                {config_str}
            ],
            key=[]
        )
        """).strip()

    # pyrefly: ignore [missing-attribute]
    src_code = kernel.src if isinstance(kernel, JITFunction) else kernel.fn.src
    res += "\n@triton.jit\n"
    res += src_code
    res += "\n"

    return res

