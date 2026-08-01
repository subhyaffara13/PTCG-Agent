
def _main():
    """Parse options and run checks on Python source."""
    import signal

    # Handle "Broken pipe" gracefully
    try:
        signal.signal(signal.SIGPIPE, lambda signum, frame: sys.exit(1))
    except AttributeError:
        pass    # not supported on Windows

    style_guide = StyleGuide(parse_argv=True)
    options = style_guide.options

    report = style_guide.check_files()

    if options.statistics:
        report.print_statistics()

    if options.benchmark:
        report.print_benchmark()

    if report.total_errors:
        if options.count:
            sys.stderr.write(str(report.total_errors) + '\n')
        sys.exit(1)


def _main(
    self: click.Command,
    *,
    args: Sequence[str] | None = None,
    prog_name: str | None = None,
    complete_var: str | None = None,
    standalone_mode: bool = True,
    windows_expand_args: bool = True,
    rich_markup_mode: MarkupMode = DEFAULT_MARKUP_MODE,
    **extra: Any,
) -> Any:
    # Typer override, duplicated from click.main() to handle custom rich exceptions
    # Verify that the environment is configured correctly, or reject
    # further execution to avoid a broken script.
    if args is None:
        args = sys.argv[1:]

        # Covered in Click tests
        if os.name == "nt" and windows_expand_args:  # pragma: no cover
            args = click.utils._expand_args(args)
    else:
        args = list(args)

    if prog_name is None:
        prog_name = click.utils._detect_program_name()

    # Process shell completion requests and exit early.
    self._main_shell_completion(extra, prog_name, complete_var)

    try:
        try:
            with self.make_context(prog_name, args, **extra) as ctx:
                rv = self.invoke(ctx)
                if not standalone_mode:
                    return rv
                # it's not safe to `ctx.exit(rv)` here!
                # note that `rv` may actually contain data like "1" which
                # has obvious effects
                # more subtle case: `rv=[None, None]` can come out of
                # chained commands which all returned `None` -- so it's not
                # even always obvious that `rv` indicates success/failure
                # by its truthiness/falsiness
                ctx.exit()
        except EOFError as e:
            click.echo(file=sys.stderr)
            raise click.Abort() from e
        except KeyboardInterrupt as e:
            raise click.exceptions.Exit(130) from e
        except click.ClickException as e:
            if not standalone_mode:
                raise
            # Typer override
            if HAS_RICH and rich_markup_mode is not None:
                from . import rich_utils

                rich_utils.rich_format_error(e)
            else:
                e.show()
            # Typer override end
            sys.exit(e.exit_code)
        except OSError as e:
            if e.errno == errno.EPIPE:
                sys.stdout = cast(TextIO, click.utils.PacifyFlushWrapper(sys.stdout))
                sys.stderr = cast(TextIO, click.utils.PacifyFlushWrapper(sys.stderr))
                sys.exit(1)
            else:
                raise
    except click.exceptions.Exit as e:
        if standalone_mode:
            sys.exit(e.exit_code)
        else:
            # in non-standalone mode, return the exit code
            # note that this is only reached if `self.invoke` above raises
            # an Exit explicitly -- thus bypassing the check there which
            # would return its result
            # the results of non-standalone execution may therefore be
            # somewhat ambiguous: if there are codepaths which lead to
            # `ctx.exit(1)` and to `return 1`, the caller won't be able to
            # tell the difference between the two
            return e.exit_code
    except click.Abort:
        if not standalone_mode:
            raise
        # Typer override
        if HAS_RICH and rich_markup_mode is not None:
            from . import rich_utils

            rich_utils.rich_abort_error()
        else:
            click.echo(_("Aborted!"), file=sys.stderr)
        # Typer override end
        sys.exit(1)


def _main(config: Config, session: Session) -> int | ExitCode | None:
    """Default command line protocol for initialization, session,
    running tests and reporting."""
    config.hook.pytest_collection(session=session)
    config.hook.pytest_runtestloop(session=session)

    if session.testsfailed:
        return ExitCode.TESTS_FAILED
    elif session.testscollected == 0:
        return ExitCode.NO_TESTS_COLLECTED
    return None


