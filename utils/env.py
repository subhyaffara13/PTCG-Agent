
def env(
    accelerate_config_file: Annotated[
        str | None,
        typer.Argument(help="The accelerate config file to use for the default values in the launching script."),
    ] = None,
) -> None:
    """Print information about the environment."""
    import safetensors

    # TODO: remove hasattr guard once safetensors >= 0.8.0 is released (adds __version__)
    safetensors_version = safetensors.__version__ if hasattr(safetensors, "__version__") else "unknown"

    accelerate_version = "not installed"
    accelerate_config = accelerate_config_str = "not found"

    if is_accelerate_available():
        import accelerate
        from accelerate.commands.config import default_config_file, load_config_from_file

        accelerate_version = accelerate.__version__
        # Get the default from the config file.
        if accelerate_config_file is not None or os.path.isfile(default_config_file):
            accelerate_config = load_config_from_file(accelerate_config_file).to_dict()

        accelerate_config_str = (
            "\n".join([f"\t- {prop}: {val}" for prop, val in accelerate_config.items()])
            if isinstance(accelerate_config, dict)
            else f"\t{accelerate_config}"
        )

    pt_version = "not installed"
    pt_cuda_available = "NA"
    pt_accelerator = "NA"
    if is_torch_available():
        import torch

        pt_version = torch.__version__
        pt_cuda_available = torch.cuda.is_available()
        pt_xpu_available = is_torch_xpu_available()
        pt_npu_available = is_torch_npu_available()
        pt_hpu_available = is_torch_hpu_available()

        if pt_cuda_available:
            pt_accelerator = "CUDA"
        elif pt_xpu_available:
            pt_accelerator = "XPU"
        elif pt_npu_available:
            pt_accelerator = "NPU"
        elif pt_hpu_available:
            pt_accelerator = "HPU"

    deepspeed_version = "not installed"
    if is_deepspeed_available():
        # Redirect command line output to silence deepspeed import output.
        with contextlib.redirect_stdout(io.StringIO()):
            import deepspeed
        deepspeed_version = deepspeed.__version__

    info = {
        "`transformers` version": __version__,
        "Platform": platform.platform(),
        "Python version": platform.python_version(),
        "Huggingface_hub version": huggingface_hub.__version__,
        "Safetensors version": f"{safetensors_version}",
        "Accelerate version": f"{accelerate_version}",
        "Accelerate config": f"{accelerate_config_str}",
        "DeepSpeed version": f"{deepspeed_version}",
        "PyTorch version (accelerator?)": f"{pt_version} ({pt_accelerator})",
        "Using distributed or parallel set-up in script?": "<fill in>",
    }
    if is_torch_available():
        if pt_cuda_available:
            info["Using GPU in script?"] = "<fill in>"
            info["GPU type"] = torch.cuda.get_device_name()
        elif pt_xpu_available:
            info["Using XPU in script?"] = "<fill in>"
            info["XPU type"] = torch.xpu.get_device_name()
        elif pt_hpu_available and hasattr(torch, "hpu"):
            info["Using HPU in script?"] = "<fill in>"
            info["HPU type"] = torch.hpu.get_device_name()
        elif pt_npu_available and hasattr(torch, "npu"):
            info["Using NPU in script?"] = "<fill in>"
            info["NPU type"] = torch.npu.get_device_name()
            if hasattr(torch.version, "cann"):
                info["CANN version"] = torch.version.cann

    print("\nCopy-and-paste the text below in your GitHub issue and FILL OUT the two last points.\n")
    print(_format_dict(info))

    return info


def env():
    with contexts.tempdir(prefix='setuptools-test.') as env_dir:
        env = Environment(env_dir)
        os.chmod(env_dir, stat.S_IRWXU)
        subs = 'home', 'lib', 'scripts', 'data', 'egg-base'
        env.paths = dict((dirname, os.path.join(env_dir, dirname)) for dirname in subs)
        list(map(os.mkdir, env.paths.values()))
        path.build({
            env.paths['home']: {
                '.pydistutils.cfg': DALS(
                    """
                [egg_info]
                egg-base = {egg-base}
                """.format(**env.paths)
                )
            }
        })
        yield env


def env():
    env = raw_env()
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env():
    env = raw_env()
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.ClipOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.ClipOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    render_mode = kwargs.get("render_mode")
    if render_mode == "ansi":
        kwargs["render_mode"] = "human"
        env = raw_env(**kwargs)
        env = wrappers.CaptureStdoutWrapper(env)
    else:
        env = raw_env(**kwargs)

    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(render_mode=None):
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env(**kwargs):
    env = raw_env(**kwargs)
    if env.continuous:
        env = wrappers.ClipOutOfBoundsWrapper(env)
    else:
        env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def env():
    project_dir = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
    template_dir = project_dir / "io" / "formats" / "templates"
    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.Environment(loader=loader, trim_blocks=True)
    return env


def env() -> None:
    """Print information about the environment."""
    dump_environment_info()

