
def run_test(ir, inputs, *, warmup_runs=10, test_runs=20) -> float:
    graph, _ = load_graph_and_inputs(ir)
    for _ in range(warmup_runs):
        graph(*inputs)

    is_cpu = None
    for input in inputs:
        if isinstance(input, torch.Tensor):
            is_cpu = input.device.type == "cpu"
            break
    if is_cpu is None:
        raise AssertionError("No tensor found in inputs")

    out = time_cpu(graph, inputs, test_runs) if is_cpu else time_cuda(graph, inputs, test_runs)
    return out


def run_test(label, routines, numerical_tests, language, commands, friendly=True):
    """A driver for the codegen tests.

       This driver assumes that a compiler ifort is present in the PATH and that
       ifort is (at least) a Fortran 90 compiler. The generated code is written in
       a temporary directory, together with a main program that validates the
       generated code. The test passes when the compilation and the validation
       run correctly.
    """

    # Check input arguments before touching the file system
    language = language.upper()
    assert language in main_template
    assert language in numerical_test_template

    # Check that environment variable makes sense
    clean = os.getenv('SYMPY_TEST_CLEAN_TEMP', 'always').lower()
    if clean not in ('always', 'success', 'never'):
        raise ValueError("SYMPY_TEST_CLEAN_TEMP must be one of the following: 'always', 'success' or 'never'.")

    # Do all the magic to compile, run and validate the test code
    # 1) prepare the temporary working directory, switch to that dir
    work = tempfile.mkdtemp("_sympy_%s_test" % language, "%s_" % label)
    oldwork = os.getcwd()
    os.chdir(work)

    # 2) write the generated code
    if friendly:
        # interpret the routines as a name_expr list and call the friendly
        # function codegen
        codegen(routines, language, "codegen", to_files=True)
    else:
        code_gen = get_code_generator(language, "codegen")
        code_gen.write(routines, "codegen", to_files=True)

    # 3) write a simple main program that links to the generated code, and that
    #    includes the numerical tests
    test_strings = []
    for fn_name, args, expected, threshold in numerical_tests:
        call_string = "%s(%s)-(%s)" % (
            fn_name, ",".join(str(arg) for arg in args), expected)
        if language == "F95":
            call_string = fortranize_double_constants(call_string)
            threshold = fortranize_double_constants(str(threshold))
        test_strings.append(numerical_test_template[language] % {
            "call": call_string,
            "threshold": threshold,
        })

    if language == "F95":
        f_name = "main.f90"
    elif language.startswith("C"):
        f_name = "main.c"
    else:
        raise NotImplementedError(
            "FIXME: filename extension unknown for language: %s" % language)

    Path(f_name).write_text(
        main_template[language] % {'statements': "".join(test_strings)})

    # 4) Compile and link
    compiled = try_run(commands)

    # 5) Run if compiled
    if compiled:
        executed = try_run(["./test.exe"])
    else:
        executed = False

    # 6) Clean up stuff
    if clean == 'always' or (clean == 'success' and compiled and executed):
        def safe_remove(filename):
            if os.path.isfile(filename):
                os.remove(filename)
        safe_remove("codegen.f90")
        safe_remove("codegen.c")
        safe_remove("codegen.h")
        safe_remove("codegen.o")
        safe_remove("main.f90")
        safe_remove("main.c")
        safe_remove("main.o")
        safe_remove("test.exe")
        os.chdir(oldwork)
        os.rmdir(work)
    else:
        print("TEST NOT REMOVED: %s" % work, file=sys.stderr)
        os.chdir(oldwork)

    # 7) Do the assertions in the end
    assert compiled, "failed to compile %s code with:\n%s" % (
        language, "\n".join(commands))
    assert executed, "failed to execute %s code from:\n%s" % (
        language, "\n".join(commands))


def run_test(test, args=(), test_atol=1e-5, n=100, iters=None,
             callback=None, minimizer_kwargs=None, options=None,
             sampling_method='sobol', workers=1):
    res = shgo(test.f, test.bounds, args=args, constraints=test.cons,
               n=n, iters=iters, callback=callback,
               minimizer_kwargs=minimizer_kwargs, options=options,
               sampling_method=sampling_method, workers=workers)

    print(f'res = {res}')
    logging.info(f'res = {res}')
    if test.expected_x is not None:
        np.testing.assert_allclose(res.x, test.expected_x,
                                   rtol=test_atol,
                                   atol=test_atol)

    # (Optional tests)
    if test.expected_fun is not None:
        np.testing.assert_allclose(res.fun,
                                   test.expected_fun,
                                   atol=test_atol)

    if test.expected_xl is not None:
        np.testing.assert_allclose(res.xl,
                                   test.expected_xl,
                                   atol=test_atol)

    if test.expected_funl is not None:
        np.testing.assert_allclose(res.funl,
                                   test.expected_funl,
                                   atol=test_atol)
    return


def run_test(
    module,
    incomplete=False,
    usesubprocess=True,
    randomize=False,
    exclude=("interactive",),
    buffer=True,
    unbuffered=None,
    verbosity=1,
):
    """Run a unit test module"""
    suite = unittest.TestSuite()

    if verbosity is None:
        verbosity = 1

    if verbosity:
        print(f"loading {module}")

    loader = PygameTestLoader(
        randomize_tests=randomize, include_incomplete=incomplete, exclude=exclude
    )
    suite.addTest(loader.loadTestsFromName(module))

    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output, buffer=buffer, verbosity=verbosity)
    results = runner.run(suite)

    if verbosity == 2:
        output.seek(0)
        print(output.read())
        output.seek(0)

    results = {
        module: {
            "output": output.getvalue(),
            "num_tests": results.testsRun,
            "num_errors": len(results.errors),
            "num_failures": len(results.failures),
        }
    }

    if usesubprocess:
        print(TEST_RESULTS_START)
        print(pformat(results))
        print(TEST_RESULTS_END)
    else:
        return results


