
def arguments(
    arguments: Arguments,
    *,
    faithful: bool,
    symint: bool = False,
    method: bool,
    cpp_no_default_args: set[str],
) -> list[Binding]:
    args: list[Argument | TensorOptionsArguments | SelfArgument] = []
    if faithful:
        args.extend(arguments.non_out)
        args.extend(arguments.out)
    else:
        args.extend(arguments.out)
        args.extend(arguments.non_out)
    return [
        r.no_default() if faithful else r
        for a in args
        for r in argument(
            a,
            faithful=faithful,
            symint=symint,
            method=method,
            has_tensor_options=arguments.tensor_options is not None,
            cpp_no_default_args=cpp_no_default_args,
        )
    ]


def arguments(func: FunctionSchema, *, symint: bool = True) -> list[Binding]:
    return [argument(a, symint=symint) for a in jit_arguments(func)]


def arguments(func: FunctionSchema, *, symint: bool) -> list[Binding]:
    args: list[Argument | TensorOptionsArguments | SelfArgument] = []
    args.extend(func.arguments.non_out)
    args.extend(func.arguments.out)
    return [
        r for arg in args for r in argument(arg, symint=symint, is_out=func.is_out_fn())
    ]


def arguments():
    import argparse  # noqa: PLC0415

    parser = argparse.ArgumentParser(description="Benchmark Stable Diffusion pipeline (optional control net for SDXL)")
    parser.add_argument(
        "--engine",
        type=str,
        default="torch",
        choices=["torch", "stable_fast", "ort_cuda", "ort_trt"],
        help="Backend engine: torch, stable_fast or ort_cuda",
    )

    parser.add_argument(
        "--name",
        type=str,
        choices=list(PipelineInfo.supported_models().keys()),
        default="stabilityai/sdxl-turbo",
        help="Stable diffusion model name. Default is stabilityai/sdxl-turbo",
    )

    parser.add_argument(
        "--work-dir",
        type=str,
        default=".",
        help="working directory for ort_cuda or ort_trt",
    )

    parser.add_argument(
        "--use_control_net",
        action="store_true",
        help="Use control net diffusers/controlnet-canny-sdxl-1.0",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="Batch size",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=1,
        help="Denoising steps",
    )

    parser.add_argument(
        "--warmup_runs",
        type=int,
        default=3,
        help="Number of warmup runs before measurement",
    )

    parser.add_argument(
        "--use_nhwc",
        action="store_true",
        help="use channel last format for torch compile",
    )

    parser.add_argument(
        "--enable_cuda_graph",
        action="store_true",
        help="enable cuda graph for stable fast",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print more information",
    )

    args = parser.parse_args()
    return args