def _main(
    *,
    args: list[str] | os.PathLike[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
    prog: str,
) -> int | ExitCode:
    # Handle a single `--version`/`-V` argument early to avoid starting up the entire pytest infrastructure.
    new_args = sys.argv[1:] if args is None else args
    if (
        isinstance(new_args, Sequence)
        and (new_args.count("--version") + new_args.count("-V")) == 1
    ):
        sys.stdout.write(f"pytest {__version__}\n")
        return ExitCode.OK

    old_pytest_version = os.environ.get("PYTEST_VERSION")
    try:
        os.environ["PYTEST_VERSION"] = __version__
        try:
            config = _prepareconfig(new_args, plugins, prog=prog)
        except ConftestImportFailure as e:
            print_conftest_import_error(e, file=sys.stderr)
            return ExitCode.USAGE_ERROR

        try:
            ret: ExitCode | int = config.hook.pytest_cmdline_main(config=config)
            try:
                return ExitCode(ret)
            except ValueError:
                return ret
        finally:
            config._ensure_unconfigure()
    except UsageError as e:
        print_usage_error(e, file=sys.stderr)
        return ExitCode.USAGE_ERROR
    finally:
        if old_pytest_version is None:
            os.environ.pop("PYTEST_VERSION", None)
        else:
            os.environ["PYTEST_VERSION"] = old_pytest_version


def _main(argv):
    """
    Run the PNG encoder with options from the command line.
    """

    # Parse command line arguments
    from optparse import OptionParser
    import re

    version = "%prog " + re.sub(r"( ?\$|URL: |Rev:)", "", __version__)
    parser = OptionParser(version=version)
    parser.set_usage("%prog [options] [imagefile]")
    parser.add_option(
        "-r",
        "--read-png",
        default=False,
        action="store_true",
        help="Read PNG, write PNM",
    )
    parser.add_option(
        "-i",
        "--interlace",
        default=False,
        action="store_true",
        help="create an interlaced PNG file (Adam7)",
    )
    parser.add_option(
        "-t",
        "--transparent",
        action="store",
        type="string",
        metavar="color",
        help="mark the specified colour (#RRGGBB) as transparent",
    )
    parser.add_option(
        "-b",
        "--background",
        action="store",
        type="string",
        metavar="color",
        help="save the specified background colour",
    )
    parser.add_option(
        "-a",
        "--alpha",
        action="store",
        type="string",
        metavar="pgmfile",
        help="alpha channel transparency (RGBA)",
    )
    parser.add_option(
        "-g",
        "--gamma",
        action="store",
        type="float",
        metavar="value",
        help="save the specified gamma value",
    )
    parser.add_option(
        "-c",
        "--compression",
        action="store",
        type="int",
        metavar="level",
        help="zlib compression level (0-9)",
    )
    parser.add_option(
        "-T",
        "--test",
        default=False,
        action="store_true",
        help="create a test image (a named PngSuite image if an argument is supplied)",
    )
    parser.add_option(
        "-L",
        "--list",
        default=False,
        action="store_true",
        help="print list of named test images",
    )
    parser.add_option(
        "-R",
        "--test-red",
        action="store",
        type="string",
        metavar="pattern",
        help="test pattern for the red image layer",
    )
    parser.add_option(
        "-G",
        "--test-green",
        action="store",
        type="string",
        metavar="pattern",
        help="test pattern for the green image layer",
    )
    parser.add_option(
        "-B",
        "--test-blue",
        action="store",
        type="string",
        metavar="pattern",
        help="test pattern for the blue image layer",
    )
    parser.add_option(
        "-A",
        "--test-alpha",
        action="store",
        type="string",
        metavar="pattern",
        help="test pattern for the alpha image layer",
    )
    parser.add_option(
        "-K",
        "--test-black",
        action="store",
        type="string",
        metavar="pattern",
        help="test pattern for greyscale image",
    )
    parser.add_option(
        "-d",
        "--test-depth",
        default=8,
        action="store",
        type="int",
        metavar="NBITS",
        help="create test PNGs that are NBITS bits per channel",
    )
    parser.add_option(
        "-S",
        "--test-size",
        action="store",
        type="int",
        metavar="size",
        help="width and height of the test image",
    )
    (options, args) = parser.parse_args(args=argv[1:])

    # Convert options
    if options.transparent is not None:
        options.transparent = color_triple(options.transparent)
    if options.background is not None:
        options.background = color_triple(options.background)

    if options.list:
        names = list(_pngsuite)
        names.sort()
        for name in names:
            print(name)
        return

    # Run regression tests
    if options.test:
        return test_suite(options, args)

    # Prepare input and output files
    if len(args) == 0:
        infilename = "-"
        infile = sys.stdin
    elif len(args) == 1:
        infilename = args[0]
        infile = open(infilename, "rb")
    else:
        parser.error("more than one input file")
    outfile = sys.stdout

    if options.read_png:
        # Encode PNG to PPM
        png = Reader(file=infile)
        width, height, pixels, meta = png.asDirect()
        write_pnm(outfile, width, height, pixels, meta)
    else:
        # Encode PNM to PNG
        format, width, height, depth, maxval = read_pnm_header(
            infile, ("P5", "P6", "P7")
        )
        # When it comes to the variety of input formats, we do something
        # rather rude.  Observe that L, LA, RGB, RGBA are the 4 colour
        # types supported by PNG and that they correspond to 1, 2, 3, 4
        # channels respectively.  So we use the number of channels in
        # the source image to determine which one we have.  We do not
        # care about TUPLTYPE.
        greyscale = depth <= 2
        pamalpha = depth in (2, 4)
        supported = (2**x - 1 for x in range(1, 17))
        try:
            mi = supported.index(maxval)
        except ValueError:
            raise NotImplementedError(
                f"your maxval ({maxval}) not in supported list {str(supported)}"
            )
        bitdepth = mi + 1
        writer = Writer(
            width,
            height,
            greyscale=greyscale,
            bitdepth=bitdepth,
            interlace=options.interlace,
            transparent=options.transparent,
            background=options.background,
            alpha=bool(pamalpha or options.alpha),
            gamma=options.gamma,
            compression=options.compression,
        )
        if options.alpha:
            pgmfile = open(options.alpha, "rb")
            format, awidth, aheight, adepth, amaxval = read_pnm_header(pgmfile, "P5")
            if amaxval != "255":
                raise NotImplementedError(
                    f"maxval {amaxval} not supported for alpha channel"
                )
            if (awidth, aheight) != (width, height):
                raise ValueError(
                    "alpha channel image size mismatch"
                    " (%s has %sx%s but %s has %sx%s)"
                    % (infilename, width, height, options.alpha, awidth, aheight)
                )
            writer.convert_ppm_and_pgm(infile, pgmfile, outfile)
        else:
            writer.convert_pnm(infile, outfile)


def _main(argv, shard_main):
  # TODO(emilyaf): Enable multiprocess tests on Windows.
  if sys.platform == "win32":
    print("Multiprocess tests are not supported on Windows.")
    return
  num_processes = NUM_PROCESSES.value
  if MULTIPROCESS_TEST_WORKER_ID.value >= 0:
    local_device_ids = _DEVICE_IDS.value
    if local_device_ids is not None:
      local_device_ids = [int(device_id) for device_id in local_device_ids]
    distributed.initialize(
        _MULTIPROCESS_TEST_CONTROLLER_ADDRESS.value,
        num_processes=num_processes,
        process_id=MULTIPROCESS_TEST_WORKER_ID.value,
        local_device_ids=local_device_ids,
        heartbeat_timeout_seconds=_HEARTBEAT_TIMEOUT.value,
        shutdown_timeout_seconds=_SHUTDOWN_TIMEOUT.value,
        initialization_timeout=_INITIALIZATION_TIMEOUT.value,
    )
    if shard_main is not None:
      return shard_main()
    return absltest.main(testLoader=jtu.JaxTestLoader())

  if not argv[0].endswith(".py"):  # Skip the interpreter path if present.
    argv = argv[1:]

  if num_processes is None:
    raise ValueError("num_processes must be set")
  gpus_per_process = _GPUS_PER_PROCESS.value
  tpu_chips_per_process = _TPU_CHIPS_PER_PROCESS.value
  num_tpu_chips = num_processes * tpu_chips_per_process
  if num_tpu_chips == 0:
    tpu_host_bounds = ""
    tpu_chips_per_host_bounds = ""
  elif num_tpu_chips == 1:
    assert tpu_chips_per_process == 1
    tpu_host_bounds = "1,1,1"
    tpu_chips_per_host_bounds = "1,1,1"
  elif num_tpu_chips == 4:
    if tpu_chips_per_process == 1:
      tpu_host_bounds = "2,2,1"
      tpu_chips_per_host_bounds = "1,1,1"
    elif tpu_chips_per_process == 2:
      tpu_host_bounds = "2,1,1"
      tpu_chips_per_host_bounds = "1,2,1"
    elif tpu_chips_per_process == 4:
      tpu_host_bounds = "1,1,1"
      tpu_chips_per_host_bounds = "2,2,1"
    else:
      raise ValueError(
          "Invalid number of TPU chips per worker {}".format(
              tpu_chips_per_process
          )
      )
  elif num_tpu_chips == 8:
    if tpu_chips_per_process == 1:
      tpu_host_bounds = "4,2,1"
      tpu_chips_per_host_bounds = "1,1,1"
    elif tpu_chips_per_process == 4:
      # Note: this branch assumes we are using 2x4 v6e LitePod, and will not
      # work with 4x2 v5e LitePod.
      tpu_host_bounds = "1,2,1"
      tpu_chips_per_host_bounds = "2,2,1"
    elif tpu_chips_per_process == 8:
      tpu_host_bounds = "1,1,1"
      tpu_chips_per_host_bounds = "2,4,1"
    else:
      # TODO(phawkins): implement other cases.
      raise ValueError(
          "Invalid number of TPU chips per worker {}".format(
              tpu_chips_per_process
          )
      )
  else:
    raise ValueError(f"Invalid number of TPU chips {num_tpu_chips}")

  if portpicker is None:
    slicebuilder_ports = [10000 + i for i in range(num_processes)]
  else:
    slicebuilder_ports = [
        portpicker.pick_unused_port() for _ in range(num_processes)
    ]
  slicebuilder_addresses = ",".join(
      f"localhost:{port}" for port in slicebuilder_ports
  )
  megascale_coordinator_port = None

  if gpus_per_process > 0:
    # Get the number of GPUs visible to this process without initializing the runtime
    if cuda_versions is not None:
      local_device_count = cuda_versions.cuda_device_count()
      if num_processes * gpus_per_process > local_device_count:
        print(
          f"Cannot run {num_processes} processes with {gpus_per_process} GPU(s) "
          f"each on a system with only {local_device_count} local GPU(s), "
          f"starting {local_device_count // gpus_per_process} instead - test "
          "cases will likely be skipped!"
        )
        num_processes = local_device_count // gpus_per_process

  if portpicker is None:
    jax_port = 9876
  else:
    # TODO(emilyaf): Use a port server if there are flaky port collisions due
    # to pick_unused_port() racing among tests.
    jax_port = portpicker.pick_unused_port()
  subprocesses = []
  output_filenames = []
  output_files = []
  sys_path = os.pathsep.join(sys.path)

  for i in range(num_processes):
    device_ids = None
    env = os.environ.copy()

    # Note: Fix for rules_python >= 1.7.0 (Strict Hermeticity):
    # The parent process sees dependencies via sys.path, but modern rules_python
    # does not export this to PYTHONPATH by default. We must manually propagate
    # it so child workers can locate dependencies.
    path_parts = [sys_path, env.get("PYTHONPATH", "")]
    env["PYTHONPATH"] = os.pathsep.join(p for p in path_parts if p)

    args = [
        "/proc/self/exe",
        *argv,
        f"--num_processes={num_processes}",
        f"--multiprocess_test_worker_id={i}",
        f"--multiprocess_test_controller_address=localhost:{jax_port}",
        f"--heartbeat_timeout={_HEARTBEAT_TIMEOUT.value}",
        f"--shutdown_timeout={_SHUTDOWN_TIMEOUT.value}",
        f"--barrier_timeout={_BARRIER_TIMEOUT.value}",
        f"--initialization_timeout={_INITIALIZATION_TIMEOUT.value}",
        "--logtostderr",
    ]

    if num_tpu_chips > 0:
      device_ids = range(
          i * tpu_chips_per_process, (i + 1) * tpu_chips_per_process)
      env["CLOUD_TPU_TASK_ID"] = str(i)
      env["TPU_CHIPS_PER_PROCESS_BOUNDS"] = tpu_chips_per_host_bounds
      env["TPU_PROCESS_BOUNDS"] = tpu_host_bounds
      env["TPU_PROCESS_ADDRESSES"] = slicebuilder_addresses
      env["TPU_PROCESS_PORT"] = str(slicebuilder_ports[i])
      env["TPU_VISIBLE_CHIPS"] = ",".join(map(str, device_ids))
      env["ALLOW_MULTIPLE_LIBTPU_LOAD"] = "1"

    if gpus_per_process > 0:
      device_ids = range(i * gpus_per_process, (i + 1) * gpus_per_process)
      args.append(f"--jax_cuda_visible_devices={','.join(map(str, device_ids))}")

    if device_ids is not None:
      args.append(f"--device_ids={','.join(map(str, device_ids))}")

    cpu_collectives_impl = CPU_COLLECTIVES_IMPLEMENTATION.value
    if cpu_collectives_impl:
      args.append(
          f"--jax_cpu_collectives_implementation={cpu_collectives_impl}"
      )

    if _ENABLE_MEGASCALE.value or cpu_collectives_impl == "megascale":
      if portpicker is None:
        megascale_port = 9877
      else:
        megascale_port = portpicker.pick_unused_port()
      if megascale_coordinator_port is None:
        megascale_coordinator_port = megascale_port
      args += [
          f"--megascale_coordinator_address=localhost:{megascale_coordinator_port}",
          f"--megascale_port={megascale_port}",
      ]

    args += EXTRA_TEST_ARGS.value

    undeclared_outputs = os.environ.get("TEST_UNDECLARED_OUTPUTS_DIR", "/tmp")
    stdout_name = f"{undeclared_outputs}/jax_{i}_stdout.log"
    stderr_name = f"{undeclared_outputs}/jax_{i}_stderr.log"

    if _DUMP_HLO.value:
      hlo_dump_path = f"{undeclared_outputs}/jax_{i}_hlo_dump/"
      os.makedirs(hlo_dump_path, exist_ok=True)
      env["XLA_FLAGS"] = f"--xla_dump_to={hlo_dump_path}"

    stdout = open(stdout_name, "wb")
    stderr = open(stderr_name, "wb")
    print(f"Launching process {i}:")
    print(f"  stdout: {stdout_name}")
    print(f"  stderr: {stderr_name}")
    proc = subprocess.Popen(args, env=env, stdout=stdout, stderr=stderr)
    subprocesses.append(proc)
    output_filenames.append((stdout_name, stderr_name))
    output_files.append((stdout, stderr))

  print(" All launched, running ".center(80, "="), flush=True)

  # Wait for all the children to finish or for a SIGTERM from bazel. If we get
  # SIGTERM, we still want to collect their logs, so kill them and continue.
  killer = GracefulKiller()
  running_procs = dict(enumerate(subprocesses))
  while not killer.kill_now and running_procs:
    time.sleep(0.1)
    for i, proc in list(running_procs.items()):
      if proc.poll() is not None:
        print(f"Process {i} finished.", flush=True)
        running_procs.pop(i)
  if killer.kill_now and running_procs:
    print("Caught termination, terminating remaining children.", flush=True)

    # Send a SIGTERM to each child process, to let it know it should terminate.
    for i, proc in running_procs.items():
      proc.terminate()
      print(f"Process {i} terminated.", flush=True)

    # We give the child process(es) a few seconds for their own cleanup, and
    # keep the rest (up to 15s) for copying the children logs into our own.
    time.sleep(5)

    # Send a SIGKILL (a "hard" kill) to each child process. This is CRITICAL:
    # without it, this process may end up waiting a long time on the proc.wait()
    # below, and never get to saving the children logs, making test timeouts
    # very hard to debug.
    for i, proc in running_procs.items():
      proc.kill()
      print(f"Process {i} killed.")
    print("Killed all child processes.", flush=True)

  retvals = []
  stdouts = []
  stderrs = []
  for proc, fds, (stdout, stderr) in zip(
      subprocesses, output_files, output_filenames
  ):
    retvals.append(proc.wait())
    for fd in fds:
      fd.close()
    stdouts.append(pathlib.Path(stdout).read_text(errors="replace"))
    stderrs.append(pathlib.Path(stderr).read_text(errors="replace"))

  print(" All finished ".center(80, "="), flush=True)

  print(" Summary ".center(80, "="))
  for i, (retval, stdout, stderr) in enumerate(zip(retvals, stdouts, stderrs)):
    m = re.search(r"Ran \d+ tests? in [\d.]+s\n\n.*", stderr, re.MULTILINE)
    result = m.group().replace("\n\n", "; ") if m else "Test crashed?"
    print(
        f"Process {i}, ret: {retval}, len(stdout): {len(stdout)}, "
        f"len(stderr): {len(stderr)}; {result}"
    )

  print(" Detailed logs ".center(80, "="))
  for i, (retval, stdout, stderr) in enumerate(zip(retvals, stdouts, stderrs)):
    print(f" Process {i}: return code: {retval} ".center(80, "="))
    if stdout:
      print(f" Process {i} stdout ".center(80, "-"))
      print(stdout)
    if stderr:
      print(f" Process {i} stderr ".center(80, "-"))
      print(stderr)

  print(" Done detailed logs ".center(80, "="), flush=True)
  for i, (retval, stderr) in enumerate(zip(retvals, stderrs)):
    if retval != 0:
      if expect_failures_with_regex is not None:
        assert re.search(
            expect_failures_with_regex, stderr
        ), f"process {i} failed, expected regex: {expect_failures_with_regex}"
      else:
        assert retval == 0, f"process {i} failed, return value: {retval}"


def _main(args=None):
    """Convert a UFO font from cubic to quadratic curves"""
    parser = argparse.ArgumentParser(prog="cu2qu")
    parser.add_argument("--version", action="version", version=fontTools.__version__)
    parser.add_argument(
        "infiles",
        nargs="+",
        metavar="INPUT",
        help="one or more input UFO source file(s).",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-e",
        "--conversion-error",
        type=float,
        metavar="ERROR",
        default=None,
        help="maximum approximation error measured in EM (default: 0.001)",
    )
    parser.add_argument(
        "-m",
        "--mixed",
        default=False,
        action="store_true",
        help="whether to used mixed quadratic and cubic curves",
    )
    parser.add_argument(
        "--keep-direction",
        dest="reverse_direction",
        action="store_false",
        help="do not reverse the contour direction",
    )

    mode_parser = parser.add_mutually_exclusive_group()
    mode_parser.add_argument(
        "-i",
        "--interpolatable",
        action="store_true",
        help="whether curve conversion should keep interpolation compatibility",
    )
    mode_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        nargs="?",
        default=1,
        const=_cpu_count(),
        metavar="N",
        help="convert using N multiple processes (default: %(default)s)",
    )

    output_parser = parser.add_mutually_exclusive_group()
    output_parser.add_argument(
        "-o",
        "--output-file",
        default=None,
        metavar="OUTPUT",
        help=(
            "output filename for the converted UFO. By default fonts are "
            "modified in place. This only works with a single input."
        ),
    )
    output_parser.add_argument(
        "-d",
        "--output-dir",
        default=None,
        metavar="DIRECTORY",
        help="output directory where to save converted UFOs",
    )

    options = parser.parse_args(args)

    if ufo_module is None:
        parser.error("Either ufoLib2 or defcon are required to run this script.")

    if not options.verbose:
        level = "WARNING"
    elif options.verbose == 1:
        level = "INFO"
    else:
        level = "DEBUG"
    logging.basicConfig(level=level)

    if len(options.infiles) > 1 and options.output_file:
        parser.error("-o/--output-file can't be used with multile inputs")

    if options.output_dir:
        output_dir = options.output_dir
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        elif not os.path.isdir(output_dir):
            parser.error("'%s' is not a directory" % output_dir)
        output_paths = [
            os.path.join(output_dir, os.path.basename(p)) for p in options.infiles
        ]
    elif options.output_file:
        output_paths = [options.output_file]
    else:
        # save in-place
        output_paths = [None] * len(options.infiles)

    kwargs = dict(
        dump_stats=options.verbose > 0,
        max_err_em=options.conversion_error,
        reverse_direction=options.reverse_direction,
        all_quadratic=False if options.mixed else True,
    )

    if options.interpolatable:
        logger.info("Converting curves compatibly")
        ufos = [open_ufo(infile) for infile in options.infiles]
        if fonts_to_quadratic(ufos, **kwargs):
            for ufo, output_path in zip(ufos, output_paths):
                logger.info("Saving %s", output_path)
                if output_path:
                    ufo.save(output_path)
                else:
                    ufo.save()
        else:
            for input_path, output_path in zip(options.infiles, output_paths):
                if output_path:
                    _copytree(input_path, output_path)
    else:
        jobs = min(len(options.infiles), options.jobs) if options.jobs > 1 else 1
        if jobs > 1:
            func = partial(_font_to_quadratic, **kwargs)
            logger.info("Running %d parallel processes", jobs)
            with closing(mp.Pool(jobs)) as pool:
                pool.starmap(func, zip(options.infiles, output_paths))
        else:
            for input_path, output_path in zip(options.infiles, output_paths):
                _font_to_quadratic(input_path, output_path, **kwargs)


