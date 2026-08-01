
def run(args: List[str]) -> None:
    assert len(args) == 1, "codespell_errors.txt"
    cache = {}
    done = set()
    with open(args[0]) as f:
        lines = f.read().splitlines()

    for line in sorted(lines):
        i = line.find(" ==> ")
        if i > 0:
            flds = line[:i].split(":")
            if len(flds) >= 2:
                filename, line_num = flds[:2]
                if filename not in cache:
                    with open(filename) as f:
                        cache[filename] = f.read().splitlines()
                supp = cache[filename][int(line_num) - 1]
                if supp not in done:
                    print(supp)
                    done.add(supp)


def run(
    main,
    argv=None,
    flags_parser=parse_flags_with_usage,
):
  """Begins executing the program.

  Args:
    main: The main function to execute. It takes an single argument "argv",
        which is a list of command line arguments with parsed flags removed.
        The return value is passed to `sys.exit`, and so for example
        a return value of 0 or None results in a successful termination, whereas
        a return value of 1 results in abnormal termination.
        For more details, see https://docs.python.org/3/library/sys#sys.exit
    argv: A non-empty list of the command line arguments including program name,
        sys.argv is used if None.
    flags_parser: Callable[[List[str]], Any], the function used to parse flags.
        The return value of this function is passed to `main` untouched.
        It must guarantee FLAGS is parsed after this function is called.
        Should be passed as a keyword-only arg which will become mandatory in a
        future release.
  - Parses command line flags with the flag module.
  - If there are any errors, prints usage().
  - Calls main() with the remaining arguments.
  - If main() raises a UsageError, prints usage and the error message.
  """
  # fmt: on
  try:
    args = _run_init(
        sys.argv if argv is None else argv,
        flags_parser,
    )
    while _init_callbacks:
      callback = _init_callbacks.popleft()
      callback()
    try:
      _run_main(main, args)
    except UsageError as error:
      usage(shorthelp=True, detailed_error=error, exitcode=error.exitcode)
    except:
      exc = sys.exc_info()[1]
      # Don't try to post-mortem debug successful SystemExits, since those
      # mean there wasn't actually an error. In particular, the test framework
      # raises SystemExit(False) even if all tests passed.
      if isinstance(exc, SystemExit) and not exc.code:
        raise

      # Check the tty so that we don't hang waiting for input in an
      # non-interactive scenario.
      if FLAGS.pdb_post_mortem and sys.stdout.isatty():
        traceback.print_exc()
        print()
        print(' *** Entering post-mortem debugging ***')
        print()
        _get_debugger_module_with_function('post_mortem').post_mortem()
      raise
  except Exception as e:
    _call_exception_handlers(e)
    raise


def run(
    func: Callable[[Unpack[PosArgsT]], Coroutine[Any, Any, T_co]],
    *args: Unpack[PosArgsT],
    token: EventLoopToken | None = None,
) -> T_co:
    """
    Call a coroutine function from a worker thread.

    :param func: a coroutine function
    :param args: positional arguments for the callable
    :param token: an event loop token to use to get back to the event loop thread
        (required if calling this function from outside an AnyIO worker thread)
    :return: the return value of the coroutine function
    :raises MissingTokenError: if no token was provided and called from outside an
        AnyIO worker thread
    :raises RunFinishedError: if the event loop tied to ``token`` is no longer running

    .. versionchanged:: 4.11.0
        Added the ``token`` parameter.

    """
    explicit_token = token is not None
    token = _token_or_error(token)
    return token.backend_class.run_async_from_thread(
        func, args, token=token.native_token if explicit_token else None
    )


def run(ctx: click.Context, override: bool, commandline: tuple[str, ...]) -> None:
    """Run command with environment variables present."""
    file = ctx.obj["FILE"]
    if not os.path.isfile(file):
        raise click.BadParameter(
            f"Invalid value for '-f' \"{file}\" does not exist.", ctx=ctx
        )
    dotenv_as_dict = {
        k: v
        for (k, v) in dotenv_values(file).items()
        if v is not None and (override or k not in os.environ)
    }

    if not commandline:
        click.echo("No command given.")
        sys.exit(1)

    run_command([*commandline, *ctx.args], dotenv_as_dict)


def run(
    fs,
    path,
    mount_point,
    foreground=True,
    threads=False,
    ready_file=False,
    ops_class=FUSEr,
):
    """Mount stuff in a local directory

    This uses fusepy to make it appear as if a given path on an fsspec
    instance is in fact resident within the local file-system.

    This requires that fusepy by installed, and that FUSE be available on
    the system (typically requiring a package to be installed with
    apt, yum, brew, etc.).

    Parameters
    ----------
    fs: file-system instance
        From one of the compatible implementations
    path: str
        Location on that file-system to regard as the root directory to
        mount. Note that you typically should include the terminating "/"
        character.
    mount_point: str
        An empty directory on the local file-system where the contents of
        the remote path will appear.
    foreground: bool
        Whether or not calling this function will block. Operation will
        typically be more stable if True.
    threads: bool
        Whether or not to create threads when responding to file operations
        within the mounter directory. Operation will typically be more
        stable if False.
    ready_file: bool
        Whether the FUSE process is ready. The ``.fuse_ready`` file will
        exist in the ``mount_point`` directory if True. Debugging purpose.
    ops_class: FUSEr or Subclass of FUSEr
        To override the default behavior of FUSEr. For Example, logging
        to file.

    """
    func = lambda: FUSE(
        ops_class(fs, path, ready_file=ready_file),
        mount_point,
        nothreads=not threads,
        foreground=foreground,
    )
    if not foreground:
        th = threading.Thread(target=func)
        th.daemon = True
        th.start()
        return th
    else:  # pragma: no cover
        try:
            func()
        except KeyboardInterrupt:
            pass


def run():
    for path in sys.path:
        inspect(path)


def run(arguments, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin):  # noqa: D103
    outputter = _Outputter.from_arguments(
        arguments=arguments,
        stdout=stdout,
        stderr=stderr,
    )

    try:
        schema = outputter.load(arguments["schema"])
    except _CannotLoadFile:
        return 1

    Validator = arguments["validator"]
    if Validator is None:
        Validator = validator_for(schema)

    try:
        Validator.check_schema(schema)
    except SchemaError as error:
        outputter.validation_error(
            instance_path=arguments["schema"],
            error=error,
        )
        return 1

    if arguments["instances"]:
        load, instances = outputter.load, arguments["instances"]
    else:
        def load(_):
            try:
                return json.load(stdin)
            except JSONDecodeError as error:
                outputter.parsing_error(
                    path="<stdin>", exc_info=sys.exc_info(),
                )
                raise _CannotLoadFile() from error
        instances = ["<stdin>"]

    resolver = _RefResolver(
        base_uri=arguments["base_uri"],
        referrer=schema,
    ) if arguments["base_uri"] is not None else None

    validator = Validator(schema, resolver=resolver)
    exit_code = 0
    for each in instances:
        try:
            instance = load(each)
        except _CannotLoadFile:
            exit_code = 1
        else:
            exit_code |= _validate_instance(
                instance_path=each,
                instance=instance,
                validator=validator,
                outputter=outputter,
            )

    return exit_code


def run(args: list[str]) -> tuple[str, str, int]:
    # Lazy import to avoid needing to import all of mypy to call run_dmypy
    from mypy.main import main

    return _run(
        lambda stdout, stderr: main(args=args, stdout=stdout, stderr=stderr, clean_exit=True)
    )


