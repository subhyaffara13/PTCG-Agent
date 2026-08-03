import functools
import sys
from typing import Any, Callable, Optional, Union

def register(t):
    """decorator to register types to Pickler's :attr:`~Pickler.dispatch` table"""
    def proxy(func):
        Pickler.dispatch[t] = func
        return func
    return proxy


def register(name: str, environment: dict[str, Any]) -> None:
    """
    Register an environment by name.  An environment contains the following:
     * specification - JSON Schema representing the environment.
     * interpreter - Function(state, environment) -> new_state
     * renderer - Function(state, environment) -> string
     * html_renderer - Function(environment) -> JavaScript HTML renderer function.
     * agents(optional) - List of default agents [Function(observation, config) -> action]
    """
    environments[name] = environment


def register(viewer: type[Viewer] | Viewer, order: int = 1) -> None:
    """
    The :py:func:`register` function is used to register additional viewers::

        from PIL import ImageShow
        ImageShow.register(MyViewer())  # MyViewer will be used as a last resort
        ImageShow.register(MySecondViewer(), 0)  # MySecondViewer will be prioritised
        ImageShow.register(ImageShow.XVViewer(), 0)  # XVViewer will be prioritised

    :param viewer: The viewer to be registered.
    :param order:
        Zero or a negative integer to prepend this viewer to the list,
        a positive integer to append it.
    """
    if isinstance(viewer, type) and issubclass(viewer, Viewer):
        viewer = viewer()
    if order > 0:
        _viewers.append(viewer)
    else:
        _viewers.insert(0, viewer)


