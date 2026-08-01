
def run_model(
    model_base, model_control, model_input, num_iterations=10, precision=1e-4
):
    clean_memory()
    for i in range(num_iterations):
        logger.info("start %s iteration", i)
        set_deterministic()
        pred_base = model_base(*model_input)
        set_deterministic()
        pred_control = model_control(*model_input)

        res = compare_parameters(model_base, model_control, precision)
        logger.info("compare parameters. Numerical result : %s", res)

        res = compare_forward_output(pred_base, pred_control, precision)
        logger.info("compare loss/predict. Numerical result : %s", res)
        # tensor may not have a grad_fn
        try:
            _ = pred_base[0].sum().backward(retain_graph=True)
            _ = pred_control[0].sum().backward(retain_graph=True)
            res = compare_gradients(model_base, model_control, precision)
            logger.info("compare param grad. Numerical result : %s", res)
        except Exception:
            logger.exception("Exception when comparing gradients")
            traceback.print_exc()

        if config.fx_passes_numeric_check["requires_optimizer"]:
            try:
                optimizer_base = optim.SGD(
                    [param for name, param in model_base.named_parameters()], lr=0.01
                )
                optimizer_base.step()

                optimizer_control = optim.SGD(
                    [param for name, param in model_control.named_parameters()], lr=0.01
                )
                optimizer_control.step()

                res = compare_parameters(model_base, model_control, precision)
                logger.info(
                    "compare parameters with optimizer added. Numerical result : %s",
                    res,
                )
            except Exception:
                logger.exception(
                    "Exception when optimizer is added to check parameter names"
                )
                traceback.print_exc()
        else:
            logger.warning(
                "no parameter with optimizer to compare with length %s before transformation"
                " and the length %s after transformation",
                len(dict(model_base.named_parameters())),
                len(dict(model_control.named_parameters())),
            )


def run_model(
    model_path,
    num_iters=1,
    debug=None,
    profile=None,
    symbolic_dims=None,
    feeds=None,
    override_initializers=True,
):
    symbolic_dims = symbolic_dims or {}
    if debug:
        print(f"Pausing execution ready for debugger to attach to pid: {os.getpid()}")
        print("Press key to continue.")
        sys.stdin.read(1)

    sess_options = None
    if profile:
        sess_options = onnxrt.SessionOptions()
        sess_options.enable_profiling = True
        sess_options.profile_file_prefix = os.path.basename(model_path)

    sess = onnxrt.InferenceSession(
        model_path,
        sess_options=sess_options,
        providers=onnxrt.get_available_providers(),
    )
    meta = sess.get_modelmeta()

    if not feeds:
        feeds = generate_feeds(sess, symbolic_dims)

    if override_initializers:
        # Starting with IR4 some initializers provide default values
        # and can be overridden (available in IR4). For IR < 4 models
        # the list would be empty
        for initializer in sess.get_overridable_initializers():
            shape = [dim if dim else 1 for dim in initializer.shape]
            if initializer.type in float_dict:
                feeds[initializer.name] = np.random.rand(*shape).astype(float_dict[initializer.type])
            elif initializer.type in integer_dict:
                feeds[initializer.name] = np.random.uniform(high=1000, size=tuple(shape)).astype(
                    integer_dict[initializer.type]
                )
            elif initializer.type == "tensor(bool)":
                feeds[initializer.name] = np.random.randint(2, size=tuple(shape)).astype("bool")
            else:
                print(f"unsupported initializer type {initializer.type} for initializer {initializer.name}")
                sys.exit(-1)

    start = timer()
    for _i in range(num_iters):
        outputs = sess.run([], feeds)  # fetch all outputs
    end = timer()

    print(f"model: {meta.graph_name}")
    print(f"version: {meta.version}")
    print(f"iterations: {num_iters}")
    print(f"avg latency: {((end - start) * 1000) / num_iters} ms")

    if profile:
        trace_file = sess.end_profiling()
        print(f"trace file written to: {trace_file}")

    return 0, feeds, num_iters > 0 and outputs


def run_model(model_path, all_inputs, use_gpu, disable_optimization):
    import onnxruntime  # noqa: PLC0415

    graph_optimization_level = None
    if disable_optimization:
        graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_DISABLE_ALL

    intra_op_num_threads = psutil.cpu_count(logical=False)

    session = create_session(
        model_path, use_gpu, "cuda" if use_gpu else "cpu", intra_op_num_threads, graph_optimization_level
    )

    output_names = [output.name for output in session.get_outputs()]
    results, latency_list = onnxruntime_inference(session, all_inputs, output_names)
    return results, latency_list, output_names