def run(args: Sequence[str], *, log_stdout: bool = False, state: AuditState = AuditState()) -> str:
    """
    Execute the given arguments.

    Uses `state` to provide feedback on the subprocess's status.

    Raises a `CalledProcessError` if the subprocess fails. Otherwise, returns
    the process's `stdout` stream as a string.
    """

    # NOTE(ww): We frequently run commands inside of ephemeral virtual environments,
    # which have long absolute paths on some platforms. These make for confusing
    # state updates, so we trim the first argument down to its basename.
    pretty_args = " ".join([os.path.basename(args[0]), *args[1:]])

    terminated = False
    stdout = b""
    stderr = b""

    # Run the process with unbuffered I/O, to make the poll-and-read loop below
    # more responsive.
    with Popen(args, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        # NOTE: We use `poll()` to control this loop instead of the `read()` call
        # to prevent deadlocks. Similarly, `read(size)` will return an empty bytes
        # once `stdout` hits EOF, so we don't have to worry about that blocking.
        while not terminated:
            terminated = process.poll() is not None
            stdout += process.stdout.read()  # type: ignore
            stderr += process.stderr.read()  # type: ignore
            state.update_state(
                f"Running {pretty_args}",
                stdout.decode(errors="replace") if log_stdout else None,
            )

        if process.returncode != 0:
            raise CalledProcessError(
                f"{pretty_args} exited with {process.returncode}",
                stderr=stderr.decode(errors="replace"),
            )

    return stdout.decode("utf-8", errors="replace")


def run() -> None:
    """
    Run the script in sys.argv[1] as if it had
    been invoked naturally.
    """
    __builtins__
    script_name = sys.argv[1]
    namespace = dict(
        __file__=script_name,
        __name__='__main__',
        __doc__=None,
    )
    sys.argv[:] = sys.argv[1:]

    open_ = getattr(tokenize, 'open', open)
    with open_(script_name) as fid:
        script = fid.read()
    norm_script = script.replace('\\r\\n', '\\n')
    code = compile(norm_script, script_name, 'exec')
    exec(code, namespace)


def run(
    source_yaml: str, output_dir: str, dry_run: bool, impl_path: str | None = None
) -> None:
    # Assumes that this file lives at torchgen/gen_backend_stubs.py
    root = Path(__file__).absolute().parent.parent
    common_dir = os.path.join(root, "aten/src")  # Assumes root is pytorch_root
    if not os.path.exists(common_dir):  # This file is out-of-tree.
        common_dir = os.path.join(root, "torchgen/packaged")

    template_dir = os.path.join(common_dir, "ATen/templates")

    def make_file_manager(install_dir: str) -> FileManager:
        return FileManager(
            install_dir=install_dir, template_dir=template_dir, dry_run=dry_run
        )

    fm = make_file_manager(output_dir)

    native_yaml_path = os.path.join(common_dir, "ATen/native/native_functions.yaml")
    tags_yaml_path = os.path.join(common_dir, "ATen/native/tags.yaml")
    parsed_yaml = parse_native_yaml(native_yaml_path, tags_yaml_path)
    native_functions, backend_indices = (
        parsed_yaml.native_functions,
        parsed_yaml.backend_indices,
    )
    grouped_native_functions = get_grouped_native_functions(native_functions)
    parsed_backend_yaml = parse_backend_yaml(
        source_yaml, grouped_native_functions, backend_indices
    )
    backend_key = parsed_backend_yaml.backend_key
    autograd_key = parsed_backend_yaml.autograd_key
    cpp_namespace = parsed_backend_yaml.cpp_namespace
    class_name = parsed_backend_yaml.class_name
    backend_indices = parsed_backend_yaml.backend_indices

    selector = SelectiveBuilder.get_nop_selector()

    if backend_key is None:
        # This could be useful if a backend wants to quickly set up a noop yaml file but doesn't have any kernels ready yet.
        return

    if class_name is None:
        # class_name is an optional argument to backend yaml file.
        # if specified it allows an external backend to override
        # the name of the class that all generated kernel definitions live under.
        # if not specified, its value is given as native_function_class_name.
        class_name = backend_indices[backend_key].native_function_class_name()
    if class_name is None:
        raise AssertionError("class_name must not be None")

    if impl_path is not None:
        error_on_missing_kernels(
            native_functions,
            backend_indices,
            backend_key,
            autograd_key,
            class_name,
            impl_path,
        )

    gen_dispatchkey_nativefunc_headers(
        fm,
        class_name,
        cpp_namespace,
        backend_indices,
        grouped_native_functions,
        backend_key,
        autograd_key,
    )

    for dispatch_key in (
        [backend_key] if autograd_key is None else [backend_key, autograd_key]
    ):
        gen_dispatcher_registrations(
            fm,
            output_dir,
            class_name,
            backend_indices,
            grouped_native_functions,
            backend_key,
            dispatch_key,
            selector,
        )


def run(
    function: Annotated[
        Callable[..., Any],
        Doc(
            """
            The function that should power this CLI application.
            """
        ),
    ],
) -> None:
    """
    This function converts a given function to a CLI application with `Typer()` and executes it.

    ## Example

    ```python
    import typer

    def main(name: str):
        print(f"Hello {name}")

    if __name__ == "__main__":
        typer.run(main)
    ```
    """
    app = Typer(add_completion=False)
    app.command()(function)
    app()


def run(args):
    torch.multiprocessing._set_thread_name("pt_elastic")

    if args.standalone:
        args.rdzv_backend = "c10d"
        args.rdzv_endpoint = "localhost:0"
        args.rdzv_id = str(uuid.uuid4())
        logger.info(
            "\n**************************************\n"
            "Rendezvous info:\n"
            "--rdzv-backend=%s "
            "--rdzv-endpoint=%s "
            "--rdzv-id=%s\n"
            "**************************************\n",
            args.rdzv_backend,
            args.rdzv_endpoint,
            args.rdzv_id,
        )
    elif (
        args.rdzv_backend == "static"
        and not args.rdzv_endpoint
        and args.master_port is None
    ):
        _, max_nodes = parse_min_max_nnodes(args.nnodes)
        if max_nodes == 1:
            args.rdzv_backend = "c10d"
            args.rdzv_endpoint = "localhost:0"
            args.rdzv_id = str(uuid.uuid4())

    # master_port is only used for the static rendezvous backend, not c10d
    if args.master_port is None:
        args.master_port = 29500

    config, cmd, cmd_args = config_from_args(args)
    elastic_launch(
        config=config,
        entrypoint=cmd,
    )(*cmd_args)


def run(command):
    """Return (return-code, stdout, stderr)."""
    shell = type(command) is str
    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
    )
    raw_output, raw_err = p.communicate()
    rc = p.returncode
    if get_platform() == "win32":
        enc = "oem"
    else:
        enc = locale.getpreferredencoding()
    output = raw_output.decode(enc)
    err = raw_err.decode(enc)
    return rc, output.strip(), err.strip()


def run(fn: Callable[_P, _R] | None = None) -> Any:
    """Don't do any dynamic compiles, just use prior optimizations"""
    if fn is not None:
        fn = innermost_fn(fn)
        assert callable(fn)
        return RunOnlyContext()(fn)
    return RunOnlyContext()