def register(linter: PyLinter) -> None:
    linter.register_checker(AsyncChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(BadChainedComparisonChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DataclassChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MisdesignChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DunderCallChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(EllipsisChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ExceptionsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(FormatChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ImportsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(LambdaExpressionChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(LoggingChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MatchStatementChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MethodArgsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(EncodingChecker(linter))
    linter.register_checker(ByIdManagedMessagesChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ModifiedIterationChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(NestedMinMaxChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(NewStyleConflictChecker(linter))


def register(linter: lint.PyLinter) -> None:
    linter.register_checker(NonAsciiNameChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(RawMetricsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(SpellingChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(StdlibChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(StringFormatChecker(linter))
    linter.register_checker(StringConstantChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(SimilaritiesChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ThreadingChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(TypeChecker(linter))
    linter.register_checker(IterableChecker(linter))


def register(linter: pylint.lint.PyLinter) -> None:
    linter.register_checker(UnicodeChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(UnsupportedVersionChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(VariablesChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(BadBuiltinChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(BroadTryClauseChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ElseifUsedChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(CodeStyleChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MisplacedComparisonConstantChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ConfusingConsecutiveElifChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ConsiderRefactorIntoWhileConditionChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ConsiderTernaryExpressionChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DictInitMutateChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DocstringParameterChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DocStringStyleChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(DunderChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(CommentChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(EqWithoutHash(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ConsiderUsingAnyOrAllChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MagicValueChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(McCabeMethodChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(NoSelfUseChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(OverlappingExceptionsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(PrivateImportChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(RedefinedLoopNameChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(MultipleTypesChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(SetMembershipChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(TypingChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(WhileChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_reporter(JSONReporter)
    linter.register_reporter(JSON2Reporter)


def register(linter: PyLinter) -> None:
    linter.register_reporter(TextReporter)
    linter.register_reporter(NoHeaderReporter)
    linter.register_reporter(ParseableTextReporter)
    linter.register_reporter(VSTextReporter)
    linter.register_reporter(ColorizedTextReporter)
    linter.register_reporter(GithubReporter)


def register(linter: PyLinter) -> None:
    linter.register_checker(BasicErrorChecker(linter))
    linter.register_checker(BasicChecker(linter))
    linter.register_checker(NameChecker(linter))
    linter.register_checker(DocStringChecker(linter))
    linter.register_checker(PassChecker(linter))
    linter.register_checker(ComparisonChecker(linter))
    linter.register_checker(FunctionChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(ClassChecker(linter))
    linter.register_checker(SpecialMethodsChecker(linter))


def register(linter: PyLinter) -> None:
    linter.register_checker(RefactoringChecker(linter))
    linter.register_checker(NotChecker(linter))
    linter.register_checker(RecommendationChecker(linter))
    linter.register_checker(ImplicitBooleanessChecker(linter))


def register() -> None:
    """
    Register pandas formatters and converters with matplotlib.

    This function modifies the global ``matplotlib.units.registry``
    dictionary. pandas adds custom converters for

    * pd.Timestamp
    * pd.Period
    * np.datetime64
    * datetime.datetime
    * datetime.date
    * datetime.time

    See Also
    --------
    deregister_matplotlib_converters : Remove pandas formatters and converters.

    Examples
    --------
    .. plot::
       :context: close-figs

        The following line is done automatically by pandas so
        the plot can be rendered:

        >>> pd.plotting.register_matplotlib_converters()

        >>> df = pd.DataFrame(
        ...     {"ts": pd.period_range("2020", periods=2, freq="M"), "y": [1, 2]}
        ... )
        >>> plot = df.plot.line(x="ts", y="y")

    Unsetting the register manually an error will be raised:

    >>> pd.set_option(
    ...     "plotting.matplotlib.register_converters", False
    ... )  # doctest: +SKIP
    >>> df.plot.line(x="ts", y="y")  # doctest: +SKIP
    Traceback (most recent call last):
    TypeError: float() argument must be a string or a real number, not 'Period'
    """
    plot_backend = _get_plot_backend("matplotlib")
    plot_backend.register()


def register(cls) -> None:
    try:
        name = cls.name
    except AttributeError:
        name = cls.__name__
    holiday_calendars[name] = cls


def register() -> None:
    pairs = get_pairs()
    for type_, cls in pairs:
        # Cache previous converter if present
        if type_ in munits.registry and not isinstance(munits.registry[type_], cls):
            previous = munits.registry[type_]
            _mpl_units[type_] = previous
        # Replace with pandas converter
        munits.registry[type_] = cls()


def register():
    """Register ONNX Runtime's built-in contrib ops.

    Should be run before torch.onnx.export().
    """

    def grid_sampler(g, input, grid, mode, padding_mode, align_corners):
        # mode
        #   'bilinear'      : onnx::Constant[value={0}]
        #   'nearest'       : onnx::Constant[value={1}]
        #   'bicubic'       : onnx::Constant[value={2}]
        # padding_mode
        #   'zeros'         : onnx::Constant[value={0}]
        #   'border'        : onnx::Constant[value={1}]
        #   'reflection'    : onnx::Constant[value={2}]
        mode = symbolic_helper._maybe_get_const(mode, "i")
        padding_mode = symbolic_helper._maybe_get_const(padding_mode, "i")
        mode_str = ["bilinear", "nearest", "bicubic"][mode]
        padding_mode_str = ["zeros", "border", "reflection"][padding_mode]
        align_corners = int(symbolic_helper._maybe_get_const(align_corners, "b"))

        return g.op(
            "com.microsoft::GridSample",
            input,
            grid,
            mode_s=mode_str,
            padding_mode_s=padding_mode_str,
            align_corners_i=align_corners,
        )

    _reg(grid_sampler)

    def inverse(g, self):
        return g.op("com.microsoft::Inverse", self).setType(self.type())

    _reg(inverse)
    torch.onnx.register_custom_op_symbolic("aten::linalg_inv", inverse, _OPSET_VERSION)
    _registered_ops.add("aten::linalg_inv")

    def gelu(g, self: torch._C.Value, approximate="none"):
        # PyTorch can emit aten::gelu with or without the optional approximate arg.
        if not isinstance(approximate, str):
            approximate = symbolic_helper._maybe_get_const(approximate, "s")

        # Use microsoft::Gelu for performance if possible. It only supports approximate == "none".
        if approximate == "none":
            return g.op("com.microsoft::Gelu", self).setType(self.type())
        return torch.onnx.symbolic_opset9.gelu(g, self, approximate)

    _reg(gelu)
    # Some PyTorch versions dispatch GELU symbolic lookup by exporter opset.
    # Registering across stable opsets keeps ORT Gelu fusion consistently enabled.
    for opset in range(9, 21):
        torch.onnx.register_custom_op_symbolic("aten::gelu", gelu, opset)

    def triu(g, self, diagonal):
        return g.op("com.microsoft::Trilu", self, diagonal, upper_i=1).setType(self.type())

    _reg(triu)

    def tril(g, self, diagonal):
        return g.op("com.microsoft::Trilu", self, diagonal, upper_i=0).setType(self.type())

    _reg(tril)

    @torch.onnx.symbolic_helper.parse_args("v")
    def DynamicTimeWarping(g, self):  # noqa: N802
        return g.op("com.microsoft::DynamicTimeWarping", self)

    _reg(DynamicTimeWarping, namespace="onnxruntime")

    def UnfoldTensor(g, self, dim, size, step):  # noqa: N802
        dim = int(symbolic_helper._maybe_get_const(dim, "i"))
        size = int(symbolic_helper._maybe_get_const(size, "i"))
        step = int(symbolic_helper._maybe_get_const(step, "i"))
        return g.op(
            "com.microsoft::UnfoldTensor",
            self,
            dim_i=dim,
            size_i=size,
            step_i=step,
        ).setType(self.type().with_sizes([None, None, None, None, size]))

    _reg(UnfoldTensor, namespace="onnxruntime")


def register(name: str) -> Register:
    return Register(int_rprimitive, "foo", is_arg=True)


def register():
    """Register the unit conversion classes with matplotlib."""
    import matplotlib.units as mplU

    mplU.registry[str] = StrConverter()
    mplU.registry[Epoch] = EpochConverter()
    mplU.registry[Duration] = EpochConverter()
    mplU.registry[UnitDbl] = UnitDblConverter()


def register(deprecation_id: str) -> None:
  _registered_deprecations[deprecation_id] = DeprecationState()


def register(
    id: str,
    entry_point: EnvCreator | str | None = None,
    reward_threshold: float | None = None,
    nondeterministic: bool = False,
    max_episode_steps: int | None = None,
    order_enforce: bool = True,
    disable_env_checker: bool = False,
    additional_wrappers: tuple[WrapperSpec, ...] = (),
    vector_entry_point: VectorEnvCreator | str | None = None,
    kwargs: dict | None = None,
):
    """Registers an environment in gymnasium with an ``id`` to use with :meth:`gymnasium.make` with the ``entry_point`` being a string or callable for creating the environment.

    The ``id`` parameter corresponds to the name of the environment, with the syntax as follows:
    ``[namespace/](env_name)[-v(version)]`` where ``namespace`` and ``-v(version)`` is optional.

    It takes arbitrary keyword arguments, which are passed to the :class:`EnvSpec` ``kwargs`` parameter.

    Args:
        id: The environment id
        entry_point: The entry point for creating the environment
        reward_threshold: The reward threshold considered for an agent to have learnt the environment
        nondeterministic: If the environment is nondeterministic (even with knowledge of the initial seed and all actions, the same state cannot be reached)
        max_episode_steps: The maximum number of episodes steps before truncation. Used by the :class:`gymnasium.wrappers.TimeLimit` wrapper if not ``None``.
        order_enforce: If to enable the order enforcer wrapper to ensure users run functions in the correct order.
            If ``True``, then the :class:`gymnasium.wrappers.OrderEnforcing` is applied to the environment.
        disable_env_checker: If to disable the :class:`gymnasium.wrappers.PassiveEnvChecker` to the environment.
        additional_wrappers: Additional wrappers to apply the environment.
        vector_entry_point: The entry point for creating the vector environment
        kwargs: arbitrary keyword arguments which are passed to the environment constructor on initialisation.

    Changelogs:
        v1.0.0 - `autoreset` and `apply_api_compatibility` parameter was removed
    """
    assert (
        entry_point is not None or vector_entry_point is not None
    ), "Either `entry_point` or `vector_entry_point` (or both) must be provided"
    ns, name, version = parse_env_id(id)

    if kwargs is None:
        kwargs = dict()
    if current_namespace is not None:
        if (
            kwargs.get("namespace") is not None
            and kwargs.get("namespace") != current_namespace
        ):
            logger.warn(
                f"Custom namespace `{kwargs.get('namespace')}` is being overridden by namespace `{current_namespace}`. "
                f"If you are developing a plugin you shouldn't specify a namespace in `register` calls. "
                "The namespace is specified through the entry point package metadata."
            )
        ns_id = current_namespace
    else:
        ns_id = ns
    full_env_id = get_env_id(ns_id, name, version)

    new_spec = EnvSpec(
        id=full_env_id,
        entry_point=entry_point,
        reward_threshold=reward_threshold,
        nondeterministic=nondeterministic,
        max_episode_steps=max_episode_steps,
        order_enforce=order_enforce,
        disable_env_checker=disable_env_checker,
        kwargs=kwargs,
        additional_wrappers=additional_wrappers,
        vector_entry_point=vector_entry_point,
    )
    _check_spec_register(new_spec)

    if new_spec.id in registry:
        logger.warn(f"Overriding environment {new_spec.id} already in registry.")
    registry[new_spec.id] = new_spec


def register(
    id: str,
    entry_point: Union[Callable, str],
    reward_threshold: Optional[float] = None,
    nondeterministic: bool = False,
    max_episode_steps: Optional[int] = None,
    order_enforce: bool = True,
    autoreset: bool = False,
    disable_env_checker: bool = False,
    apply_api_compatibility: bool = False,
    **kwargs,
):
    """Register an environment with gym.

    The `id` parameter corresponds to the name of the environment, with the syntax as follows:
    `(namespace)/(env_name)-v(version)` where `namespace` is optional.

    It takes arbitrary keyword arguments, which are passed to the `EnvSpec` constructor.

    Args:
        id: The environment id
        entry_point: The entry point for creating the environment
        reward_threshold: The reward threshold considered to have learnt an environment
        nondeterministic: If the environment is nondeterministic (even with knowledge of the initial seed and all actions)
        max_episode_steps: The maximum number of episodes steps before truncation. Used by the Time Limit wrapper.
        order_enforce: If to enable the order enforcer wrapper to ensure users run functions in the correct order
        autoreset: If to add the autoreset wrapper such that reset does not need to be called.
        disable_env_checker: If to disable the environment checker for the environment. Recommended to False.
        apply_api_compatibility: If to apply the `StepAPICompatibility` wrapper.
        **kwargs: arbitrary keyword arguments which are passed to the environment constructor
    """
    global registry, current_namespace
    ns, name, version = parse_env_id(id)

    if current_namespace is not None:
        if (
            kwargs.get("namespace") is not None
            and kwargs.get("namespace") != current_namespace
        ):
            logger.warn(
                f"Custom namespace `{kwargs.get('namespace')}` is being overridden by namespace `{current_namespace}`. "
                f"If you are developing a plugin you shouldn't specify a namespace in `register` calls. "
                "The namespace is specified through the entry point package metadata."
            )
        ns_id = current_namespace
    else:
        ns_id = ns

    full_id = get_env_id(ns_id, name, version)

    new_spec = EnvSpec(
        id=full_id,
        entry_point=entry_point,
        reward_threshold=reward_threshold,
        nondeterministic=nondeterministic,
        max_episode_steps=max_episode_steps,
        order_enforce=order_enforce,
        autoreset=autoreset,
        disable_env_checker=disable_env_checker,
        apply_api_compatibility=apply_api_compatibility,
        **kwargs,
    )
    _check_spec_register(new_spec)
    if new_spec.id in registry:
        logger.warn(f"Overriding environment {new_spec.id} already in registry.")
    registry[new_spec.id] = new_spec


def register():
    register_implementation("http", HTTPFileSystem, clobber=True)
    register_implementation("https", HTTPFileSystem, clobber=True)
    register_implementation("sync-http", HTTPFileSystem, clobber=True)
    register_implementation("sync-https", HTTPFileSystem, clobber=True)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Call, inference_tip(infer_namespace), _looks_like_namespace
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.ClassDef, attr_attributes_transform, is_decorated_with_attrs
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        ClassDef, service_request_transform, _looks_like_boto3_service_request
    )


def register(manager: AstroidManager) -> None:
    # Builtins inference
    register_builtin_transform(manager, infer_bool, "bool")
    register_builtin_transform(manager, infer_super, "super")
    register_builtin_transform(manager, infer_callable, "callable")
    register_builtin_transform(manager, infer_property, "property")
    register_builtin_transform(manager, infer_getattr, "getattr")
    register_builtin_transform(manager, infer_hasattr, "hasattr")
    register_builtin_transform(manager, infer_tuple, "tuple")
    register_builtin_transform(manager, infer_set, "set")
    register_builtin_transform(manager, infer_list, "list")
    register_builtin_transform(manager, infer_dict, "dict")
    register_builtin_transform(manager, infer_frozenset, "frozenset")
    register_builtin_transform(manager, infer_type, "type")
    register_builtin_transform(manager, infer_slice, "slice")
    register_builtin_transform(manager, infer_isinstance, "isinstance")
    register_builtin_transform(manager, infer_issubclass, "issubclass")
    register_builtin_transform(manager, infer_len, "len")
    register_builtin_transform(manager, infer_str, "str")
    register_builtin_transform(manager, infer_int, "int")
    register_builtin_transform(manager, infer_dict_fromkeys, "dict.fromkeys")

    # Infer object.__new__ calls
    manager.register_transform(
        nodes.ClassDef,
        inference_tip(_infer_object__new__decorator),
        _infer_object__new__decorator_check,
    )

    manager.register_transform(
        nodes.Call,
        inference_tip(_infer_copy_method),
        lambda node: isinstance(node.func, nodes.Attribute)
        and node.func.attrname == "copy",
    )

    manager.register_transform(
        nodes.Call,
        inference_tip(_infer_str_format_call),
        _is_str_format_call,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "collections", _collections_transform)

    # Starting with Python39 some objects of the collection module are subscriptable
    # thanks to the __class_getitem__ method but the way it is implemented in
    # _collection_abc makes it difficult to infer. (We would have to handle AssignName inference in the
    # getitem method of the ClassDef class) Instead we put here a mock of the __class_getitem__ method
    manager.register_transform(
        ClassDef, easy_class_getitem_inference, _looks_like_subscriptable
    )

    if PY313_PLUS:
        register_module_extender(
            manager, "collections.abc", _collections_abc_313_transform
        )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "crypt", _re_transform)


def register(manager: AstroidManager) -> None:
    if not hasattr(sys, "pypy_version_info"):
        # No need of this module in pypy where everything is written in python
        register_module_extender(manager, "ctypes", enrich_ctypes_redefined_types)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "curses", _curses_transform)


def register(manager: AstroidManager) -> None:
    if PY313_PLUS:
        manager.register_transform(
            nodes.Module,
            _resolve_private_replace_to_public,
            _looks_like_dataclasses,
        )

    manager.register_transform(
        nodes.ClassDef, dataclass_transform, is_decorated_with_dataclass
    )

    manager.register_transform(
        nodes.Call,
        inference_tip(infer_dataclass_field_call, raise_on_overwrite=True),
        _looks_like_dataclass_field_call,
    )

    manager.register_transform(
        nodes.Unknown,
        inference_tip(infer_dataclass_attribute, raise_on_overwrite=True),
        _looks_like_dataclass_attribute,
    )


def register(manager: AstroidManager) -> None:
    if PY312_PLUS:
        register_module_extender(manager, "datetime", datetime_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "dateutil.parser", dateutil_transform)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.FunctionDef, _transform_lru_cache, _looks_like_lru_cache
    )

    manager.register_transform(
        nodes.Call,
        inference_tip(_functools_partial_inference),
        _looks_like_partial,
    )


def register(manager: AstroidManager) -> None:
    manager.register_failed_import_hook(_import_gi_module)
    manager.register_transform(
        nodes.Call, _register_require_version, _looks_like_require_version
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "hashlib", _hashlib_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "http", _http_transform)
    register_module_extender(manager, "http.client", _http_client_transform)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        node_class=FunctionDef,
        transform=remove_draw_parameter_from_composite_strategy,
        predicate=is_decorated_with_st_composite,
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        ClassDef, _transform_buffered, lambda node: node.name in BUFFERED
    )
    manager.register_transform(
        ClassDef, _transform_text_io_wrapper, lambda node: node.name == TextIOWrapper
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "mechanize", mechanize_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "multiprocessing.managers", _multiprocessing_managers_transform
    )
    register_module_extender(manager, "multiprocessing", _multiprocessing_transform)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Call, inference_tip(infer_named_tuple), _looks_like_namedtuple
    )
    manager.register_transform(nodes.Call, inference_tip(infer_enum), _looks_like_enum)
    manager.register_transform(
        nodes.ClassDef, infer_enum_class, predicate=_is_enum_subclass
    )
    manager.register_transform(
        nodes.ClassDef,
        inference_tip(infer_typing_namedtuple_class),
        _has_namedtuple_base,
    )
    manager.register_transform(
        nodes.FunctionDef,
        inference_tip(infer_typing_namedtuple_function),
        lambda node: node.name == "NamedTuple"
        and getattr(node.root(), "name", None) == "typing",
    )
    manager.register_transform(
        nodes.Call,
        inference_tip(infer_typing_namedtuple),
        _looks_like_typing_namedtuple,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.core.einsumfunc", numpy_core_einsumfunc_transform
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.core.fromnumeric", numpy_core_fromnumeric_transform
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Attribute,
        inference_tip(functools.partial(infer_numpy_attribute, METHODS_TO_BE_INFERRED)),
        functools.partial(
            attribute_name_looks_like_numpy_member,
            frozenset(METHODS_TO_BE_INFERRED.keys()),
        ),
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.core.multiarray", numpy_core_multiarray_transform
    )

    method_names = frozenset(METHODS_TO_BE_INFERRED.keys())

    manager.register_transform(
        nodes.Attribute,
        inference_tip(functools.partial(infer_numpy_attribute, METHODS_TO_BE_INFERRED)),
        functools.partial(attribute_name_looks_like_numpy_member, method_names),
    )
    manager.register_transform(
        nodes.Name,
        inference_tip(functools.partial(infer_numpy_name, METHODS_TO_BE_INFERRED)),
        functools.partial(member_name_looks_like_numpy_member, method_names),
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.core.numeric", numpy_core_numeric_transform
    )

    manager.register_transform(
        nodes.Attribute,
        inference_tip(functools.partial(infer_numpy_attribute, METHODS_TO_BE_INFERRED)),
        functools.partial(
            attribute_name_looks_like_numpy_member,
            frozenset(METHODS_TO_BE_INFERRED.keys()),
        ),
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.core.numerictypes", numpy_core_numerictypes_transform
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "numpy.core.umath", numpy_core_umath_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "numpy.ma", numpy_ma_transform)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Attribute,
        inference_tip(infer_numpy_ndarray),
        _looks_like_numpy_ndarray,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(
        manager, "numpy.random.mtrand", numpy_random_mtrand_transform
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Subscript,
        inference_tip(infer_parents_subscript),
        _looks_like_parents_subscript,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "pkg_resources", pkg_resources_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "pytest", pytest_transform)
    register_module_extender(manager, "py.test", pytest_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "PyQt4.QtCore", pyqt4_qtcore_transform)
    manager.register_transform(
        nodes.FunctionDef, transform_pyqt_signal, _looks_like_signal
    )
    manager.register_transform(
        nodes.ClassDef,
        transform_pyside_signal,
        lambda node: node.qname() in {"PySide.QtCore.Signal", "PySide2.QtCore.Signal"},
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Call, inference_tip(infer_random_sample), _looks_like_random_sample
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "re", _re_transform)
    manager.register_transform(
        nodes.Call, inference_tip(infer_pattern_match), _looks_like_pattern_or_match
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "regex", _regex_transform)
    manager.register_transform(
        nodes.Call, inference_tip(infer_pattern_match), _looks_like_pattern_or_match
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "responses", responses_funcs)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "scipy.signal", scipy_signal)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "signal", _signals_enums_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "six", six_moves_transform)
    register_module_extender(
        manager, "requests.packages.urllib3.packages.six", six_moves_transform
    )
    manager.register_failed_import_hook(_six_fail_hook)
    manager.register_transform(
        nodes.ClassDef,
        transform_six_add_metaclass,
        _looks_like_decorated_with_six_add_metaclass,
    )
    manager.register_transform(
        nodes.ClassDef,
        transform_six_with_metaclass,
        _looks_like_nested_from_six_with_metaclass,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "sqlalchemy.orm.session", _session_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "ssl", ssl_transform)


def register(manager: AstroidManager) -> None:
    """Register statistics-specific inference improvements."""
    manager.register_transform(
        nodes.Call,
        inference_tip(infer_statistics_quantiles),
        _looks_like_statistics_quantiles,
    )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "subprocess", _subprocess_transform)


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "threading", _thread_transform)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Name, inference_tip(infer_type_sub), _looks_like_type_subscript
    )


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.Call,
        inference_tip(infer_typing_typevar_or_newtype),
        looks_like_typing_typevar_or_newtype,
    )
    manager.register_transform(
        nodes.Subscript, inference_tip(infer_typing_attr), _looks_like_typing_subscript
    )
    manager.register_transform(
        nodes.Call, inference_tip(infer_typing_cast), _looks_like_typing_cast
    )

    manager.register_transform(
        nodes.FunctionDef, inference_tip(infer_typedDict), _looks_like_typedDict
    )

    manager.register_transform(
        nodes.Call, inference_tip(infer_typing_alias), _looks_like_typing_alias
    )
    manager.register_transform(
        nodes.Call, inference_tip(infer_special_alias), _looks_like_special_alias
    )

    if PY312_PLUS:
        register_module_extender(manager, "typing", _typing_transform)
        manager.register_transform(
            nodes.ClassDef,
            inference_tip(infer_typing_generic_class_pep695),
            _looks_like_generic_class_pep695,
        )


def register(manager: AstroidManager) -> None:
    register_module_extender(manager, "unittest", IsolatedAsyncioTestCaseImport)


def register(manager: AstroidManager) -> None:
    manager.register_transform(
        nodes.ClassDef, _patch_uuid_class, lambda node: node.qname() == "uuid.UUID"
    )