def _main(args=None):
    """Convert an OpenType font from quadratic to cubic curves"""
    parser = argparse.ArgumentParser(prog="qu2cu")
    parser.add_argument("--version", action="version", version=fontTools.__version__)
    parser.add_argument(
        "infiles",
        nargs="+",
        metavar="INPUT",
        help="one or more input TTF source file(s).",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-e",
        "--conversion-error",
        type=float,
        metavar="ERROR",
        default=0.001,
        help="maxiumum approximation error measured in EM (default: 0.001)",
    )
    parser.add_argument(
        "-c",
        "--all-cubic",
        default=False,
        action="store_true",
        help="whether to only use cubic curves",
    )

    output_parser = parser.add_mutually_exclusive_group()
    output_parser.add_argument(
        "-o",
        "--output-file",
        default=None,
        metavar="OUTPUT",
        help=("output filename for the converted TTF."),
    )
    output_parser.add_argument(
        "-d",
        "--output-dir",
        default=None,
        metavar="DIRECTORY",
        help="output directory where to save converted TTFs",
    )

    options = parser.parse_args(args)

    if options.conversion_error <= 0:
        parser.error("--conversion-error must be greater than zero")

    if not options.verbose:
        level = "WARNING"
    elif options.verbose == 1:
        level = "INFO"
    else:
        level = "DEBUG"
    logging.basicConfig(level=level)

    if len(options.infiles) > 1 and options.output_file:
        parser.error("-o/--output-file can't be used with multile inputs")

    if options.output_dir:
        output_dir = options.output_dir
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        elif not os.path.isdir(output_dir):
            parser.error("'%s' is not a directory" % output_dir)
        output_paths = [
            os.path.join(output_dir, os.path.basename(p)) for p in options.infiles
        ]
    elif options.output_file:
        output_paths = [options.output_file]
    else:
        output_paths = [
            makeOutputFileName(p, overWrite=True, suffix=".cubic")
            for p in options.infiles
        ]

    kwargs = dict(
        dump_stats=options.verbose > 0,
        max_err_em=options.conversion_error,
        all_cubic=options.all_cubic,
    )

    for input_path, output_path in zip(options.infiles, output_paths):
        _font_to_cubic(input_path, output_path, **kwargs)