def run(
    num_groups: int,
    problem_sizes_mnkl: tuple[int, int, int, int],
    host_problem_shape_available: bool,
    ab_dtype: Type[cutlass.Numeric],
    c_dtype: Type[cutlass.Numeric],
    acc_dtype: Type[cutlass.Numeric],
    a_major: str,
    b_major: str,
    c_major: str,
    mma_tiler_mn: tuple[int, int],
    cluster_shape_mn: tuple[int, int],
    use_2cta_instrs: bool,
    tensormap_update_mode: utils.TensorMapUpdateMode,
    tolerance: float,
    warmup_iterations: int,
    iterations: int,
    skip_ref_check: bool,
    use_cold_l2: bool = False,
    **kwargs,
):
    """Run grouped GEMM example with specified configurations.

    :param use_cold_l2: Whether to use circular buffer strategy to ensure cold L2 cache, defaults to False
    :type use_cold_l2: bool, optional
    :return: Execution time of the GEMM kernel in microseconds
    :rtype: float
    """
    print("Running Blackwell Grouped GEMM test with:")
    print(f"{num_groups} groups")
    for i, (m, n, k, l) in enumerate(problem_sizes_mnkl):
        print(f"Group {i}: {m}x{n}x{k}x{l}")
    print(f"AB dtype: {ab_dtype}, C dtype: {c_dtype}, Acc dtype: {acc_dtype}")
    print(f"Matrix majors - A: {a_major}, B: {b_major}, C: {c_major}")
    print(f"Mma Tiler (M, N): {mma_tiler_mn}, Cluster Shape (M, N): {cluster_shape_mn}")
    print(f"2CTA MMA instructions: {'True' if use_2cta_instrs else 'False'}")
    print(f"Tensor map update mode: {tensormap_update_mode}")
    print(f"Tolerance: {tolerance}")
    print(f"Warmup iterations: {warmup_iterations}")
    print(f"Iterations: {iterations}")
    print(f"Skip reference checking: {skip_ref_check}")
    print(f"Use cold L2: {'True' if use_cold_l2 else 'False'}")

    # Skip unsupported types
    if ab_dtype not in {
        cutlass.Float16,
        cutlass.BFloat16,
    }:
        raise ValueError(f"Skip unsupported ab_dtype {ab_dtype}")
    if c_dtype not in {cutlass.Float16, cutlass.BFloat16, cutlass.Float32}:
        raise ValueError(f"Skip unsupported c_dtype {c_dtype}")
    # Skip unsupported acc dtype
    if acc_dtype not in {cutlass.Float32, cutlass.Float16}:
        raise ValueError(f"Skip unsupported acc_dtype {acc_dtype}")
    # Skip invalid ab_dtype and acc_dtype combination
    if ab_dtype == cutlass.BFloat16 and acc_dtype == cutlass.Float16:
        raise ValueError("Skip invalid ab_dtype and acc_dtype combination")
    # Skip invalid mma tile shape
    if not (
        (not use_2cta_instrs and mma_tiler_mn[0] in [64, 128])
        or (use_2cta_instrs and mma_tiler_mn[0] in [128, 256])
    ):
        raise ValueError(f"Skip invalid mma tiler M {mma_tiler_mn[0]}")
    if mma_tiler_mn[1] not in range(32, 257, 32):
        raise ValueError(f"Skip invalid mma tiler N {mma_tiler_mn[1]}")
    # Skip illegal cluster shape
    if cluster_shape_mn[0] % (2 if use_2cta_instrs else 1) != 0:
        raise ValueError(
            f"cluster_shape_m need align with use_2cta_instrs config {cluster_shape_mn}"
        )
    # Skip invalid cluster shape
    is_power_of_2 = lambda x: x > 0 and (x & (x - 1)) == 0
    if (
        cluster_shape_mn[0] * cluster_shape_mn[1] > 16
        or cluster_shape_mn[0] <= 0
        or cluster_shape_mn[1] <= 0
        or not is_power_of_2(cluster_shape_mn[0])
        or not is_power_of_2(cluster_shape_mn[1])
    ):
        raise ValueError(f"Skip invalid cluster shape {cluster_shape_mn}")

    # Skip illegal problem shape for load/store alignment
    def check_contigous_16B_alignment(dtype, is_mode0_major, tensor_shape):
        major_mode_idx = 0 if is_mode0_major else 1
        num_major_elements = tensor_shape[major_mode_idx]
        num_contiguous_elements = 16 * 8 // dtype.width
        return num_major_elements % num_contiguous_elements == 0

    if (
        not check_contigous_16B_alignment(ab_dtype, a_major == "m", (m, k, l))
        or not check_contigous_16B_alignment(ab_dtype, b_major == "n", (n, k, l))
        or not check_contigous_16B_alignment(c_dtype, c_major == "m", (m, n, l))
    ):
        raise ValueError("Skip invalid problem alignment")
    if not torch.cuda.is_available():
        raise RuntimeError("GPU is required to run this example!")

    # Create tensors for all groups using the new function
    (
        ptrs_abc,
        torch_tensors_abc,
        cute_tensors_abc,
        strides_abc,
        torch_fp32_tensors_abc,
    ) = create_tensors_for_all_groups(
        problem_sizes_mnkl,
        ab_dtype,
        c_dtype,
        a_major,
        b_major,
        c_major,
    )

    # Setup inital tensors for TMA of A,B and C
    alignment = 16  # 16 bytes aligned
    min_ab_size = alignment * 8 // ab_dtype.width
    min_c_size = alignment * 8 // c_dtype.width
    initial_cute_tensors_abc = [
        create_tensor_and_stride(1, min_ab_size, min_ab_size, a_major == "m", ab_dtype)[
            2
        ],
        create_tensor_and_stride(1, min_ab_size, min_ab_size, b_major == "n", ab_dtype)[
            2
        ],
        create_tensor_and_stride(1, min_c_size, min_c_size, c_major == "m", c_dtype)[2],
    ]

    hardware_info = utils.HardwareInfo()
    sm_count = hardware_info.get_max_active_clusters(1)
    max_active_clusters = hardware_info.get_max_active_clusters(
        cluster_shape_mn[0] * cluster_shape_mn[1]
    )

    # Prepare tensormap buffer for each SM
    num_tensormap_buffers = sm_count
    tensormap_shape = (
        num_tensormap_buffers,
        GroupedGemmKernel.num_tensormaps,
        GroupedGemmKernel.bytes_per_tensormap // 8,
    )
    tensor_of_tensormap, tensor_of_tensormap_torch = cutlass_torch.cute_tensor_like(
        torch.empty(tensormap_shape, dtype=torch.int64),
        cutlass.Int64,
        is_dynamic_layout=False,
    )

    grouped_gemm = GroupedGemmKernel(
        acc_dtype,
        use_2cta_instrs,
        mma_tiler_mn,
        cluster_shape_mn,
        tensormap_update_mode,
    )

    # layout (num_groups, 4):(4, 1)
    (
        tensor_of_dim_size_mnkl,
        tensor_of_dim_size_mnkl_torch,
    ) = cutlass_torch.cute_tensor_like(
        torch.tensor(problem_sizes_mnkl, dtype=torch.int32),
        cutlass.Int32,
        is_dynamic_layout=False,
        assumed_align=16,
    )

    # layout (num_groups, 3, 2):(6, 2, 1)
    tensor_of_strides_abc, tensor_of_strides_abc_torch = cutlass_torch.cute_tensor_like(
        torch.tensor(strides_abc, dtype=torch.int32),
        cutlass.Int32,
        is_dynamic_layout=False,
        assumed_align=16,
    )

    # layout (num_groups,3):(3, 1)
    tensor_of_ptrs_abc, tensor_of_ptrs_abc_torch = cutlass_torch.cute_tensor_like(
        torch.tensor(ptrs_abc, dtype=torch.int64),
        cutlass.Int64,
        is_dynamic_layout=False,
        assumed_align=16,
    )

    # Compute total number of cluster tiles we need to compute for given grouped GEMM problem
    def compute_total_num_clusters(
        problem_sizes_mnkl: List[tuple[int, int, int, int]],
        cluster_tile_shape_mn: tuple[int, int],
    ) -> int:
        total_num_clusters = 0
        for m, n, _, _ in problem_sizes_mnkl:
            num_clusters_mn = tuple(
                (x + y - 1) // y for x, y in zip((m, n), cluster_tile_shape_mn)
            )
            total_num_clusters += functools.reduce(lambda x, y: x * y, num_clusters_mn)
        return total_num_clusters

    # Compute cluster tile shape
    def compute_cluster_tile_shape(
        mma_tiler_mn: tuple[int, int],
        cluster_shape_mn: tuple[int, int],
        use_2cta_instrs: bool,
    ) -> tuple[int, int]:
        cta_tile_shape_mn = list(mma_tiler_mn)
        if use_2cta_instrs:
            cta_tile_shape_mn[0] = cta_tile_shape_mn[0] // 2
        return tuple(x * y for x, y in zip(cta_tile_shape_mn, cluster_shape_mn))

    cluster_tile_shape_mn = compute_cluster_tile_shape(
        mma_tiler_mn, cluster_shape_mn, use_2cta_instrs
    )

    # If the host problem shape is available, we will launch the grid with only
    # the necessary clusters. The function compute_total_num_clusters() does that.
    # If the problem shape only exists on device, we will need to launch all active
    # clusters possible on a device.
    if host_problem_shape_available:
        print("Problem shapes available on host and device")
        total_num_clusters = compute_total_num_clusters(
            problem_sizes_mnkl, cluster_tile_shape_mn
        )
    else:
        print("Problem shapes available only on device")
        total_num_clusters = max_active_clusters

    # Initialize Stream
    current_stream = cutlass_torch.default_stream()

    # try to check CUDA version to decide the opt level
    try:
        from cutlass import CUDA_VERSION

        opt_level = (
            3
            if CUDA_VERSION.major < 13
            or (CUDA_VERSION.major == 13 and CUDA_VERSION.minor < 1)
            else 2
        )
    except ImportError:
        opt_level = 3
    # Compile grouped GEMM kernel
    compiled_grouped_gemm = cute.compile(
        grouped_gemm,
        initial_cute_tensors_abc[0],
        initial_cute_tensors_abc[1],
        initial_cute_tensors_abc[2],
        num_groups,
        tensor_of_dim_size_mnkl,
        tensor_of_strides_abc,
        tensor_of_ptrs_abc,
        total_num_clusters,
        tensor_of_tensormap,
        max_active_clusters,
        current_stream,
        options=f"--opt-level {opt_level}",
    )

    if not skip_ref_check:
        compiled_grouped_gemm(
            initial_cute_tensors_abc[0],
            initial_cute_tensors_abc[1],
            initial_cute_tensors_abc[2],
            tensor_of_dim_size_mnkl,
            tensor_of_strides_abc,
            tensor_of_ptrs_abc,
            tensor_of_tensormap,
            current_stream,
        )

        # Compute reference result
        for i, (a, b, c) in enumerate(torch_tensors_abc):
            ref = torch.einsum(
                "mkl,nkl->mnl",
                a.cpu().to(dtype=torch.float32),
                b.cpu().to(dtype=torch.float32),
            )
            print(f"checking group {i}")
            torch.testing.assert_close(
                c.cpu(),
                ref.to(cutlass_torch.dtype(c_dtype)),
                atol=tolerance,
                rtol=1e-05,
            )

    if iterations <= 0:
        return 0

    def generate_tensors():
        # Reuse existing CPU tensors and create new GPU tensors from them
        (
            ptrs_abc_workspace,
            torch_tensors_abc_workspace,
            cute_tensors_abc_workspace,
            strides_abc_workspace,
            _,
        ) = create_tensors_for_all_groups(
            problem_sizes_mnkl,
            ab_dtype,
            c_dtype,
            a_major,
            b_major,
            c_major,
            torch_fp32_tensors_abc,
        )

        initial_cute_tensors_abc_workspace = [
            create_tensor_and_stride(
                1, min_ab_size, min_ab_size, a_major == "m", ab_dtype
            )[2],
            create_tensor_and_stride(
                1, min_ab_size, min_ab_size, b_major == "n", ab_dtype
            )[2],
            create_tensor_and_stride(
                1, min_c_size, min_c_size, c_major == "m", c_dtype
            )[2],
        ]

        # Create new tensors for this workspace
        tensor_of_strides_abc_workspace, _ = cutlass_torch.cute_tensor_like(
            torch.tensor(strides_abc_workspace, dtype=torch.int32),
            cutlass.Int32,
            is_dynamic_layout=False,
            assumed_align=16,
        )

        tensor_of_ptrs_abc_workspace, _ = cutlass_torch.cute_tensor_like(
            torch.tensor(ptrs_abc_workspace, dtype=torch.int64),
            cutlass.Int64,
            is_dynamic_layout=False,
            assumed_align=16,
        )

        tensormap_workspace, _ = cutlass_torch.cute_tensor_like(
            torch.empty(tensormap_shape, dtype=torch.int64),
            cutlass.Int64,
            is_dynamic_layout=False,
        )

        args = testing.JitArguments(
            initial_cute_tensors_abc_workspace[0],
            initial_cute_tensors_abc_workspace[1],
            initial_cute_tensors_abc_workspace[2],
            tensor_of_dim_size_mnkl,
            tensor_of_strides_abc_workspace,
            tensor_of_ptrs_abc_workspace,
            tensormap_workspace,
            current_stream,
        )
        args.add_to_scope([torch_tensors_abc_workspace])
        return args

    workspace_count = 1
    if use_cold_l2:
        one_workspace_bytes = (
            sum(
                [
                    sum(
                        [
                            torch_tensor.numel() * torch_tensor.element_size()
                            for torch_tensor in group_tensors
                        ]
                    )
                    for group_tensors in torch_tensors_abc
                ]
            )
            +
            # Add size of strides tensor
            tensor_of_strides_abc_torch.numel()
            * tensor_of_strides_abc_torch.element_size()
            +
            # Add size of ptrs tensor
            tensor_of_ptrs_abc_torch.numel() * tensor_of_ptrs_abc_torch.element_size()
            +
            # Add size of tensormap tensor
            tensor_of_tensormap_torch.numel() * tensor_of_tensormap_torch.element_size()
        )
        workspace_count = testing.get_workspace_count(
            one_workspace_bytes, warmup_iterations, iterations
        )

    exec_time = testing.benchmark(
        compiled_grouped_gemm,
        workspace_generator=generate_tensors,
        workspace_count=workspace_count,
        stream=current_stream,
        warmup_iterations=warmup_iterations,
        iterations=iterations,
    )

    runtime_s = exec_time / 1.0e6
    fmas = 0
    for group in range(num_groups):
        [M, N, K, _] = problem_sizes_mnkl[group]
        fmas += M * N * K
    flop = 2 * fmas
    gflop = flop / 1.0e9
    gflops = gflop / runtime_s

    print("Average Runtime : ", exec_time / 1000, "ms")
    print("GFLOPS          : ", gflops)

    return exec_time  # Return execution time in microseconds