def run_test(
    baseline_model,
    optimized_model,
    output_dir,
    batch_size,
    sequence_length,
    use_gpu,
    test_cases,
    seed,
    verbose,
    rtol,
    atol,
    input_ids_name,
    segment_ids_name,
    input_mask_name,
    mask_type,
    dictionary_size: int = 1024,
):
    # Try deduce input names from optimized model.
    input_ids, segment_ids, input_mask = get_bert_inputs(
        optimized_model, input_ids_name, segment_ids_name, input_mask_name
    )

    # Use random mask length for accuracy test. It might introduce slight inflation in latency reported in this script.
    average_sequence_length = int(sequence_length / 2) if sequence_length >= 2 else sequence_length
    all_inputs = generate_test_data(
        batch_size,
        sequence_length,
        test_cases,
        seed,
        verbose,
        input_ids,
        segment_ids,
        input_mask,
        average_sequence_length,
        True,  # random sequence length
        mask_type,
        dictionary_size=dictionary_size,
    )

    baseline_results, baseline_latency, output_names = run_model(
        baseline_model, all_inputs, use_gpu, disable_optimization=True
    )
    if verbose:
        print(f"baseline average latency (all optimizations disabled): {statistics.mean(baseline_latency) * 1000} ms")

    if output_dir is not None:
        for i, inputs in enumerate(all_inputs):
            output_test_data(output_dir, i, inputs)

    treatment_results, treatment_latency, treatment_output_names = run_model(
        optimized_model, all_inputs, use_gpu, disable_optimization=False
    )
    if verbose:
        print(f"treatment average latency: {statistics.mean(treatment_latency) * 1000} ms")

    # Validate the output of baseline and treatment, to make sure the results are similar.
    return compare(baseline_results, treatment_results, verbose, rtol, atol)


def run_test(
    args: argparse.Namespace,
    csv_writer: csv.DictWriter | None = None,
):
    use_gpu: bool = args.use_gpu
    enable_cuda_graph: bool = args.use_cuda_graph
    repeats: int = args.repeats

    if use_gpu:
        device_id = torch.cuda.current_device()
        device = torch.device("cuda", device_id)
        provider = "CUDAExecutionProvider"
    else:
        device_id = 0
        device = torch.device("cpu")
        enable_cuda_graph = False
        provider = "CPUExecutionProvider"

    dtypes = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}
    config = TestConfig(
        model_type=args.model_type,
        onnx_path=args.onnx_path,
        sam2_dir=args.sam2_dir,
        component=args.component,
        provider=provider,
        batch_size=args.batch_size,
        height=args.height,
        width=args.width,
        device=device,
        use_tf32=True,
        enable_cuda_graph=enable_cuda_graph,
        dtype=dtypes[args.dtype],
        prefer_nhwc=args.prefer_nhwc,
        repeats=args.repeats,
        warm_up=args.warm_up,
        enable_nvtx_profile=args.enable_nvtx_profile,
        enable_ort_profile=args.enable_ort_profile,
        enable_torch_profile=args.enable_torch_profile,
        torch_compile_mode=args.torch_compile_mode,
        verbose=False,
    )

    if args.engine == "ort":
        sess_options = SessionOptions()
        sess_options.intra_op_num_threads = args.intra_op_num_threads
        if config.enable_ort_profile:
            sess_options.enable_profiling = True
            sess_options.log_severity_level = 4
            sess_options.log_verbosity_level = 0

        session = create_session(config, sess_options)
        input_dict = config.random_inputs()

        # warm up session
        try:
            for _ in range(config.warm_up):
                _ = measure_latency(session, input_dict)
        except Exception as e:
            print(f"Failed to run {config=}. Exception: {e}")
            return

        if config.enable_nvtx_profile:
            import nvtx  # noqa: PLC0415
            from cuda import cudart  # noqa: PLC0415

            cudart.cudaProfilerStart()
            with nvtx.annotate("one_run"):
                _ = session.infer(input_dict)
            cudart.cudaProfilerStop()

        if config.enable_ort_profile:
            session.ort_session.end_profiling()

        if repeats == 0:
            return

        latency_list = []
        for _ in range(repeats):
            latency = measure_latency(session, input_dict)
            latency_list.append(latency)
        average_latency = statistics.mean(latency_list)

        del session
    else:  # torch
        with torch.no_grad():
            try:
                average_latency = run_torch(config)
            except Exception as e:
                print(f"Failed to run {config=}. Exception: {e}")
                return

        if repeats == 0:
            return

    engine = args.engine + ":" + ("cuda" if use_gpu else "cpu")
    row = {
        "model_type": args.model_type,
        "component": args.component,
        "dtype": args.dtype,
        "use_gpu": use_gpu,
        "enable_cuda_graph": enable_cuda_graph,
        "prefer_nhwc": config.prefer_nhwc,
        "use_tf32": config.use_tf32,
        "batch_size": args.batch_size,
        "height": args.height,
        "width": args.width,
        "multi_mask_output": args.multimask_output,
        "num_labels": config.num_labels,
        "num_points": config.num_points,
        "num_masks": config.num_masks,
        "intra_op_num_threads": args.intra_op_num_threads,
        "warm_up": config.warm_up,
        "repeats": repeats,
        "enable_nvtx_profile": args.enable_nvtx_profile,
        "torch_compile_mode": args.torch_compile_mode,
        "engine": engine,
        "average_latency": average_latency,
    }

    if csv_writer is not None:
        csv_writer.writerow(row)

    print(f"{vars(config)}")
    print(f"{row}")

