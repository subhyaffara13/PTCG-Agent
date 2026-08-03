import os
import sys
from typing import Callable

def build(
    base_model_cls: Callable[P, _BaseModelT],
    *args: P.args,
    **kwargs: P.kwargs,
) -> _BaseModelT:
    """Construct a BaseModel class without validation.

    This is useful for cases where you need to instantiate a `BaseModel`
    from an API response as this provides type-safe params which isn't supported
    by helpers like `construct_type()`.

    ```py
    build(MyModel, my_field_a="foo", my_field_b=123)
    ```
    """
    if args:
        raise TypeError(
            "Received positional arguments which are not supported; Keyword arguments must be used instead",
        )

    return cast(_BaseModelT, construct_type(type_=base_model_cls, value=kwargs))


def build(session: nox.Session) -> None:
    """
    Build SDists and wheels.
    """

    session.install("build")
    session.log("Building normal files")
    session.run("python", "-m", "build", *session.posargs)
    session.log("Building pybind11-global files (PYBIND11_GLOBAL_SDIST=1)")
    session.run(
        "python", "-m", "build", *session.posargs, env={"PYBIND11_GLOBAL_SDIST": "1"}
    )


def build(
    sources: list[BuildSource],
    options: Options,
    alt_lib_path: str | None = None,
    flush_errors: Callable[[str | None, list[str], bool], None] | None = None,
    fscache: FileSystemCache | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    extra_plugins: Sequence[Plugin] | None = None,
    worker_env: Mapping[str, str] | None = None,
) -> BuildResult:
    """Analyze a program.

    A single call to build performs parsing, semantic analysis and optionally
    type checking for the program *and* all imported modules, recursively.

    Return BuildResult if successful or only non-blocking errors were found;
    otherwise raise CompileError.

    If a flush_errors callback is provided, all error messages will be
    passed to it and the errors and messages fields of BuildResult and
    CompileError (respectively) will be empty. Otherwise, those fields will
    report any error messages.

    Args:
      sources: list of sources to build
      options: build options
      alt_lib_path: an additional directory for looking up library modules
        (takes precedence over other directories)
      flush_errors: optional function to flush errors after a file is processed
      fscache: optionally a file-system cacher
      stdout: Output stream to use instead of `sys.stdout`
      stderr: Error stream to use instead of `sys.stderr`
      extra_plugins: Plugins to use in addition to those loaded from config
      worker_env: An environment to start parallel build workers (used for tests)
    """
    # If we were not given a flush_errors, we use one that will populate those
    # fields for callers that want the traditional API.
    messages = []

    # This is mostly for the benefit of tests that use builtins fixtures.
    instance_cache.reset()
    reset_known_modules_cache()

    def default_flush_errors(
        filename: str | None, new_messages: list[str], is_serious: bool
    ) -> None:
        messages.extend(new_messages)

    flush_errors = flush_errors or default_flush_errors
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    extra_plugins = extra_plugins or []

    # Create metastore before workers to avoid race conditions.
    metastore = create_metastore(options, parallel_worker=False)
    workers = []
    connect_threads = []
    # A quasi-unique ID for this specific mypy invocation.
    build_id = os.urandom(4).hex()
    options_data = None
    if options.num_workers > 0:
        os.makedirs(options.cache_dir, exist_ok=True)
        options_data = os_path_join(options.cache_dir, f".worker_options.{build_id}.data")
        with open(options_data, "wb") as f:
            f.write(options.to_bytes())
        workers = [
            WorkerClient(
                f".mypy_worker.{build_id}.{idx}.json", options_data, worker_env or os.environ
            )
            for idx in range(options.num_workers)
        ]
        sources_message = SourcesDataMessage(sources=sources)
        buf = WriteBuffer()
        sources_message.write(buf)
        sources_data = buf.getvalue()

        def connect(wc: WorkerClient, data: bytes) -> None:
            # Start loading sources in each worker as soon as it is up.
            wc.connect()
            if not wc.connected:
                # Caller should detect this and fail gracefully.
                return
            wc.conn.write_bytes(data)

        # We don't wait for workers to be ready until they are actually needed.
        for worker in workers:
            thread = Thread(target=connect, args=(worker, sources_data))
            thread.start()
            connect_threads.append(thread)

    try:
        result = build_inner(
            sources,
            options,
            alt_lib_path,
            flush_errors,
            fscache,
            stdout,
            stderr,
            extra_plugins,
            workers,
            connect_threads,
            metastore,
        )
        result.errors = messages
        return result
    except CompileError as e:
        # CompileErrors raised from an errors object carry all the
        # messages that have not been reported out by error streaming.
        # Patch it up to contain either none or all none of the messages,
        # depending on whether we are flushing errors.
        serious = not e.use_stdout
        flush_errors(None, e.messages, serious)
        e.messages = messages
        raise
    finally:
        # In case of an early crash it is better to wait for workers to become ready, and
        # shut them down cleanly. Otherwise, they will linger until connection timeout.
        for thread in connect_threads:
            thread.join()
        if options_data is not None:
            os.unlink(options_data)
        for worker in workers:
            if not worker.connected:
                continue
            try:
                send(worker.conn, SccRequestMessage(scc_ids=[], import_errors={}, mod_data={}))
            except (OSError, IPCException):
                pass
        for worker in workers:
            worker.close()