def run(n, stmt, fuzzer_cls) -> None:
    float_iter = fuzzer_cls(seed=0, dtype=torch.float32).take(n)
    int_iter = fuzzer_cls(seed=0, dtype=torch.int32).take(n)
    raw_results = []
    for i, (float_values, int_values) in enumerate(zip(float_iter, int_iter, strict=True)):
        float_tensors, float_tensor_params, float_params = float_values
        int_tensors, int_tensor_params, int_params = int_values

        # This benchmark assumes that the two fuzzers generate identically
        # sized and strided Tensors, since the same seed is used.
        assert_dicts_equal(float_params, int_params)
        assert_dicts_equal(float_tensor_params["x"], int_tensor_params["x"])

        float_measurement, int_measurement = (
            Timer(
                stmt,
                globals=tensors,
            ).blocked_autorange(min_run_time=_MEASURE_TIME)
            for tensors in (float_tensors, int_tensors)
        )

        descriptions = []
        for name in float_tensors:
            shape_str = "(" + ", ".join([
                f"2 ** {int(np.log2(i))}"
                if 2 ** int(np.log2(i)) == i and i > 1
                else str(i)
                for i in float_tensors[name].shape
            ]) + ")"
            order = float_tensor_params[name]["order"]
            order_str = ("" if all(order == np.arange(len(order))) else str(tuple(order)))
            steps = float_tensor_params[name]["steps"]
            steps_str = str(steps) if sum(steps) > len(steps) else ""
            descriptions.append((name, shape_str, order_str, steps_str))
        raw_results.append((float_measurement, int_measurement, descriptions))

        print(f"\r{i + 1} / {n}", end="")
    print()

    parsed_results, name_len, shape_len, order_len, steps_len = [], 0, 0, 0, 0
    for float_measurement, int_measurement, descriptions in raw_results:
        t_float = float_measurement.median * 1e6
        t_int = int_measurement.median * 1e6
        rel_diff = abs(t_float - t_int) / (t_float + t_int) * 2
        parsed_results.append((t_float, t_int, rel_diff, descriptions))
        for name, shape, order, steps in descriptions:
            name_len = max(name_len, len(name))
            shape_len = max(shape_len, len(shape))
            order_len = max(order_len, len(order))
            steps_len = max(steps_len, len(steps))

    parsed_results.sort(key=operator.itemgetter(2))

    print(f"stmt: {stmt}")
    print(f" diff    faster{'':>17}{' ' * name_len} ", end="")
    print(f"{'shape'.ljust(shape_len)}{'':>16}{'order'.ljust(order_len)}", end="")
    print(f"          steps\n{'-' * 100}")
    for results, spacer in [(parsed_results[:10], "..."), (parsed_results[-10:], "")]:
        for t_float, t_int, rel_diff, descriptions in results:
            time_str = [f"{rel_diff * 100:>4.1f}%    {'int' if t_int < t_float else 'float':<20}"]
            time_str.extend(["".ljust(len(time_str[0])) for _ in descriptions[:-1]])
            for t_str, (name, shape, order, steps) in zip(time_str, descriptions, strict=True):
                name = f"{name}:".ljust(name_len + 1)
                shape = shape.ljust(shape_len + 10)
                order = order.ljust(order_len)
                print(f"{t_str} {name}  {shape}|     {order}      |   {steps}")
        print(spacer)


