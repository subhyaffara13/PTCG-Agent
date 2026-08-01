
def _dump_launch_params(args, kwargs, launcher, kernel_name, grid):
    call_args = []
    call_kwargs = {}
    for arg in args:
        if isinstance(arg, (int, bool)):
            call_args.append(str(arg))
        else:
            call_args.append("T")
    for k, v in kwargs.items():
        if isinstance(arg, (int, bool)):
            call_kwargs[k] = v
        else:
            call_kwargs[k] = v
    call_kwargs.update(launcher.config.kwargs)
    call_kwargs["num_warps"] = launcher.config.num_warps
    call_kwargs["num_stages"] = launcher.config.num_stages
    if HAS_WARP_SPEC:
        call_kwargs["num_consumer_groups"] = getattr(
            launcher.config, "num_consumer_groups", 0
        )
        call_kwargs["num_buffers_warp_spec"] = getattr(
            launcher.config, "num_buffers_warp_spec", 0
        )
    args_str = [*call_args]
    args_str.extend(f"{k}={v}" for k, v in call_kwargs.items())
    args_str = ", ".join(args_str)
    abs_path = os.path.abspath(sys.argv[0])
    with open(f"{abs_path}.launch_params", "a") as f:
        f.write(f"{kernel_name} | {args_str} | {grid!r}\n")