def build(
    requirements: Iterable[InstallRequirement],
    wheel_cache: WheelCache,
    verify: bool,
) -> BuildResult:
    """Build wheels.

    :return: The list of InstallRequirement that succeeded to build and
        the list of InstallRequirement that failed to build.
    """
    if not requirements:
        return [], []

    # Build the wheels.
    logger.info(
        "Building wheels for collected packages: %s",
        ", ".join(req.name for req in requirements),  # type: ignore
    )

    with indent_log():
        build_successes, build_failures = [], []
        for req in requirements:
            assert req.name
            cache_dir = _get_cache_dir(req, wheel_cache)
            wheel_file = _build_one(
                req,
                cache_dir,
                verify,
                req.editable and req.permit_editable_wheels,
            )
            if wheel_file:
                # Record the download origin in the cache
                if req.download_info is not None:
                    # download_info is guaranteed to be set because when we build an
                    # InstallRequirement it has been through the preparer before, but
                    # let's be cautious.
                    wheel_cache.record_download_origin(cache_dir, req.download_info)
                # Update the link for this.
                req.link = Link(path_to_url(wheel_file))
                req.local_file_path = req.link.file_path
                assert req.link.is_wheel
                build_successes.append(req)
            else:
                build_failures.append(req)

    # notify success/failure
    if build_successes:
        logger.info(
            "Successfully built %s",
            " ".join([req.name for req in build_successes]),  # type: ignore
        )
    if build_failures:
        logger.info(
            "Failed to build %s",
            " ".join([req.name for req in build_failures]),  # type: ignore
        )
    # Return a list of requirements that failed to build
    return build_successes, build_failures


def build(cfile, outputfilename, compile_extra, link_extra,
          include_dirs, libraries, library_dirs):
    "use meson to build"

    build_dir = cfile.parent / "build"
    os.makedirs(build_dir, exist_ok=True)
    with open(cfile.parent / "meson.build", "wt") as fid:
        link_dirs = ['-L' + d for d in library_dirs]
        fid.write(textwrap.dedent(f"""\
            project('foo', 'c')
            py = import('python').find_installation(pure: false)
            py.extension_module(
                '{outputfilename.parts[-1]}',
                '{cfile.parts[-1]}',
                c_args: {compile_extra},
                link_args: {link_dirs},
                include_directories: {include_dirs},
            )
        """))
    native_file_name = cfile.parent / ".mesonpy-native-file.ini"
    with open(native_file_name, "wt") as fid:
        fid.write(textwrap.dedent(f"""\
            [binaries]
            python = '{sys.executable}'
        """))
    if sys.platform == "win32":
        run_subprocess(["meson", "setup",
                        "--buildtype=release",
                        "--vsenv", ".."],
                       build_dir)
    else:
        run_subprocess(["meson", "setup", "--vsenv",
                        "..", f'--native-file={os.fspath(native_file_name)}'],
                       build_dir)

    so_name = outputfilename.parts[-1] + get_so_suffix()
    run_subprocess(["meson", "compile"], build_dir)
    os.rename(str(build_dir / so_name), cfile.parent / so_name)
    return cfile.parent / so_name


def build(f, font, tableTag=None):
    """Convert a Monotype font layout file to an OpenType layout object

    A font object must be passed, but this may be a "dummy" font; it is only
    used for sorting glyph sets when making coverage tables and to hold the
    OpenType layout table while it is being built.

    Args:
            f: A file object.
            font (TTFont): A font object.
            tableTag (string): If provided, asserts that the file contains data for the
                    given OpenType table.

    Returns:
            An object representing the table. (e.g. ``table_G_S_U_B_``)
    """
    lines = Tokenizer(f)
    return parseTable(lines, font, tableTag=tableTag)