def run():
    for path in sys.path:
        inspect(path)


def run(cmd, env=None):
    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, **(env or {})},
        # ^-- allow overwriting instead of discarding the current env
    )

    out = r.stdout + "\n" + r.stderr
    # pytest omits stdout/err by default, if the test fails they help debugging
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Command: {cmd}\nreturn code: {r.returncode}\n\n{out}")

    if r.returncode == 0:
        return out
    raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)


def run(case, run_lambda, set_key, index=0, total_cases=0):
    """Runs the single passed case, returning an mp dictionary and index"""
    t_start = time.perf_counter()

    res = run_lambda(case)

    print(f"Finished {index + 1}/{total_cases} in batch. "
          f"(Took {time.perf_counter() - t_start}s)")

    return index, set_key, mp_res_to_dict(MPResult(case, res))


def Run(argv: Sequence[str] | None = None) -> NoReturn:
    """Standalone command line access point."""
    parser = argparse.ArgumentParser(
        prog="symilar", description="Finds copy pasted blocks in a set of files."
    )
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "-d",
        "--duplicates",
        type=int,
        default=DEFAULT_MIN_SIMILARITY_LINE,
        help=SimilaritiesChecker.MIN_SIMILARITY_HELP,
    )
    parser.add_argument(
        "-i",
        "--ignore-comments",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_COMMENTS_HELP,
    )
    parser.add_argument(
        "--ignore-docstrings",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_DOCSTRINGS_HELP,
    )
    parser.add_argument(
        "--ignore-imports",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_IMPORTS_HELP,
    )
    parser.add_argument(
        "--ignore-signatures",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_SIGNATURES_HELP,
    )
    parsed_args = parser.parse_args(args=argv)
    similar_runner = Symilar(
        min_lines=parsed_args.duplicates,
        ignore_comments=parsed_args.ignore_comments,
        ignore_docstrings=parsed_args.ignore_docstrings,
        ignore_imports=parsed_args.ignore_imports,
        ignore_signatures=parsed_args.ignore_signatures,
    )
    for filename in parsed_args.files:
        with open(filename, encoding="utf-8") as stream:
            similar_runner.append_stream(filename, stream)
    similar_runner.run()
    # the sys exit must be kept because of the unit tests that rely on it
    sys.exit(0)


