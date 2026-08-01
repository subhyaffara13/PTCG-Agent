
def dispatch(
    sources: list[BuildSource],
    manager: BuildManager,
    stdout: TextIO,
    connect_threads: list[Thread],
) -> Graph:
    log_configuration(manager, sources)

    t0 = time.time()

    # We disable GC while loading the graph as a performance optimization for
    # cold-cache runs. The parsed ASTs are trees, and therefore should not have any
    # reference cycles. This is an important optimization, since we create a lot of
    # new objects while parsing files.
    global initial_gc_freeze_done
    if (
        not manager.options.test_env
        and platform.python_implementation() == "CPython"
        and not initial_gc_freeze_done
    ):
        gc.disable()
    graph = load_graph(sources, manager)

    # This is a kind of unfortunate hack to work around some of fine-grained's
    # fragility: if we have loaded less than 50% of the specified files from
    # cache in fine-grained cache mode, load the graph again honestly.
    # In this case, we just turn the cache off entirely, so we don't need
    # to worry about some files being loaded and some from cache and so
    # that fine-grained mode never *writes* to the cache.
    if manager.use_fine_grained_cache() and len(graph) < 0.50 * len(sources):
        manager.log("Redoing load_graph without cache because too much was missing")
        manager.cache_enabled = False
        graph = load_graph(sources, manager)

    if (
        not manager.options.test_env
        and platform.python_implementation() == "CPython"
        and not initial_gc_freeze_done
    ):
        gc.freeze()
        gc.unfreeze()
        gc.enable()
        initial_gc_freeze_done = True

    for id in graph:
        manager.import_map[id] = graph[id].dependencies_set

    t1 = time.time()
    manager.add_stats(
        graph_size=len(graph),
        stubs_found=sum(g.path is not None and g.path.endswith(".pyi") for g in graph.values()),
        graph_load_time=(t1 - t0),
        fm_cache_size=len(manager.find_module_cache.results),
    )
    if not graph:
        print("Nothing to do?!", file=stdout)
        return graph
    manager.log(f"Loaded graph with {len(graph)} nodes ({t1 - t0:.3f} sec)")
    if manager.options.dump_graph:
        dump_graph(graph, stdout)
        return graph

    # Fine-grained dependencies that didn't have an associated module in the build
    # are serialized separately, so we read them after we load the graph.
    # We need to read them both for running in daemon mode and if we are generating
    # a fine-grained cache (so that we can properly update them incrementally).
    # The `read_deps_cache` will also validate
    # the deps cache against the loaded individual cache files.
    if manager.options.cache_fine_grained or manager.use_fine_grained_cache():
        t2 = time.time()
        fg_deps_meta = read_deps_cache(manager, graph)
        manager.add_stats(load_fg_deps_time=time.time() - t2)
        if fg_deps_meta is not None:
            manager.fg_deps_meta = fg_deps_meta
        elif manager.stats.get("fresh_metas", 0) > 0:
            # Clear the stats, so we don't infinite loop because of positive fresh_metas
            manager.stats.clear()
            # There were some cache files read, but no fine-grained dependencies loaded.
            manager.log("Error reading fine-grained dependencies cache -- aborting cache load")
            manager.cache_enabled = False
            manager.log("Falling back to full run -- reloading graph...")
            return dispatch(sources, manager, stdout, connect_threads)

    # If we are loading a fine-grained incremental mode cache, we
    # don't want to do a real incremental reprocess of the
    # graph---we'll handle it all later.
    if not manager.use_fine_grained_cache():
        # Wait for workers since they may be needed at this point.
        for thread in connect_threads:
            thread.join()
        not_connected = [str(idx) for idx, wc in enumerate(manager.workers) if not wc.connected]
        if not_connected:
            raise OSError(f"Cannot connect to build worker(s): {', '.join(not_connected)}")
        process_graph(graph, manager)
        # Update plugins snapshot.
        write_plugins_snapshot(manager)
        manager.old_plugins_snapshot = manager.plugins_snapshot
        if manager.options.cache_fine_grained or manager.options.fine_grained_incremental:
            # If we are running a daemon or are going to write cache for further fine-grained use,
            # then we need to collect fine-grained protocol dependencies.
            # Since these are a global property of the program, they are calculated after we
            # processed the whole graph.
            type_state.add_all_protocol_deps(manager.fg_deps)
            if not manager.options.fine_grained_incremental:
                rdeps = generate_deps_for_cache(manager, graph)
                write_deps_cache(rdeps, manager, graph)

    if manager.options.dump_deps:
        # This speeds up startup a little when not using the daemon mode.
        from mypy.server.deps import dump_all_dependencies

        dump_all_dependencies(
            manager.modules, manager.all_types, manager.options.python_version, manager.options
        )

    return graph