def build(
    designspace,
    master_finder=lambda s: s,
    exclude=[],
    optimize=True,
    colr_layer_reuse=True,
    drop_implied_oncurves=False,
):
    """
    Build variation font from a designspace file.

    If master_finder is set, it should be a callable that takes master
    filename as found in designspace file and map it to master font
    binary as to be opened (eg. .ttf or .otf).
    """
    if hasattr(designspace, "sources"):  # Assume a DesignspaceDocument
        pass
    else:  # Assume a file path
        designspace = DesignSpaceDocument.fromfile(designspace)

    ds = load_designspace(designspace)
    log.info("Building variable font")

    log.info("Loading master fonts")
    master_fonts = load_masters(designspace, master_finder)

    # TODO: 'master_ttfs' is unused except for return value, remove later
    master_ttfs = []
    for master in master_fonts:
        try:
            master_ttfs.append(master.reader.file.name)
        except AttributeError:
            master_ttfs.append(None)  # in-memory fonts have no path

    if drop_implied_oncurves and "glyf" in master_fonts[ds.base_idx]:
        drop_count = drop_implied_oncurve_points(*master_fonts)
        log.info(
            "Dropped %s on-curve points from simple glyphs in the 'glyf' table",
            drop_count,
        )

    # Copy the base master to work from it
    vf = deepcopy(master_fonts[ds.base_idx])

    if "DSIG" in vf:
        del vf["DSIG"]

    # Clear USE_MY_METRICS composite flags if set inconsistently across masters.
    if "glyf" in vf:
        _unset_inconsistent_use_my_metrics_flags(vf, master_fonts)

    # TODO append masters as named-instances as well; needs .designspace change.
    fvar = _add_fvar(vf, ds.axes, ds.instances)
    if "STAT" not in exclude:
        _add_stat(vf)

    # Map from axis names to axis tags...
    normalized_master_locs = [
        {ds.axes[k].tag: v for k, v in loc.items()} for loc in ds.normalized_master_locs
    ]
    # From here on, we use fvar axes only
    axisTags = [axis.axisTag for axis in fvar.axes]

    # Assume single-model for now.
    model = models.VariationModel(normalized_master_locs, axisOrder=axisTags)
    assert 0 == model.mapping[ds.base_idx]

    log.info("Building variations tables")
    if "avar" not in exclude:
        _add_avar(vf, ds.axes, ds.axisMappings, axisTags)
    if "BASE" not in exclude and "BASE" in vf:
        _add_BASE(vf, model, master_fonts, axisTags)
    if "MVAR" not in exclude:
        _add_MVAR(vf, model, master_fonts, axisTags)
    if "HVAR" not in exclude:
        _add_HVAR(vf, model, master_fonts, axisTags)
    if "VVAR" not in exclude and "vmtx" in vf:
        _add_VVAR(vf, model, master_fonts, axisTags)
    if "GDEF" not in exclude or "GPOS" not in exclude:
        _merge_OTL(vf, model, master_fonts, axisTags)
    if "gvar" not in exclude and "glyf" in vf:
        _add_gvar(vf, model, master_fonts, optimize=optimize)
    if "cvar" not in exclude and "glyf" in vf:
        _merge_TTHinting(vf, model, master_fonts)
    if "GSUB" not in exclude and ds.rules:
        featureTags = _feature_variations_tags(ds)
        _add_GSUB_feature_variations(
            vf, ds.axes, ds.internal_axis_supports, ds.rules, featureTags
        )
    if "CFF2" not in exclude and ("CFF " in vf or "CFF2" in vf):
        _add_CFF2(vf, model, master_fonts)
        if "post" in vf:
            # set 'post' to format 2 to keep the glyph names dropped from CFF2
            post = vf["post"]
            if post.formatType != 2.0:
                post.formatType = 2.0
                post.extraNames = []
                post.mapping = {}
    if "COLR" not in exclude and "COLR" in vf and vf["COLR"].version > 0:
        _add_COLR(vf, model, master_fonts, axisTags, colr_layer_reuse)

    set_default_weight_width_slant(
        vf, location={axis.axisTag: axis.defaultValue for axis in vf["fvar"].axes}
    )

    for tag in exclude:
        if tag in vf:
            del vf[tag]

    # TODO: Only return vf for 4.0+, the rest is unused.
    return vf, model, master_ttfs


def build(font, designspace_file):
    ds = load_designspace(designspace_file, require_sources=False)

    if not "fvar" in font:
        if "name" not in font:
            font["name"] = newTable("name")
        _add_fvar(font, ds.axes, ds.instances)

    axisTags = [a.axisTag for a in font["fvar"].axes]

    if "avar" in font:
        log.warning("avar table already present, overwriting.")
        del font["avar"]

    _add_avar(font, ds.axes, ds.axisMappings, axisTags)