def run():
    pg.init()

    fontdir = os.path.dirname(os.path.abspath(__file__))
    font = freetype.Font(os.path.join(fontdir, "data", "sans.ttf"))

    screen = pg.display.set_mode((800, 600))
    screen.fill("gray")

    font.underline_adjustment = 0.5
    font.pad = True
    font.render_to(
        screen,
        (32, 32),
        "Hello World",
        "red3",
        "dimgray",
        size=64,
        style=freetype.STYLE_UNDERLINE | freetype.STYLE_OBLIQUE,
    )
    font.pad = False

    font.render_to(
        screen,
        (32, 128),
        "abcdefghijklm",
        "dimgray",
        "green3",
        size=64,
    )

    font.vertical = True
    font.render_to(screen, (32, 200), "Vertical?", "blue3", None, size=32)
    font.vertical = False

    font.render_to(screen, (64, 190), "Let's spin!", "red3", None, size=48, rotation=55)

    font.render_to(
        screen, (160, 290), "All around!", "green3", None, size=48, rotation=-55
    )

    font.render_to(screen, (250, 220), "and BLEND", (255, 0, 0, 128), None, size=64)

    font.render_to(screen, (265, 237), "or BLAND!", (0, 0xCC, 28, 128), None, size=64)

    # Some pinwheels
    font.origin = True
    for angle in range(0, 360, 45):
        font.render_to(screen, (150, 420), ")", "black", size=48, rotation=angle)
    font.vertical = True
    for angle in range(15, 375, 30):
        font.render_to(screen, (600, 400), "|^*", "orange", size=48, rotation=angle)
    font.vertical = False
    font.origin = False

    utext = "I \u2665 Unicode"
    font.render_to(screen, (298, 320), utext, (0, 0xCC, 0xDD), None, size=64)

    utext = "\u2665"
    font.render_to(screen, (480, 32), utext, "gray", "red3", size=148)

    font.render_to(
        screen,
        (380, 380),
        "...yes, this is an SDL surface",
        "black",
        None,
        size=24,
        style=freetype.STYLE_STRONG,
    )

    font.origin = True
    r = font.render_to(
        screen,
        (100, 530),
        "stretch",
        "red3",
        None,
        size=(24, 24),
        style=freetype.STYLE_NORMAL,
    )
    font.render_to(
        screen,
        (100 + r.width, 530),
        " VERTICAL",
        "red3",
        None,
        size=(24, 48),
        style=freetype.STYLE_NORMAL,
    )

    r = font.render_to(
        screen,
        (100, 580),
        "stretch",
        "blue3",
        None,
        size=(24, 24),
        style=freetype.STYLE_NORMAL,
    )
    font.render_to(
        screen,
        (100 + r.width, 580),
        " HORIZONTAL",
        "blue3",
        None,
        size=(48, 24),
        style=freetype.STYLE_NORMAL,
    )

    pg.display.flip()

    while True:
        if pg.event.wait().type in (pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
            break

    pg.quit()


def run(*args, **kwds):
    """Run the Pygame unit test suite and return (total tests run, fails dict)

    Positional arguments (optional):
    The names of tests to include. If omitted then all tests are run. Test
    names need not include the trailing '_test'.

    Keyword arguments:
    incomplete - fail incomplete tests (default False)
    usesubprocess - run all test suites in the current process
                   (default False, use separate subprocesses)
    dump - dump failures/errors as dict ready to eval (default False)
    file - if provided, the name of a file into which to dump failures/errors
    timings - if provided, the number of times to run each individual test to
              get an average run time (default is run each test once)
    exclude - A list of TAG names to exclude from the run. The items may be
              comma or space separated.
    show_output - show silenced stderr/stdout on errors (default False)
    all - dump all results, not just errors (default False)
    randomize - randomize order of tests (default False)
    seed - if provided, a seed randomizer integer
    multi_thread - if provided, the number of THREADS in which to run
                   subprocessed tests
    time_out - if subprocess is True then the time limit in seconds before
               killing a test (default 30)
    fake - if provided, the name of the fake tests package in the
           run_tests__tests subpackage to run instead of the normal
           Pygame tests
    python - the path to a python executable to run subprocessed tests
             (default sys.executable)
    interactive - allow tests tagged 'interactive'.

    Return value:
    A tuple of total number of tests run, dictionary of error information. The
    dictionary is empty if no errors were recorded.

    By default individual test modules are run in separate subprocesses. This
    recreates normal Pygame usage where pygame.init() and pygame.quit() are
    called only once per program execution, and avoids unfortunate
    interactions between test modules. Also, a time limit is placed on test
    execution, so frozen tests are killed when there time allotment expired.
    Use the single process option if threading is not working properly or if
    tests are taking too long. It is not guaranteed that all tests will pass
    in single process mode.

    Tests are run in a randomized order if the randomize argument is True or a
    seed argument is provided. If no seed integer is provided then the system
    time is used.

    Individual test modules may have a corresponding *_tags.py module,
    defining a __tags__ attribute, a list of tag strings used to selectively
    omit modules from a run. By default only the 'interactive', 'ignore', and
    'subprocess_ignore' tags are ignored. 'interactive' is for modules that
    take user input, like cdrom_test.py. 'ignore' and 'subprocess_ignore' for
    for disabling modules for foreground and subprocess modes respectively.
    These are for disabling tests on optional modules or for experimental
    modules with known problems. These modules can be run from the console as
    a Python program.

    This function can only be called once per Python session. It is not
    reentrant.

    """

    global was_run

    if was_run:
        raise RuntimeError("run() was already called this session")
    was_run = True

    options = kwds.copy()
    option_usesubprocess = options.get("usesubprocess", False)
    option_dump = options.pop("dump", False)
    option_file = options.pop("file", None)
    option_randomize = options.get("randomize", False)
    option_seed = options.get("seed", None)
    option_multi_thread = options.pop("multi_thread", 1)
    option_time_out = options.pop("time_out", 120)
    option_fake = options.pop("fake", None)
    option_python = options.pop("python", sys.executable)
    option_exclude = options.pop("exclude", ())
    option_interactive = options.pop("interactive", False)

    if not option_interactive and "interactive" not in option_exclude:
        option_exclude += ("interactive",)
    if option_usesubprocess and "subprocess_ignore" not in option_exclude:
        option_exclude += ("subprocess_ignore",)
    elif "ignore" not in option_exclude:
        option_exclude += ("ignore",)

    option_exclude += ("python3_ignore",)
    option_exclude += ("SDL2_ignore",)

    main_dir, test_subdir, fake_test_subdir = prepare_test_env()

    ###########################################################################
    # Compile a list of test modules. If fake, then compile list of fake
    # xxxx_test.py from run_tests__tests

    TEST_MODULE_RE = re.compile(r"^(.+_test)\.py$")

    test_mods_pkg_name = test_pkg_name

    working_dir_temp = tempfile.mkdtemp()

    if option_fake is not None:
        test_mods_pkg_name = ".".join(
            [test_mods_pkg_name, "run_tests__tests", option_fake]
        )
        test_subdir = os.path.join(fake_test_subdir, option_fake)
        working_dir = test_subdir
    else:
        working_dir = working_dir_temp

    # Added in because some machines will need os.environ else there will be
    # false failures in subprocess mode. Same issue as python2.6. Needs some
    # env vars.

    test_env = os.environ

    fmt1 = "%s.%%s" % test_mods_pkg_name
    fmt2 = "%s.%%s_test" % test_mods_pkg_name
    if args:
        test_modules = [m.endswith("_test") and (fmt1 % m) or (fmt2 % m) for m in args]
    else:
        test_modules = []
        for f in sorted(os.listdir(test_subdir)):
            for match in TEST_MODULE_RE.findall(f):
                test_modules.append(fmt1 % (match,))

    ###########################################################################
    # Remove modules to be excluded.

    tmp = test_modules
    test_modules = []
    for name in tmp:
        tag_module_name = f"{name[0:-5]}_tags"
        try:
            tag_module = import_submodule(tag_module_name)
        except ImportError:
            test_modules.append(name)
        else:
            try:
                tags = tag_module.__tags__
            except AttributeError:
                print(f"{tag_module_name} has no tags: ignoring")
                test_modules.append(name)
            else:
                for tag in tags:
                    if tag in option_exclude:
                        print(f"skipping {name} (tag '{tag}')")
                        break
                else:
                    test_modules.append(name)
    del tmp, tag_module_name, name

    ###########################################################################
    # Meta results

    results = {}
    meta_results = {"__meta__": {}}
    meta = meta_results["__meta__"]

    ###########################################################################
    # Randomization

    if option_randomize or option_seed is not None:
        if option_seed is None:
            option_seed = time.time()
        meta["random_seed"] = option_seed
        print(f"\nRANDOM SEED USED: {option_seed}\n")
        random.seed(option_seed)
        random.shuffle(test_modules)

    ###########################################################################
    # Single process mode

    if not option_usesubprocess:
        options["exclude"] = option_exclude
        t = time.time()
        for module in test_modules:
            results.update(run_test(module, **options))
        t = time.time() - t

    ###########################################################################
    # Subprocess mode
    #

    else:
        if is_pygame_pkg:
            from pygame.tests.test_utils.async_sub import proc_in_time_or_kill
        else:
            from test.test_utils.async_sub import proc_in_time_or_kill

        pass_on_args = ["--exclude", ",".join(option_exclude)] + [
            "--" + field
            for field in ("randomize", "incomplete", "unbuffered", "verbosity")
            if kwds.get(field)
        ]

        def sub_test(module):
            print(f"loading {module}")

            cmd = [option_python, "-m", test_runner_mod, module] + pass_on_args

            return (
                module,
                (cmd, test_env, working_dir),
                proc_in_time_or_kill(
                    cmd, option_time_out, env=test_env, wd=working_dir
                ),
            )

        if option_multi_thread > 1:

            def tmap(f, args):
                return pygame.threads.tmap(
                    f, args, stop_on_error=False, num_workers=option_multi_thread
                )

        else:
            tmap = map

        t = time.time()

        for module, cmd, (return_code, raw_return) in tmap(sub_test, test_modules):
            test_file = f"{os.path.join(test_subdir, module)}.py"
            cmd, test_env, working_dir = cmd

            test_results = get_test_results(raw_return)
            if test_results:
                results.update(test_results)
            else:
                results[module] = {}

            results[module].update(
                {
                    "return_code": return_code,
                    "raw_return": raw_return,
                    "cmd": cmd,
                    "test_file": test_file,
                    "test_env": test_env,
                    "working_dir": working_dir,
                    "module": module,
                }
            )

        t = time.time() - t

    ###########################################################################
    # Output Results
    #

    untrusty_total, combined = combine_results(results, t)
    total, n_errors, n_failures = count_results(results)

    meta["total_tests"] = total
    meta["combined"] = combined
    meta["total_errors"] = n_errors
    meta["total_failures"] = n_failures
    results.update(meta_results)

    if not option_usesubprocess and total != untrusty_total:
        raise AssertionError(
            "Something went wrong in the Test Machinery:\n"
            "total: %d != untrusty_total: %d" % (total, untrusty_total)
        )

    if not option_dump:
        print(combined)
    else:
        print(TEST_RESULTS_START)
        print(pformat(results))

    if option_file is not None:
        results_file = open(option_file, "w")
        try:
            results_file.write(pformat(results))
        finally:
            results_file.close()

    shutil.rmtree(working_dir_temp)

    return total, n_errors + n_failures


def run(args):
    num_threads = args.thread_num if args.thread_num > 0 else psutil.cpu_count(logical=False)

    # Set OMP environment variable before importing onnxruntime. Needed for cpu only, and no impact for onnxruntime-gpu package.
    if "OMP_NUM_THREADS" not in os.environ:
        os.environ["OMP_NUM_THREADS"] = str(num_threads)

    from onnx import load  # noqa: PLC0415
    from onnx_model import OnnxModel  # noqa: PLC0415

    onnx_model = OnnxModel(load(args.model))

    all_inputs = None
    if args.dummy_inputs == "bert":
        all_inputs = create_bert_inputs(
            onnx_model,
            args.batch_size,
            args.sequence_length,
            args.samples,
            args.input_ids_name,
            args.segment_ids_name,
            args.input_mask_name,
        )
    elif args.dummy_inputs == "gpt2":
        all_inputs = create_gpt2_inputs(
            onnx_model,
            args.batch_size,
            args.sequence_length,
            args.past_sequence_length,
            args.samples,
        )
    elif args.dummy_inputs == "longformer":
        all_inputs = create_longformer_inputs(
            onnx_model,
            args.batch_size,
            args.sequence_length,
            args.global_length,
            args.samples,
        )
    else:  # default
        all_inputs = create_dummy_inputs(onnx_model, args.batch_size, args.sequence_length, args.samples)

    profile_file = run_profile(
        args.model,
        args.use_gpu,
        args.provider,
        args.basic_optimization,
        args.thread_num,
        all_inputs,
    )

    return profile_file


def run(args) -> list[dict[str, Any]]:
    torch.set_grad_enabled(False)

    # set random seed manually to get deterministic results
    benchmark_helper.set_random_seed(123)

    # Currently, the longformer attention operator could only run in GPU (no CPU implementation yet).
    device = torch.device("cuda:0")

    if args.memory:
        return [test_memory(args, device)]  # Convert to List so that return type is same as test_latency

    return test_latency(args, device)


def run():
    _path = os.getcwd()
    os.chdir(tempfile.gettempdir())
    print('------')
    print(f'os.name={os.name!r}')
    print('------')
    print(f'sys.platform={sys.platform!r}')
    print('------')
    print('sys.version:')
    print(sys.version)
    print('------')
    print('sys.prefix:')
    print(sys.prefix)
    print('------')
    print(f"sys.path={':'.join(sys.path)!r}")
    print('------')

    try:
        import numpy
        has_numpy = 1
    except ImportError as e:
        print('Failed to import numpy:', e)
        has_numpy = 0

    try:
        from numpy.f2py import f2py2e
        has_f2py2e = 1
    except ImportError as e:
        print('Failed to import f2py2e:', e)
        has_f2py2e = 0

    if has_numpy:
        try:
            print(f'Found numpy version {numpy.__version__!r} in {numpy.__file__}')
        except Exception as msg:
            print('error:', msg)
            print('------')

    if has_f2py2e:
        try:
            print(f'Found f2py2e version {f2py2e.__version__.version!r} in '
                  f'{f2py2e.__file__}')
        except Exception as msg:
            print('error:', msg)
            print('------')

    os.chdir(_path)


def run(arguments, content, options, state_machine, state, lineno):
    document = state_machine.document
    env = document.settings.env
    config = env.config
    nofigs = 'nofigs' in options

    if config.plot_srcset and setup.app.builder.name == 'singlehtml':
        raise ExtensionError(
            'plot_srcset option not compatible with single HTML writer')

    formats = get_plot_formats(config)
    default_fmt = formats[0][0]

    options.setdefault('include-source', config.plot_include_source)
    options.setdefault('show-source-link', config.plot_html_show_source_link)
    options.setdefault('filename-prefix', None)

    if 'class' in options:
        # classes are parsed into a list of string, and output by simply
        # printing the list, abusing the fact that RST guarantees to strip
        # non-conforming characters
        options['class'] = ['plot-directive'] + options['class']
    else:
        options.setdefault('class', ['plot-directive'])
    keep_context = 'context' in options
    context_opt = None if not keep_context else options['context']

    rst_file = document.attributes['source']
    rst_dir = os.path.dirname(rst_file)

    if len(arguments):
        if not config.plot_basedir:
            source_file_name = os.path.join(setup.app.builder.srcdir,
                                            directives.uri(arguments[0]))
        else:
            source_file_name = os.path.join(setup.confdir, config.plot_basedir,
                                            directives.uri(arguments[0]))
        # If there is content, it will be passed as a caption.
        caption = '\n'.join(content)

        # Enforce unambiguous use of captions.
        if "caption" in options:
            if caption:
                raise ValueError(
                    'Caption specified in both content and options.'
                    ' Please remove ambiguity.'
                )
            # Use caption option
            caption = options["caption"]

        # If the optional function name is provided, use it
        if len(arguments) == 2:
            function_name = arguments[1]
        else:
            function_name = None

        code = Path(source_file_name).read_text(encoding='utf-8')
        if options['filename-prefix']:
            output_base = options['filename-prefix']
            check_output_base_name(env, output_base)
        else:
            output_base = os.path.basename(source_file_name)
    else:
        source_file_name = rst_file
        code = textwrap.dedent("\n".join(map(str, content)))
        if options['filename-prefix']:
            output_base = options['filename-prefix']
            check_output_base_name(env, output_base)
        else:
            base, ext = os.path.splitext(os.path.basename(source_file_name))
            counter = document.attributes.get('_plot_counter', 0) + 1
            document.attributes['_plot_counter'] = counter
            output_base = '%s-%d.py' % (base, counter)
        function_name = None
        caption = options.get('caption', '')

    base, source_ext = os.path.splitext(output_base)
    if source_ext in ('.py', '.rst', '.txt'):
        output_base = base
    else:
        source_ext = ''

    # ensure that LaTeX includegraphics doesn't choke in foo.bar.pdf filenames
    output_base = output_base.replace('.', '-')

    # is it in doctest format?
    is_doctest = contains_doctest(code)
    if 'format' in options:
        if options['format'] == 'python':
            is_doctest = False
        else:
            is_doctest = True

    # determine output directory name fragment
    source_rel_name = relpath(source_file_name, setup.confdir)
    source_rel_dir = os.path.dirname(source_rel_name).lstrip(os.path.sep)

    # build_dir: where to place output files (temporarily)
    build_dir = os.path.join(os.path.dirname(setup.app.doctreedir),
                             'plot_directive',
                             source_rel_dir)
    # get rid of .. in paths, also changes pathsep
    # see note in Python docs for warning about symbolic links on Windows.
    # need to compare source and dest paths at end
    build_dir = os.path.normpath(build_dir)
    os.makedirs(build_dir, exist_ok=True)

    # how to link to files from the RST file
    try:
        build_dir_link = relpath(build_dir, rst_dir).replace(os.path.sep, '/')
    except ValueError:
        # on Windows, relpath raises ValueError when path and start are on
        # different mounts/drives
        build_dir_link = build_dir

    # get list of included rst files so that the output is updated when any
    # plots in the included files change. These attributes are modified by the
    # include directive (see the docutils.parsers.rst.directives.misc module).
    try:
        source_file_includes = [os.path.join(os.getcwd(), t[0])
                                for t in state.document.include_log]
    except AttributeError:
        # the document.include_log attribute only exists in docutils >=0.17,
        # before that we need to inspect the state machine
        possible_sources = {os.path.join(setup.confdir, t[0])
                            for t in state_machine.input_lines.items}
        source_file_includes = [f for f in possible_sources
                                if os.path.isfile(f)]
    # remove the source file itself from the includes
    try:
        source_file_includes.remove(source_file_name)
    except ValueError:
        pass

    # save script (if necessary)
    if options['show-source-link']:
        Path(build_dir, output_base + (source_ext or '.py')).write_text(
            doctest.script_from_examples(code)
            if source_file_name == rst_file and is_doctest
            else code,
            encoding='utf-8')

    # make figures
    try:
        results = render_figures(code=code,
                                 code_path=source_file_name,
                                 output_dir=build_dir,
                                 output_base=output_base,
                                 context=keep_context,
                                 function_name=function_name,
                                 config=config,
                                 context_reset=context_opt == 'reset',
                                 close_figs=context_opt == 'close-figs',
                                 code_includes=source_file_includes)
        errors = []
    except PlotError as err:
        reporter = state.memo.reporter
        sm = reporter.system_message(
            2, "Exception occurred in plotting {}\n from {}:\n{}".format(
                output_base, source_file_name, err),
            line=lineno)
        results = [(code, [])]
        errors = [sm]

    # Properly indent the caption
    if caption and config.plot_srcset:
        caption = ':caption: ' + caption.replace('\n', ' ')
    elif caption:
        caption = '\n' + '\n'.join('      ' + line.strip()
                                   for line in caption.split('\n'))
    # generate output restructuredtext
    total_lines = []
    for j, (code_piece, images) in enumerate(results):
        if options['include-source']:
            if is_doctest:
                lines = ['', *code_piece.splitlines()]
            else:
                lines = ['.. code-block:: python']
                if 'code-caption' in options:
                    code_caption = options['code-caption'].replace('\n', ' ')
                    lines.append(f'   :caption: {code_caption}')
                lines.extend(['', *textwrap.indent(code_piece, '    ').splitlines()])
            source_code = "\n".join(lines)
        else:
            source_code = ""

        if nofigs:
            images = []

        if 'alt' in options:
            options['alt'] = options['alt'].replace('\n', ' ')

        opts = [
            f':{key}: {val}' for key, val in options.items()
            if key in ('alt', 'height', 'width', 'scale', 'align', 'class')]

        # Not-None src_name signals the need for a source download in the
        # generated html
        if j == 0 and options['show-source-link']:
            src_name = output_base + (source_ext or '.py')
        else:
            src_name = None
        if config.plot_srcset:
            srcset = [*_parse_srcset(config.plot_srcset).values()]
            template = TEMPLATE_SRCSET
        else:
            srcset = None
            template = TEMPLATE

        result = jinja2.Template(config.plot_template or template).render(
            default_fmt=default_fmt,
            build_dir=build_dir_link,
            src_name=src_name,
            multi_image=len(images) > 1,
            options=opts,
            srcset=srcset,
            images=images,
            source_code=source_code,
            html_show_formats=config.plot_html_show_formats and len(images),
            caption=caption)
        total_lines.extend(result.split("\n"))
        total_lines.extend("\n")

    if total_lines:
        state_machine.insert_input(total_lines, source=source_file_name)

    return errors


def run(
    path: Optional[str] = typer.Argument(
        None,
        help=(
            "Path to a local folder containing an agent.json file or a built-in agent "
            "stored in the 'tiny-agents/tiny-agents' Hugging Face dataset "
            "(https://huggingface.co/datasets/tiny-agents/tiny-agents)"
        ),
        show_default=False,
    ),
):
    try:
        asyncio.run(run_agent(path))
    except KeyboardInterrupt:
        print(ANSI.red("\nApplication terminated by KeyboardInterrupt."), flush=True)
        raise typer.Exit(code=130)
    except Exception as e:
        print(ANSI.red(f"\nAn unexpected error occurred: {e}"), flush=True)
        raise e


def run(argv: List[Text]):
    # ------------------------------------------
    # argparse command line argument definitions
    # ------------------------------------------
    parser = argparse.ArgumentParser(
        description="An OpenType table diff tool for fonts."
    )
    parser.add_argument(
        "-l",
        "--summary",
        action="store_true",
        help="Report table presence and binary equality only",
    )
    parser.add_argument(
        "-U",
        "--lines",
        type=int,
        default=3,
        help="Number of context lines for unified diff (default: 3)",
    )
    parser.add_argument(
        "-t",
        "--include",
        type=str,
        nargs="+",
        default=None,
        help="Font tables to include. Multiple options are allowed.",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="+",
        default=None,
        help="Font tables to exclude. Multiple options are allowed.",
    )
    parser.add_argument(
        "--diff", type=str, help="Run external diff tool command (default: diff)"
    )
    parser.add_argument(
        "--diff-arg",
        type=str,
        default=None,
        help="External diff tool arguments (default: -u)",
    )
    parser.add_argument(
        "--color",
        choices=["auto", "never", "always"],
        default="auto",
        help="Whether to colorize output (default: auto)",
    )
    parser.add_argument(
        "--y1",
        type=int,
        default=-1,
        metavar="NUMBER",
        help="Select font number for TrueType Collection (.ttc/.otc) FILE1, starting from 0",
    )
    parser.add_argument(
        "--y2",
        type=int,
        default=-1,
        metavar="NUMBER",
        help="Select font number for TrueType Collection (.ttc/.otc) FILE2, starting from 0",
    )
    parser.add_argument(
        "-a",
        "--always",
        action="store_true",
        help="Compare tables even if binary identical",
    )
    parser.add_argument(
        "-b",
        "--binary",
        action="store_true",
        help="Compare tables only if binaries differ (default)",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress all output"
    )
    parser.add_argument("FILE1", help="Font file path 1")
    parser.add_argument("FILE2", help="Font file path 2")

    args: argparse.Namespace = parser.parse_args(argv)

    # /////////////////////////////////////////////////////////
    #
    #  Validations
    #
    # /////////////////////////////////////////////////////////

    # ----------------------------------
    #  Incompatible argument validations
    # ----------------------------------

    if args.always and args.binary:
        if not args.quiet:
            sys.stderr.write(
                f"[*] Error: --always and --binary are mutually exclusive options. "
                f"Please use ONLY one of these options in your command.{os.linesep}"
            )
        return 2
    if not args.always:
        args.binary = True

    # -------------------------------
    #  File path argument validations
    # -------------------------------

    if not file_exists(args.FILE1):
        if not args.quiet:
            sys.stderr.write(
                f"[*] ERROR: The file path '{args.FILE1}' can not be found.{os.linesep}"
            )
        return 2
    if not file_exists(args.FILE2):
        if not args.quiet:
            sys.stderr.write(
                f"[*] ERROR: The file path '{args.FILE2}' can not be found.{os.linesep}"
            )
        return 2

    # /////////////////////////////////////////////////////////
    #
    #  Command line logic
    #
    # /////////////////////////////////////////////////////////

    # parse explicitly included or excluded tables in
    # the command line arguments
    # set as a Python list if it was defined on the command line
    # or as None if it was not set on the command line
    include_list: Optional[List[Text]] = get_tables_argument_list(args.include)
    exclude_list: Optional[List[Text]] = get_tables_argument_list(args.exclude)

    if args.summary:
        try:
            identical, output = summarize(
                args.FILE1,
                args.FILE2,
                include_tables=include_list,
                exclude_tables=exclude_list,
                font_number_1=args.y1,
                font_number_2=args.y2,
            )
            if not args.quiet:
                sys.stdout.write(output)
            return 0 if identical else 1
        except Exception as e:
            if not args.quiet:
                sys.stderr.write(f"[*] ERROR: {e}{os.linesep}")
            return 2

    if args.binary:
        excluded_binary_tables = get_binary_exclude_tables(
            args.FILE1,
            args.FILE2,
            include_tables=include_list,
            exclude_tables=exclude_list,
            font_number_1=args.y1,
            font_number_2=args.y2,
        )
        if include_list is not None:
            include_list = [
                tag for tag in include_list if tag not in excluded_binary_tables
            ]
        else:
            if exclude_list is None:
                exclude_list = []
            exclude_list.extend(sorted(excluded_binary_tables))

    diff_tool = args.diff
    color_output = args.color == "always" or (
        args.color == "auto" and sys.stdout.isatty
    )

    if diff_tool is None:
        diff_tool = shutil.which("diff")
    elif diff_tool:
        diff_tool = shutil.which(diff_tool)
        if diff_tool is None:
            if not args.quiet:
                sys.stderr.write(
                    f"[*] ERROR: The external diff tool executable "
                    f"'{args.diff}' was not found.{os.linesep}"
                )
            return 2

    try:
        if diff_tool:
            diff_arg = args.diff_arg
            if diff_arg is None:
                if args.lines == 3:
                    diff_arg = ["-u"]
                else:
                    diff_arg = ["-u{}".format(args.lines)]
                if _is_gnu_diff(diff_tool):
                    diff_arg.append(r"-F^\s\s<")
            else:
                diff_arg = diff_arg.split()

            output = run_external_diff(
                diff_tool,
                diff_arg,
                args.FILE1,
                args.FILE2,
                include_tables=include_list,
                exclude_tables=exclude_list,
                font_number_a=args.y1,
                font_number_b=args.y2,
                use_multiprocess=True,
            )
        else:
            output = u_diff(
                args.FILE1,
                args.FILE2,
                context_lines=args.lines,
                include_tables=include_list,
                exclude_tables=exclude_list,
                font_number_a=args.y1,
                font_number_b=args.y2,
                use_multiprocess=True,
            )

        if color_output:
            output = [color_unified_diff_line(line) for line in output]

        output = "".join(output)
        if not args.quiet:
            pipe_output(output)
        return 1 if output else 0

    except Exception as e:
        if not args.quiet:
            sys.stderr.write(f"[*] ERROR: {e}{os.linesep}")
        return 2


def run(
    func: Callable[[Unpack[PosArgsT]], Awaitable[T_Retval]],
    *args: Unpack[PosArgsT],
    backend: str = "asyncio",
    backend_options: dict[str, Any] | None = None,
) -> T_Retval:
    """
    Run the given coroutine function in an asynchronous event loop.

    The current thread must not be already running an event loop.

    :param func: a coroutine function
    :param args: positional arguments to ``func``
    :param backend: name of the asynchronous event loop implementation – currently
        either ``asyncio`` or ``trio``
    :param backend_options: keyword arguments to call the backend ``run()``
        implementation with (documented :ref:`here <backend options>`)
    :return: the return value of the coroutine function
    :raises RuntimeError: if an asynchronous event loop is already running in this
        thread
    :raises LookupError: if the named backend is not found

    """
    if asynclib_name := current_async_library():
        raise RuntimeError(f"Already running {asynclib_name} in this thread")

    try:
        async_backend = get_async_backend(backend)
    except ImportError as exc:
        if backend in BACKENDS:
            raise LookupError(
                f"Backend {backend!r} is not available. "
                f"Install it with: pip install anyio[{backend}]"
            ) from exc

        raise LookupError(f"No such backend: {backend}") from exc

    token = None
    if asynclib_name is None:
        # Since we're in control of the event loop, we can cache the name of the async
        # library
        token = set_current_async_library(backend)

    try:
        backend_options = backend_options or {}
        return async_backend.run(func, args, {}, backend_options)
    finally:
        reset_current_async_library(token)