def dispatch(
    node: torch.fx.Node, registry: _registration.ONNXRegistry
) -> tuple[Callable | None, str]:
    """Dispatch a node to an ONNX function based on the node's target and the ONNX registry.

    Args:
        node: The node to dispatch.
        registry: The ONNX registry to use for dispatching.

    Returns:
        A tuple containing the matched ONNX function and a string describing the reason for failure or success.
    """
    decomp_metas = registry.get_decomps(node.target)  # type: ignore[arg-type]
    # Determine if the node has complex inputs.
    is_complex = any(_arg_has_complex_dtype(arg) for arg in node.args) or any(
        _arg_has_complex_dtype(arg) for arg in node.kwargs.values()
    )
    if is_complex:
        decomp_metas = [decomp for decomp in decomp_metas if decomp.is_complex]
        if not decomp_metas:
            return None, "No decompositions registered for the complex-valued input"
    else:
        decomp_metas = [decomp for decomp in decomp_metas if not decomp.is_complex]
        if not decomp_metas:
            return None, "No decompositions registered for the real-valued input"

    # NOTE: Complex overload type matching logic has been removed to keep this simple
    # There should no longer be overloads (for the same opset version) in torchlib anymore
    return (decomp_metas[0].onnx_function, "The first implementation is used")


def dispatch(
    *types: Unpack[Ts], **kwargs: Any
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Dispatch function on the types of the inputs
    Supports dispatch on all non-keyword arguments.
    Collects implementations based on the function name.  Ignores namespaces.
    If ambiguous type signatures occur a warning is raised when the function is
    defined suggesting the additional method to break the ambiguity.

    Example:
        >>> # xdoctest: +SKIP
        >>> @dispatch(int)
        ... def f(x):
        ...     return x + 1
        >>> @dispatch(float)
        ... def f(x):
        ...     return x - 1
        >>> # xdoctest: +SKIP
        >>> f(3)
        4
        >>> f(3.0)
        2.0
        >>> # Specify an isolated namespace with the namespace keyword argument
        >>> my_namespace = {}
        >>> @dispatch(int, namespace=my_namespace)
        ... def foo(x):
        ...     return x + 1
        >>> # Dispatch on instance methods within classes
        >>> class MyClass(object):
        ...     @dispatch(list)
        ...     def __init__(self, data):
        ...         self.data = data
        ...
        ...     @dispatch(int)
        ...     def __init__(self, datum):
        ...         self.data = [datum]
        >>> MyClass([1, 2, 3]).data
        [1, 2, 3]
        >>> MyClass(3).data
        [3]
    """
    namespace = kwargs.get("namespace", global_namespace)

    types_tuple: tuple[type, ...] = tuple(types)  # type: ignore[arg-type]

    def _df(func):
        name = func.__name__

        if ismethod(func):
            dispatcher = inspect.currentframe().f_back.f_locals.get(  # type: ignore[union-attr]
                name,  # type: ignore[union-attr]
                MethodDispatcher(name),
            )
        else:
            if name not in namespace:
                namespace[name] = Dispatcher(name)
            dispatcher = namespace[name]

        dispatcher.add(types_tuple, func)
        return dispatcher

    return _df


def dispatch(*types, namespace=global_namespace, on_ambiguity=ambiguity_warn):
    """ Dispatch function on the types of the inputs

    Supports dispatch on all non-keyword arguments.

    Collects implementations based on the function name.  Ignores namespaces.

    If ambiguous type signatures occur a warning is raised when the function is
    defined suggesting the additional method to break the ambiguity.

    Examples
    --------

    >>> from sympy.multipledispatch import dispatch
    >>> @dispatch(int)
    ... def f(x):
    ...     return x + 1

    >>> @dispatch(float)
    ... def f(x): # noqa: F811
    ...     return x - 1

    >>> f(3)
    4
    >>> f(3.0)
    2.0

    Specify an isolated namespace with the namespace keyword argument

    >>> my_namespace = dict()
    >>> @dispatch(int, namespace=my_namespace)
    ... def foo(x):
    ...     return x + 1

    Dispatch on instance methods within classes

    >>> class MyClass(object):
    ...     @dispatch(list)
    ...     def __init__(self, data):
    ...         self.data = data
    ...     @dispatch(int)
    ...     def __init__(self, datum): # noqa: F811
    ...         self.data = [datum]
    """
    types = tuple(types)

    def _(func):
        name = func.__name__

        if ismethod(func):
            dispatcher = inspect.currentframe().f_back.f_locals.get(
                name,
                MethodDispatcher(name))
        else:
            if name not in namespace:
                namespace[name] = Dispatcher(name)
            dispatcher = namespace[name]

        dispatcher.add(types, func, on_ambiguity=on_ambiguity)
        return dispatcher
    return _

