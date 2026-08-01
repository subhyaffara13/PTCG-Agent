
def pytest_collection_modifyitems(config, items):
    # Setting this to True here allows tests to be set up before dispatching
    # any function call to a backend.
    if config.backend:
        # Allow pluggable backends to add markers to tests (such as skip or xfail)
        # when running in auto-conversion test mode
        backend_name = config.backend
        if backend_name != "networkx":
            nx.utils.backends._dispatchable._is_testing = True
            nx.config.backend_priority.algos = [backend_name]
            nx.config.backend_priority.generators = [backend_name]
            backend = nx.utils.backends.backends[backend_name].load()
            if hasattr(backend, "on_start_tests"):
                getattr(backend, "on_start_tests")(items)

    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


def pytest_collection_modifyitems(items, config) -> None:
    is_doctest = config.getoption("--doctest-modules") or config.getoption(
        "--doctest-cython", default=False
    )

    # Warnings from doctests that can be ignored; place reason in comment above.
    # Each entry specifies (path, message) - see the ignore_doctest_warning function
    ignored_doctest_warnings = [
        ("api.interchange.from_dataframe", "The DataFrame Interchange Protocol"),
        ("is_int64_dtype", "is_int64_dtype is deprecated"),
        ("is_interval_dtype", "is_interval_dtype is deprecated"),
        ("is_period_dtype", "is_period_dtype is deprecated"),
        ("is_datetime64tz_dtype", "is_datetime64tz_dtype is deprecated"),
        ("is_categorical_dtype", "is_categorical_dtype is deprecated"),
        ("is_sparse", "is_sparse is deprecated"),
        ("CategoricalDtype._from_values_or_dtype", "Constructing a Categorical"),
        ("DataFrame.__dataframe__", "The DataFrame Interchange Protocol"),
        ("DataFrameGroupBy.fillna", "DataFrameGroupBy.fillna is deprecated"),
        ("DataFrameGroupBy.corrwith", "DataFrameGroupBy.corrwith is deprecated"),
        ("NDFrame.replace", "Series.replace without 'value'"),
        ("NDFrame.clip", "Downcasting behavior in Series and DataFrame methods"),
        ("Series.idxmin", "The behavior of Series.idxmin"),
        ("Series.idxmax", "The behavior of Series.idxmax"),
        ("SeriesGroupBy.fillna", "SeriesGroupBy.fillna is deprecated"),
        ("SeriesGroupBy.idxmin", "The behavior of Series.idxmin"),
        ("SeriesGroupBy.idxmax", "The behavior of Series.idxmax"),
        ("to_pytimedelta", "The behavior of TimedeltaProperties.to_pytimedelta"),
        ("NDFrame.reindex_like", "keyword argument 'method' is deprecated"),
        # Docstring divides by zero to show behavior difference
        ("missing.mask_zero_div_zero", "divide by zero encountered"),
        (
            "pandas.core.generic.NDFrame.first",
            "first is deprecated and will be removed in a future version. "
            "Please create a mask and filter using `.loc` instead",
        ),
        (
            "Resampler.fillna",
            "DatetimeIndexResampler.fillna is deprecated",
        ),
        (
            "DataFrameGroupBy.fillna",
            "DataFrameGroupBy.fillna with 'method' is deprecated",
        ),
        ("read_parquet", "Passing a BlockManager to DataFrame is deprecated"),
    ]

    if is_doctest:
        for item in items:
            for path, message in ignored_doctest_warnings:
                ignore_doctest_warning(item, path, message)


def pytest_collection_modifyitems(config, items):
    """pytest hook."""
    # handle splits
    process_split(config, items)


def pytest_collection_modifyitems(
    session: Session, config: Config, items: list[Item]
) -> None:
    """Called after collection has been performed. May filter or re-order
    the items in-place.

    When items are deselected (filtered out from ``items``),
    the hook :hook:`pytest_deselected` must be called explicitly
    with the deselected items to properly notify other plugins,
    e.g. with ``config.hook.pytest_deselected(items=deselected_items)``.

    :param session: The pytest session object.
    :param config: The pytest config object.
    :param items: List of item objects.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """


def pytest_collection_modifyitems(items: list[nodes.Item], config: Config) -> None:
    deselect_prefixes = tuple(config.getoption("deselect") or [])
    if not deselect_prefixes:
        return

    remaining = []
    deselected = []
    for colitem in items:
        if colitem.nodeid.startswith(deselect_prefixes):
            deselected.append(colitem)
        else:
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining


def pytest_collection_modifyitems(items: list[Item], config: Config) -> None:
    deselect_by_keyword(items, config)
    deselect_by_mark(items, config)

