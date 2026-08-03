import functools
import itertools
import os
import pathlib
import re
import sys
import time
from typing import Any, Dict, Optional

def load(file, **kwds):
    """load an object that was stored with dill.temp.dump

    file: filehandle
    mode: mode to open the file, one of: {'r', 'rb'}

    >>> dumpfile = dill.temp.dump([1, 2, 3, 4, 5])
    >>> dill.temp.load(dumpfile)
    [1, 2, 3, 4, 5]
    """
    import dill as pickle
    mode = kwds.pop('mode', 'rb')
    name = getattr(file, 'name', file) # name=file.name or name=file (if str)
    return pickle.load(open(name, mode=mode, **kwds))


def load(file, ignore=None, **kwds):
    """
    Unpickle an object from a file.

    See :func:`loads` for keyword arguments.
    """
    return Unpickler(file, ignore=ignore, **kwds).load()


def load(filename: str) -> ImageFont:
    """
    Load a font file. This function loads a font object from the given
    bitmap font file, and returns the corresponding font object. For loading TrueType
    or OpenType fonts instead, see :py:func:`~PIL.ImageFont.truetype`.

    :param filename: Name of font file.
    :return: A font object.
    :exception OSError: If the file could not be read.
    """
    f = ImageFont()
    f._load_pilfont(filename)
    return f


def load(filename: str) -> tuple[bytes, str]:
    # FIXME: supports GIMP gradients only

    with open(filename, "rb") as fp:
        paletteHandlers: list[
            type[
                GimpPaletteFile.GimpPaletteFile
                | GimpGradientFile.GimpGradientFile
                | PaletteFile.PaletteFile
            ]
        ] = [
            GimpPaletteFile.GimpPaletteFile,
            GimpGradientFile.GimpGradientFile,
            PaletteFile.PaletteFile,
        ]
        for paletteHandler in paletteHandlers:
            try:
                fp.seek(0)
                lut = paletteHandler(fp).getpalette()
                if lut:
                    break
            except (SyntaxError, ValueError):
                pass
        else:
            msg = "cannot load palette"
            raise OSError(msg)

    return lut  # data, rawmode


def load(data: bytes) -> Dict[str, Array]:
    """
    Loads a safetensors file into flax format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, Array]`: dictionary that contains name as key, value as `Array` on cpu

    Example:

    ```python
    from safetensors.flax import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    flat = numpy.load(data)
    return _np2jnp(flat)


def load(data: bytes) -> Dict[str, mx.array]:
    """
    Loads a safetensors file into MLX format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, mx.array]`: dictionary that contains name as key, value as `mx.array`

    Example:

    ```python
    from safetensors.mlx import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    flat = numpy.load(data)
    return _np2mx(flat)


def load(data: bytes) -> Dict[str, np.ndarray]:
    """
    Loads a safetensors file into numpy format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, np.ndarray]`: dictionary that contains name as key, value as `np.ndarray` on cpu

    Example:

    ```python
    from safetensors.numpy import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    flat = deserialize(data)
    return _view2np(flat)


def load(data: bytes, device: str = "cpu") -> Dict[str, paddle.Tensor]:
    """
    Loads a safetensors file into paddle format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, paddle.Tensor]`: dictionary that contains name as key, value as `paddle.Tensor` on cpu

    Example:

    ```python
    from safetensors.paddle import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    if paddle.__version__ >= "3.2.0":
        flat = deserialize(data)
        return _view2paddle(flat, device)
    else:
        flat = numpy.load(data)
        return _np2paddle(flat, device)


def load(data: bytes) -> Dict[str, tf.Tensor]:
    """
    Loads a safetensors file into tensorflow format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, tf.Tensor]`: dictionary that contains name as key, value as `tf.Tensor` on cpu

    Example:

    ```python
    from safetensors.tensorflow import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    flat = numpy.load(data)
    return _np2tf(flat)


def load(data: bytes) -> Dict[str, torch.Tensor]:
    """
    Loads a safetensors file into torch format from pure bytes.

    Args:
        data (`bytes`):
            The content of a safetensors file

    Returns:
        `Dict[str, torch.Tensor]`: dictionary that contains name as key, value as `torch.Tensor` on cpu

    Example:

    ```python
    from safetensors.torch import load

    file_path = "./my_folder/bert.safetensors"
    with open(file_path, "rb") as f:
        data = f.read()

    loaded = load(data)
    ```
    """
    flat = deserialize(data)
    return _view2torch(flat)


def load(eps):
    """
    Given a Distribution.entry_points, produce EntryPoints.
    """
    groups = itertools.chain.from_iterable(
        load_group(value, group) for group, value in eps.items()
    )
    return validate(metadata.EntryPoints(groups))


def load(fp, encoding=None, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None,
        use_decimal=False, allow_nan=False, array_hook=None, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document as `str` or `bytes`) to a Python object.

    *encoding* determines the encoding used to interpret any
    `bytes` objects decoded by this instance (``'utf-8'`` by
    default). It has no effect when decoding `str` objects.

    *object_hook*, if specified, will be called with the result of every
    JSON object decoded and its return value will be used in place of the
    given :class:`dict`.  This can be used to provide custom
    deserializations (e.g. to support JSON-RPC class hinting).

    *object_pairs_hook* is an optional function that will be called with
    the result of any object literal decode with an ordered list of pairs.
    The return value of *object_pairs_hook* will be used instead of the
    :class:`dict`.  This feature can be used to implement custom decoders
    that rely on the order that the key and value pairs are decoded (for
    example, :func:`collections.OrderedDict` will remember the order of
    insertion). If *object_hook* is also defined, the *object_pairs_hook*
    takes priority.

    *parse_float*, if specified, will be called with the string of every
    JSON float to be decoded. By default, this is equivalent to
    ``float(num_str)``. This can be used to use another datatype or parser
    for JSON floats (e.g. :class:`decimal.Decimal`).

    *parse_int*, if specified, will be called with the string of every
    JSON int to be decoded. By default, this is equivalent to
    ``int(num_str)``.  This can be used to use another datatype or parser
    for JSON integers (e.g. :class:`float`).

    *allow_nan*, if True (default false), will allow the parser to
    accept the non-standard floats ``NaN``, ``Infinity``, and ``-Infinity``
    and enable the use of the deprecated *parse_constant*.

    If *use_decimal* is true (default: ``False``) then it implies
    parse_float=decimal.Decimal for parity with ``dump``.

    *parse_constant*, if specified, will be
    called with one of the following strings: ``'-Infinity'``,
    ``'Infinity'``, ``'NaN'``. It is not recommended to use this feature,
    as it is rare to parse non-compliant JSON containing these values.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg. NOTE: You should use *object_hook* or *object_pairs_hook* instead
    of subclassing whenever possible.

    """
    return loads(fp.read(),
        encoding=encoding, cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook,
        use_decimal=use_decimal, allow_nan=allow_nan,
        array_hook=array_hook, **kw)


def load(__fp: IO[bytes], *, parse_float: ParseFloat = float) -> dict[str, Any]:
    """Parse TOML from a binary file object."""
    b = __fp.read()
    try:
        s = b.decode()
    except AttributeError:
        raise TypeError(
            "File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`"
        ) from None
    return loads(s, parse_float=parse_float)


def load(fp: IO[str] | IO[bytes]) -> TOMLDocument:
    """
    Load toml document from a file-like object.
    """
    return parse(fp.read())


def load(
    repo_or_dir,
    model,
    *args,
    source="github",
    trust_repo="check",
    force_reload=False,
    verbose=True,
    skip_validation=False,
    **kwargs,
):
    r"""
    Load a model from a github repo or a local directory.

    Note: Loading a model is the typical use case, but this can also be used to
    for loading other objects such as tokenizers, loss functions, etc.

    If ``source`` is 'github', ``repo_or_dir`` is expected to be
    of the form ``repo_owner/repo_name[:ref]`` with an optional
    ref (a tag or a branch).

    If ``source`` is 'local', ``repo_or_dir`` is expected to be a
    path to a local directory.

    Args:
        repo_or_dir (str): If ``source`` is 'github',
            this should correspond to a github repo with format ``repo_owner/repo_name[:ref]`` with
            an optional ref (tag or branch), for example 'pytorch/vision:0.10'. If ``ref`` is not specified,
            the default branch is assumed to be ``main`` if it exists, and otherwise ``master``.
            If ``source`` is 'local'  then it should be a path to a local directory.
        model (str): the name of a callable (entrypoint) defined in the
            repo/dir's ``hubconf.py``.
        *args (optional): the corresponding args for callable ``model``.
        source (str, optional): 'github' or 'local'. Specifies how
            ``repo_or_dir`` is to be interpreted. Default is 'github'.
        trust_repo (bool or str): ``"check"``, ``True`` or ``False``.
            This parameter was introduced in v1.12 and helps ensuring that users
            only run code from repos that they trust.

            - If ``False``, a prompt will ask the user whether the repo should
              be trusted.
            - If ``True``, the repo will be added to the trusted list and loaded
              without requiring explicit confirmation.
            - If ``"check"``, the repo will be checked against the list of
              trusted repos in the cache. If it is not present in that list, the
              behaviour will fall back onto the ``trust_repo=False`` option.

            Default is ``"check"``.
        force_reload (bool, optional): whether to force a fresh download of
            the github repo unconditionally. Does not have any effect if
            ``source = 'local'``. Default is ``False``.
        verbose (bool, optional): If ``False``, mute messages about hitting
            local caches. Note that the message about first download cannot be
            muted. Does not have any effect if ``source = 'local'``.
            Default is ``True``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the branch or commit
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
        **kwargs (optional): the corresponding kwargs for callable ``model``.

    Returns:
        The output of the ``model`` callable when called with the given
        ``*args`` and ``**kwargs``.

    Example:
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_HUB)
        >>> # from a github repo
        >>> repo = "pytorch/vision"
        >>> model = torch.hub.load(
        ...     repo, "resnet50", weights="ResNet50_Weights.IMAGENET1K_V1"
        ... )
        >>> # from a local directory
        >>> path = "/some/local/path/pytorch/vision"
        >>> # xdoctest: +SKIP
        >>> model = torch.hub.load(path, "resnet50", weights="ResNet50_Weights.DEFAULT")
    """
    source = source.lower()

    if source not in ("github", "local"):
        raise ValueError(
            f'Unknown source: "{source}". Allowed values: "github" | "local".'
        )

    if source == "github":
        repo_or_dir = _get_cache_or_reload(
            repo_or_dir,
            force_reload,
            trust_repo,
            verbose=verbose,
            skip_validation=skip_validation,
        )

    model = _load_local(repo_or_dir, model, *args, **kwargs)
    return model


def load(
    f: FileLike,
    map_location: MAP_LOCATION = None,
    pickle_module: Any = None,
    *,
    weights_only: bool | None = None,
    mmap: bool | None = None,
    **pickle_load_args: Any,
) -> Any:
    # Reference: https://github.com/pytorch/pytorch/issues/54354
    # The first line of this docstring overrides the one Sphinx generates for the
    # documentation. We need it so that Sphinx doesn't leak `pickle`s path from
    # the build environment (e.g. `<module 'pickle' from '/leaked/path').

    """load(f, map_location=None, pickle_module=pickle, *, weights_only=True, mmap=None, **pickle_load_args)

    Loads an object saved with :func:`torch.save` from a file.

    .. warning::
        :func:`torch.load()` uses an unpickler under the hood. **Never load data from an untrusted source.**

        See :ref:`weights-only-security` for more details.

    :func:`torch.load` uses Python's unpickling facilities but treats storages,
    which underlie tensors, specially. They are first deserialized on the
    CPU and are then moved to the device they were saved from. If this fails
    (e.g. because the run time system doesn't have certain devices), an exception
    is raised. However, storages can be dynamically remapped to an alternative
    set of devices using the :attr:`map_location` argument.

    If :attr:`map_location` is a callable, it will be called once for each serialized
    storage with two arguments: storage and location. The storage argument
    will be the initial deserialization of the storage, residing on the CPU.
    Each serialized storage has a location tag associated with it which
    identifies the device it was saved from, and this tag is the second
    argument passed to :attr:`map_location`. The builtin location tags are ``'cpu'``
    for CPU tensors and ``'cuda:device_id'`` (e.g. ``'cuda:2'``) for CUDA tensors.
    :attr:`map_location` should return either ``None`` or a storage. If
    :attr:`map_location` returns a storage, it will be used as the final deserialized
    object, already moved to the right device. Otherwise, :func:`torch.load` will
    fall back to the default behavior, as if :attr:`map_location` wasn't specified.

    If :attr:`map_location` is a :class:`torch.device` object or a string containing
    a device tag, it indicates the location where all tensors should be loaded.

    Otherwise, if :attr:`map_location` is a dict, it will be used to remap location tags
    appearing in the file (keys), to ones that specify where to put the
    storages (values).

    User extensions can register their own location tags and tagging and
    deserialization methods using :func:`torch.serialization.register_package`.

    See :ref:`layout-control` for more advanced tools to manipulate a checkpoint.

    Args:
        f: a file-like object (has to implement :meth:`read`, :meth:`readline`, :meth:`tell`, and :meth:`seek`),
            or a string or os.PathLike object containing a file name
        map_location: a function, :class:`torch.device`, string or a dict specifying how to remap storage
            locations
        pickle_module: module used for unpickling metadata and objects (has to
            match the :attr:`pickle_module` used to serialize file)
        weights_only: Indicates whether unpickler should be restricted to
            loading only tensors, primitive types, dictionaries
            and any types added via :func:`torch.serialization.add_safe_globals`.
            See :ref:`weights-only` for more details.
        mmap: Indicates whether the file should be mapped rather than loading all the storages into memory.
            Typically, tensor storages in the file will first be moved from disk to CPU memory, after which they
            are moved to the location that they were tagged with when saving, or specified by ``map_location``. This
            second step is a no-op if the final location is CPU. When the ``mmap`` flag is set, instead of copying the
            tensor storages from disk to CPU memory in the first step, ``f`` is mapped, which means tensor storages
            will be lazily loaded when their data is accessed.
        pickle_load_args: optional keyword arguments passed over to
            :func:`pickle_module.load` and :func:`pickle_module.Unpickler`,
            only works if :attr:`weights_only=False`, e.g., :attr:`errors=...`.

    .. note::
        When you call :func:`torch.load()` on a file which contains GPU tensors, those tensors
        will be loaded to GPU by default. You can call ``torch.load(.., map_location='cpu')``
        and then :meth:`load_state_dict` to avoid GPU RAM surge when loading a model checkpoint.

    .. note::
        By default, we decode byte strings as ``utf-8``.  This is to avoid a common error
        case ``UnicodeDecodeError: 'ascii' codec can't decode byte 0x...``
        when loading files saved by Python 2 in Python 3.  If this default
        is incorrect, you may use an extra :attr:`encoding` keyword argument to specify how
        these objects should be loaded, e.g., :attr:`encoding='latin1'` decodes them
        to strings using ``latin1`` encoding, and :attr:`encoding='bytes'` keeps them
        as byte arrays which can be decoded later with ``byte_array.decode(...)``.

    Example:
        >>> # xdoctest: +SKIP("undefined filepaths")
        >>> torch.load("tensors.pt", weights_only=True)
        # Load all tensors onto the CPU
        >>> torch.load(
        ...     "tensors.pt",
        ...     map_location=torch.device("cpu"),
        ...     weights_only=True,
        ... )
        # Load all tensors onto the CPU, using a function
        >>> torch.load(
        ...     "tensors.pt",
        ...     map_location=lambda storage, loc: storage,
        ...     weights_only=True,
        ... )
        # Load all tensors onto GPU 1
        >>> torch.load(
        ...     "tensors.pt",
        ...     map_location=lambda storage, loc: storage.cuda(1),  # type: ignore[attr-defined]
        ...     weights_only=True,
        ... )  # type: ignore[attr-defined]
        # Map tensors from GPU 1 to GPU 0
        >>> torch.load(
        ...     "tensors.pt",
        ...     map_location={"cuda:1": "cuda:0"},
        ...     weights_only=True,
        ... )
        # Load tensor from io.BytesIO object
        # Loading from a buffer setting weights_only=False, warning this can be unsafe
        >>> with open("tensor.pt", "rb") as f:
        ...     buffer = io.BytesIO(f.read())
        >>> torch.load(buffer, weights_only=False)
        # Load a module with 'ascii' encoding for unpickling
        # Loading from a module setting weights_only=False, warning this can be unsafe
        >>> torch.load("module.pt", encoding="ascii", weights_only=False)
    """
    torch._C._log_api_usage_once("torch.load")
    DOCS_MESSAGE = (
        "\n\nCheck the documentation of torch.load to learn more about types accepted by default with "
        "weights_only https://pytorch.org/docs/stable/generated/torch.load.html."
    )

    def _get_wo_message(message: str) -> str:
        unsafe_global_pattern = r"GLOBAL (\S+) was not an allowed global by default."
        has_unsafe_global = re.search(unsafe_global_pattern, message) is not None
        blocklist_pattern = r"whose module (\S+) is blocked"
        has_blocklist = re.search(blocklist_pattern, message) is not None
        import_pattern = r"(\S+) must be (\S+) to load"
        has_import = re.search(import_pattern, message) is not None
        if has_unsafe_global:
            updated_message = (
                "Weights only load failed. This file can still be loaded, to do so you have two options, "
                "\033[1mdo those steps only if you trust the source of the checkpoint\033[0m. "
                f"\n\t(1) {UNSAFE_MESSAGE}\n\t(2) Alternatively, to load with `weights_only=True` please check "
                "the recommended steps in the following error message.\n\tWeightsUnpickler error: "
                + message
            )
        else:
            if has_import:
                return f"Weights only load failed. {message}\n {UNSAFE_MESSAGE}\n"
            else:
                updated_message = f"Weights only load failed. {UNSAFE_MESSAGE}\n"
                if not has_blocklist:
                    updated_message += (
                        "Please file an issue with the following so that we can make "
                        "`weights_only=True` compatible with your use case: WeightsUnpickler error: "
                    )
            updated_message += "\n\n" + message
        return updated_message + DOCS_MESSAGE

    weights_only_not_set = weights_only is None

    if weights_only_not_set:
        weights_only = _default_to_weights_only(pickle_module)

    true_values = ["1", "y", "yes", "true"]
    # Add ability to force safe only or non-safe weight loads via environment variables
    force_weights_only_load = (
        os.getenv("TORCH_FORCE_WEIGHTS_ONLY_LOAD", "0") in true_values
    )
    force_no_weights_only_load = (
        os.getenv("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "0") in true_values
    )

    if force_weights_only_load and force_no_weights_only_load:
        raise RuntimeError(
            "Only one of `TORCH_FORCE_WEIGHTS_ONLY_LOAD` or `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD` "
            "should be set, but both were set."
        )
    elif force_weights_only_load:
        weights_only = True
    elif force_no_weights_only_load:
        # TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD can only override if callsite did not explicitly set weights_only
        if weights_only_not_set:
            warnings.warn(
                "Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the"
                "`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.",
                UserWarning,
                stacklevel=2,
            )
            weights_only = False

    if weights_only:
        if pickle_module is not None:
            raise RuntimeError(
                "Can not safely load weights when explicit pickle_module is specified"
            )
    else:
        if pickle_module is None:
            pickle_module = pickle

    if pickle_load_args != {} and weights_only:
        warnings.warn("pickle_load_args only works if `weights_only=False`.")

    # make flipping default BC-compatible
    if mmap is None:
        from torch.utils.serialization import config

        mmap = config.load.mmap

    _check_dill_version(pickle_module)

    if "encoding" not in pickle_load_args:
        pickle_load_args["encoding"] = "utf-8"

    with _open_file_like(f, "rb") as opened_file:
        if _is_zipfile(opened_file):
            # The zipfile reader is going to advance the current file position.
            # If we want to actually tail call to torch.jit.load, we need to
            # reset back to the original position.
            orig_position = opened_file.tell()
            overall_storage = None
            with _open_zipfile_reader(opened_file) as opened_zipfile:
                if _is_torchscript_zip(opened_zipfile):
                    warnings.warn(
                        "'torch.load' received a zip file that looks like a TorchScript archive"
                        " dispatching to 'torch.jit.load' (call 'torch.jit.load' directly to"
                        " silence this warning)",
                        UserWarning,
                        stacklevel=2,
                    )
                    if weights_only:
                        raise RuntimeError(
                            "Cannot use ``weights_only=True`` with TorchScript archives passed to "
                            "``torch.load``. " + UNSAFE_MESSAGE
                        )
                    opened_file.seek(orig_position)
                    return torch.jit.load(opened_file, map_location=map_location)
                if mmap:
                    if not _is_path(f):
                        raise ValueError(
                            "f must be a file path in order to use the mmap argument"
                        )
                    size = os.path.getsize(f)
                    if not IS_WINDOWS:
                        shared = get_default_mmap_options() == MAP_SHARED
                    else:
                        shared = False
                    overall_storage = torch.UntypedStorage.from_file(
                        os.fspath(f),
                        shared,
                        size,
                    )
                if weights_only:
                    try:
                        return _load(
                            opened_zipfile,
                            map_location,
                            _weights_only_unpickler,
                            overall_storage=overall_storage,
                            **pickle_load_args,
                        )
                    except pickle.UnpicklingError as e:
                        raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
                return _load(
                    opened_zipfile,
                    map_location,
                    pickle_module,
                    overall_storage=overall_storage,
                    **pickle_load_args,
                )
        if mmap:
            f_name = "" if not isinstance(f, str) else f"{f}, "
            raise RuntimeError(
                "mmap can only be used with files saved with "
                f"`torch.save({f_name}_use_new_zipfile_serialization=True), "
                "please torch.save your checkpoint with this option in order to use mmap."
            )
        if weights_only:
            try:
                return _legacy_load(
                    opened_file,
                    map_location,
                    _weights_only_unpickler,
                    **pickle_load_args,
                )
            except pickle.UnpicklingError as e:
                raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
        return _legacy_load(
            opened_file, map_location, pickle_module, **pickle_load_args
        )


def load(file, *, encoding: str = "ASCII"):
    return Unpickler(file, encoding=encoding).load()


def load(stream, Loader):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    loader = Loader(stream)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()


def load(
    f: FileLike,
    *,
    extra_files: dict[str, Any] | None = None,
    expected_opset_version: dict[str, int] | None = None,
) -> ExportedProgram:
    """

    .. warning::
        Under active development, saved files may not be usable in newer versions
        of PyTorch.

    .. warning::
        :func:`torch.export.load()` uses pickle under the hood to load models. **Never load data from an untrusted source.**

    Loads an :class:`ExportedProgram` previously saved with
    :func:`torch.export.save <torch.export.save>`.

    Args:
        f (str | os.PathLike[str] | IO[bytes]): A file-like object (has to
         implement write and flush) or a string containing a file name.

        extra_files (Optional[Dict[str, Any]]): The extra filenames given in
         this map would be loaded and their content would be stored in the
         provided map.

        expected_opset_version (Optional[Dict[str, int]]): A map of opset names
         to expected opset versions

    Returns:
        An :class:`ExportedProgram` object

    Example::

        import torch
        import io

        # Load ExportedProgram from file
        ep = torch.export.load("exported_program.pt2")

        # Load ExportedProgram from io.BytesIO object
        with open("exported_program.pt2", "rb") as f:
            buffer = io.BytesIO(f.read())
        buffer.seek(0)
        ep = torch.export.load(buffer)

        # Load with extra files.
        extra_files = {"foo.txt": ""}  # values will be replaced with data
        ep = torch.export.load("exported_program.pt2", extra_files=extra_files)
        print(extra_files["foo.txt"])
        print(ep(torch.randn(5)))
    """
    if isinstance(f, (str, os.PathLike)):
        f = os.fspath(f)

    extra_files = extra_files or {}

    from torch.export.pt2_archive._package import load_pt2, PT2ArchiveContents

    try:
        pt2_contents = load_pt2(
            f,
            expected_opset_version=expected_opset_version,
        )
    except RuntimeError:
        log.warning("Ran into the following error when deserializing", exc_info=True)
        pt2_contents = PT2ArchiveContents({}, {}, {})

    if len(pt2_contents.exported_programs) > 0 or len(pt2_contents.extra_files) > 0:
        for k, v in pt2_contents.extra_files.items():
            extra_files[k] = v

        return pt2_contents.exported_programs["model"]

    # TODO: For backward compatibility, we support loading a zip file from 2.7. Delete this path in 2.9(?)
    with zipfile.ZipFile(f, "r") as zipf:
        if "version" not in zipf.namelist():
            raise RuntimeError(
                "We ran into an error when deserializing the saved file. "
                "Please check the warnings above for possible errors. "
            )

        log.warning(
            "Trying to deserialize for the older format. This version of file is "
            "deprecated. Please generate a new pt2 saved file."
        )

        # Check the version
        version = zipf.read("version").decode().split(".")
        from torch._export.serde.schema import (
            SCHEMA_VERSION,  # todo change archive version to schema version
        )

        if len(version) != len(SCHEMA_VERSION):
            raise AssertionError(
                "Version in the saved file has incorrect length, double check if the file is generated by torch.export.save()"
            )
        if version[0] != str(SCHEMA_VERSION[0]):
            raise RuntimeError(
                f"Serialized version {version} does not match our current "
                f"schema version {SCHEMA_VERSION}."
            )

        from torch._export.serde.serialize import deserialize, SerializedArtifact

        # Load serialized_ep and serialized_state_dict from the zip file

        serialized_exported_program: bytes | None = None
        serialized_state_dict: bytes | None = None
        serialized_constants: bytes | None = None
        serialized_example_inputs: bytes | None = None

        for file_info in zipf.infolist():
            file_content = zipf.read(file_info.filename)

            if file_info.filename == "serialized_exported_program.json":
                serialized_exported_program = file_content
            elif file_info.filename == "serialized_state_dict.json":
                warnings.warn("This version of file is deprecated", stacklevel=2)
                serialized_state_dict = file_content
            elif file_info.filename == "serialized_constants.json":
                warnings.warn("This version of file is deprecated", stacklevel=2)
                serialized_constants = file_content
            elif file_info.filename == "serialized_state_dict.pt":
                serialized_state_dict = file_content
            elif file_info.filename == "serialized_constants.pt":
                serialized_constants = file_content
            elif file_info.filename == "serialized_example_inputs.pt":
                serialized_example_inputs = file_content
            elif file_info.filename.startswith("extra_files"):
                filename = file_info.filename.split("/", 1)[1]
                extra_files[filename] = file_content.decode("utf-8")

        if serialized_exported_program is None:
            raise AssertionError("serialized_exported_program is None")
        if serialized_state_dict is None:
            raise AssertionError("serialized_state_dict is None")
        if serialized_constants is None:
            raise AssertionError("serialized_constants is None")
        if serialized_example_inputs is None:
            raise AssertionError("serialized_example_inputs is None")
        artifact: SerializedArtifact = SerializedArtifact(
            serialized_exported_program,
            serialized_state_dict,
            serialized_constants,
            serialized_example_inputs,
        )

        # Deserialize ExportedProgram
        ep = deserialize(artifact, expected_opset_version)

        return ep


def load(f, map_location=None, _extra_files=None, _restore_shapes=False):
    r"""
    Load a :class:`ScriptModule` or :class:`ScriptFunction` previously saved with :func:`torch.jit.save <torch.jit.save>`.

    All previously saved modules, no matter their device, are first loaded onto CPU,
    and then are moved to the devices they were saved from. If this fails (e.g.
    because the run time system doesn't have certain devices), an exception is
    raised.

    Args:
        f: a file-like object (has to implement read, readline, tell, and seek),
            or a string containing a file name
        map_location (string or torch.device): A simplified version of
            ``map_location`` in `torch.jit.save` used to dynamically remap
            storages to an alternative set of devices.
        _extra_files (dictionary of filename to content): The extra
            filenames given in the map would be loaded and their content
            would be stored in the provided map.
        _restore_shapes (bool): Whether or not to retrace the module on load using stored inputs

    Returns:
        A :class:`ScriptModule` object.

    .. warning::
        It is possible to construct malicious pickle data which will execute arbitrary code
        during func:`torch.jit.load`. Never load data that could have come from an untrusted
        source, or that could have been tampered with. **Only load data you trust**.

    Example:
    .. testcode::

        import torch
        import io

        torch.jit.load('scriptmodule.pt')

        # Load ScriptModule from io.BytesIO object
        with open('scriptmodule.pt', 'rb') as f:
            buffer = io.BytesIO(f.read())

        # Load all tensors to the original device
        torch.jit.load(buffer)

        # Load all tensors onto CPU, using a device
        buffer.seek(0)
        torch.jit.load(buffer, map_location=torch.device('cpu'))

        # Load all tensors onto CPU, using a string
        buffer.seek(0)
        torch.jit.load(buffer, map_location='cpu')

        # Load with extra files.
        extra_files = {'foo.txt': ''}  # values will be replaced with data
        torch.jit.load('scriptmodule.pt', _extra_files=extra_files)
        print(extra_files['foo.txt'])

    .. testoutput::
        :hide:

        ...

    .. testcleanup::

        import os
        os.remove("scriptmodule.pt")
    """
    if sys.version_info >= (3, 14):
        warnings.warn(
            "`torch.jit.load` is not supported in Python 3.14+ and may break. "
            "Please switch to `torch.export`.",
            DeprecationWarning,
        )
    else:
        warnings.warn(
            "`torch.jit.load` is deprecated. Please switch to `torch.export`.",
            DeprecationWarning,
        )
    if isinstance(f, (str, os.PathLike)):
        if not os.path.exists(f):
            raise ValueError(f"The provided filename {f} does not exist")
        if os.path.isdir(f):
            raise ValueError(f"The provided filename {f} is a directory")

    map_location = validate_map_location(map_location)
    if _extra_files is None:
        _extra_files = {}

    cu = torch._C.CompilationUnit()
    if isinstance(f, (str, os.PathLike)):
        cpp_module = torch._C.import_ir_module(
            cu,
            os.fspath(f),
            map_location,
            _extra_files,
            # pyrefly: ignore [bad-argument-count]
            _restore_shapes,
        )  # type: ignore[call-arg]
    else:
        cpp_module = torch._C.import_ir_module_from_buffer(
            cu,
            f.read(),
            map_location,
            _extra_files,
            # pyrefly: ignore [bad-argument-count]
            _restore_shapes,
        )  # type: ignore[call-arg]

    # TODO: Pretty sure this approach loses ConstSequential status and such
    ret = wrap_cpp_module(cpp_module)
    log_torchscript_usage("load", model_id=_get_model_id(ret))
    return ret


def load(name,
         sources: str | list[str],
         extra_cflags=None,
         extra_cuda_cflags=None,
         extra_sycl_cflags=None,
         extra_ldflags=None,
         extra_include_paths=None,
         build_directory=None,
         verbose=False,
         with_cuda: bool | None = None,
         with_sycl: bool | None = None,
         is_python_module=True,
         is_standalone=False,
         keep_intermediates=True):
    """
    Load a PyTorch C++ extension just-in-time (JIT).

    To load an extension, a Ninja build file is emitted, which is used to
    compile the given sources into a dynamic library. This library is
    subsequently loaded into the current Python process as a module and
    returned from this function, ready for use.

    By default, the directory to which the build file is emitted and the
    resulting library compiled to is ``<tmp>/torch_extensions/<name>``, where
    ``<tmp>`` is the temporary folder on the current platform and ``<name>``
    the name of the extension. This location can be overridden in two ways.
    First, if the ``TORCH_EXTENSIONS_DIR`` environment variable is set, it
    replaces ``<tmp>/torch_extensions`` and all extensions will be compiled
    into subfolders of this directory. Second, if the ``build_directory``
    argument to this function is supplied, it overrides the entire path, i.e.
    the library will be compiled into that folder directly.

    To compile the sources, the default system compiler (``c++``) is used,
    which can be overridden by setting the ``CXX`` environment variable. To pass
    additional arguments to the compilation process, ``extra_cflags`` or
    ``extra_ldflags`` can be provided. For example, to compile your extension
    with optimizations, pass ``extra_cflags=['-O3']``. You can also use
    ``extra_cflags`` to pass further include directories.

    CUDA support with mixed compilation is provided. Simply pass CUDA source
    files (``.cu`` or ``.cuh``) along with other sources. Such files will be
    detected and compiled with nvcc rather than the C++ compiler. This includes
    passing the CUDA lib64 directory as a library directory, and linking
    ``cudart``. You can pass additional flags to nvcc via
    ``extra_cuda_cflags``, just like with ``extra_cflags`` for C++. Various
    heuristics for finding the CUDA install directory are used, which usually
    work fine. If not, setting the ``CUDA_HOME`` environment variable is the
    safest option.

    SYCL support with mixed compilation is provided. Simply pass SYCL source
    files (``.sycl``) along with other sources. Such files will be detected
    and compiled with SYCL compiler (such as Intel DPC++ Compiler) rather
    than the C++ compiler. You can pass additional flags to SYCL compiler
    via ``extra_sycl_cflags``, just like with ``extra_cflags`` for C++.
    SYCL compiler is expected to be found via system PATH environment
    variable.

    Args:
        name: The name of the extension to build. This MUST be the same as the
            name of the pybind11 module!
        sources: A list of relative or absolute paths to C++ source files.
        extra_cflags: optional list of compiler flags to forward to the build.
        extra_cuda_cflags: optional list of compiler flags to forward to nvcc
            when building CUDA sources.
        extra_sycl_cflags: optional list of compiler flags to forward to SYCL
            compiler when building SYCL sources.
        extra_ldflags: optional list of linker flags to forward to the build.
        extra_include_paths: optional list of include directories to forward
            to the build.
        build_directory: optional path to use as build workspace.
        verbose: If ``True``, turns on verbose logging of load steps.
        with_cuda: Determines whether CUDA headers and libraries are added to
            the build. If set to ``None`` (default), this value is
            automatically determined based on the existence of ``.cu`` or
            ``.cuh`` in ``sources``. Set it to `True`` to force CUDA headers
            and libraries to be included.
        with_sycl: Determines whether SYCL headers and libraries are added to
            the build. If set to ``None`` (default), this value is
            automatically determined based on the existence of ``.sycl`` in
            ``sources``. Set it to `True`` to force SYCL headers and
            libraries to be included.
        is_python_module: If ``True`` (default), imports the produced shared
            library as a Python module. If ``False``, behavior depends on
            ``is_standalone``.
        is_standalone: If ``False`` (default) loads the constructed extension
            into the process as a plain dynamic library. If ``True``, build a
            standalone executable.

    Returns:
        If ``is_python_module`` is ``True``:
            Returns the loaded PyTorch extension as a Python module.

        If ``is_python_module`` is ``False`` and ``is_standalone`` is ``False``:
            Returns nothing. (The shared library is loaded into the process as
            a side effect.)

        If ``is_standalone`` is ``True``.
            Return the path to the executable. (On Windows, TORCH_LIB_PATH is
            added to the PATH environment variable as a side effect.)

    Example:
        >>> # xdoctest: +SKIP
        >>> from torch.utils.cpp_extension import load
        >>> module = load(
        ...     name='extension',
        ...     sources=['extension.cpp', 'extension_kernel.cu'],
        ...     extra_cflags=['-O2'],
        ...     verbose=True)
    """
    return _jit_compile(
        name,
        [sources] if isinstance(sources, str) else sources,
        extra_cflags,
        extra_cuda_cflags,
        extra_sycl_cflags,
        extra_ldflags,
        extra_include_paths,
        build_directory or _get_build_directory(name, verbose),
        verbose,
        with_cuda,
        with_sycl,
        is_python_module,
        is_standalone,
        keep_intermediates=keep_intermediates)


def load(
    state_dict: dict[str, Any],
    *,
    checkpoint_id: str | os.PathLike | None = None,
    storage_reader: StorageReader | None = None,
    planner: LoadPlanner | None = None,
    process_group: dist.ProcessGroup | None = None,
    no_dist: bool = False,
) -> None:
    """
    Load a checkpoint into a distributed state dict in SPMD style.

    Each rank must have the same keys in their ``state_dict`` provided to this
    API. Mismatched keys may result in hangs or errors. If unsure, you can use
    the ``utils._assert_same_keys`` API to check (but may incur communication
    costs).

    Each rank will try to read the least amount of data necessary
    to fulfill the requested `state_dict`. When loading :class:`ShardedTensor`
    or :class:`DTensor` instances, each rank only reads data for their local shards.

    For each ``Stateful`` object (having both a ``state_dict`` and a ``load_state_dict``),
    load will first call ``state_dict`` before attempting deserialization, followed by
    ``load_state_dict`` once the deserialization is complete.
    For each non-``Stateful`` object, load will deserialize the object, and then replace
    it in the ``state_dict`` with the deserialized object.

    .. warning::
        All tensors in ``state_dict`` must be allocated on their
        destination device *prior to* calling this function.

        All non-tensor data is loaded using `torch.load()` and modified in place
        on state_dict.

    .. warning::
        Users must call `load_state_dict` on the root module to ensure load
        pos-processing and non-tensor data properly propagates.

    .. note:
        If no process group is initialized, this function will assume the intent
        is to load a checkpoint into the local process. This can be useful in the
        case of local inference, and when using regular Tensors (as opposed to DTensor
         or ShardedTensor)

    .. note:
        Rank 0 is assumed to be the coordinator rank.

    Args:
        state_dict (Dict[str, Any]): The state_dict to load the checkpoint into.
        checkpoint_id (Union[str, os.PathLike, None]):
            The ID of this checkpoint instance. The meaning of the checkpoint_id
            depends on the storage. It can be a path to a folder or to a file.
            It can also be a key if the storage is a key-value store.
            (Default: ``None``)
        storage_reader (Optional[StorageReader]):
            Instance of StorageWriter used to perform reads. If this is not
            specified, DCP will automatically infer the reader based on the
            checkpoint_id. If checkpoint_id is also None, an exception will
            be raised. (Default: ``None``)
        planner (Optional[LoadPlanner]):
            Instance of LoadPlanner. If this is not specified, the default
            planner will be used. (Default: ``None``)
        process_group (Optional[ProcessGroup]):
            ProcessGroup to be used for cross-rank synchronization.
            (Default: ``None``)
        no_dist (bool): If ``True``, this function will assume the intent is to load
            a checkpoint without using cross-rank synchronization. (Default: ``False``)
    Returns:
        None.

    Examples
        >>> # xdoctest: +SKIP
        >>> my_model = MyModule()
        >>> optimizer = Adagrad(my_model.parameters())
        >>> model_state_dict = my_model.state_dict()
        >>> fs_storage_reader = torch.distributed.checkpoint.FileSystemReader(
        ...     "/checkpoint/1"
        ... )

        >>> torch.distributed.checkpoint.load_state_dict(
        >>>     state_dict=model_state_dict,
        >>>     storage_reader=fs_storage_reader,
        >>> )

        >>> # module.load_state_dict() function might have customized steps
        >>> # to flush the state_dict, must call it to
        >>> # ensure correct behavior.
        >>> my_model.load_state_dict(model_state_dict)

    .. note::
        load_state_dict uses collectives to coordinate reads across ranks.
        For NCCL-based process groups, internal tensor representations of
        objects must be moved to the GPU device before communication takes place.
        In this case, the device used is given by ``torch.cuda.current_device()``
        and it is the user's responsibility to ensure that this is set so that each
        rank has an individual GPU, via ``torch.cuda.set_device()``.
    """

    no_dist = no_dist or (not dist.is_available()) or (not dist.is_initialized())
    if no_dist:
        warnings.warn(
            "torch.distributed is disabled, unavailable or uninitialized, assuming the intent is to load in a single process.",
            stacklevel=2,
        )

    with _profile():
        storage_reader = cast(
            StorageReader, _storage_setup(storage_reader, checkpoint_id, reader=True)
        )

        # All ranks must have the same keys in their `state_dict` provided to
        # this API.  See documentation for more details.
        # Here we simply sort the keys to ensure that all ranks load values in
        # the same order.
        keys = sorted(state_dict.keys())

        stateful_sd = {}
        for key in keys:
            if key not in state_dict:
                continue
            elem = state_dict[key]
            stateful_sd[key] = elem.state_dict() if isinstance(elem, Stateful) else elem

        _load_state_dict(
            state_dict=stateful_sd,
            storage_reader=storage_reader,
            process_group=process_group,
            no_dist=no_dist,
            planner=planner,
        )
        for key in keys:
            if key not in state_dict:
                continue
            elem = state_dict[key]
            if isinstance(elem, Stateful):
                # If the state_dict is a Stateful object,
                # DCP does an in-place load in the original state dict.
                elem.load_state_dict(stateful_sd[key])
            else:
                # Otherwise, replace the state_dict with the loaded state_dict.
                state_dict[key] = stateful_sd[key]


def load(s):
    """Loads a boolean expression from a string.

    Examples
    ========

    >>> from sympy.logic.utilities.dimacs import load
    >>> load('1')
    cnf_1
    >>> load('1 2')
    cnf_1 | cnf_2
    >>> load('1 \\n 2')
    cnf_1 & cnf_2
    >>> load('1 2 \\n 3')
    cnf_3 & (cnf_1 | cnf_2)
    """
    clauses = []

    lines = s.split('\n')

    pComment = re.compile(r'c.*')
    pStats = re.compile(r'p\s*cnf\s*(\d*)\s*(\d*)')

    while len(lines) > 0:
        line = lines.pop(0)

        # Only deal with lines that aren't comments
        if not pComment.match(line):
            m = pStats.match(line)

            if not m:
                nums = line.rstrip('\n').split(' ')
                list = []
                for lit in nums:
                    if lit != '':
                        if int(lit) == 0:
                            continue
                        num = abs(int(lit))
                        sign = True
                        if int(lit) < 0:
                            sign = False

                        if sign:
                            list.append(Symbol("cnf_%s" % num))
                        else:
                            list.append(~Symbol("cnf_%s" % num))

                if len(list) > 0:
                    clauses.append(Or(*list))

    return And(*clauses)


def load(__fp: IO[bytes], *, parse_float: ParseFloat = float) -> dict[str, Any]:
    """Parse TOML from a binary file object."""
    b = __fp.read()
    try:
        s = b.decode()
    except AttributeError:
        raise TypeError(
            "File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`"
        ) from None
    return loads(s, parse_float=parse_float)


def load(unicode_version: str = "auto") -> CellTable:
    """Load a cell table for the given unicode version.

    Args:
        unicode_version: Unicode version, or `None` to auto-detect.

    """
    if unicode_version == "auto":
        unicode_version = os.environ.get("UNICODE_VERSION", "latest")
        try:
            _parse_version(unicode_version)
        except ValueError:
            # The environment variable is invalid
            # Fallback to using the latest version seems reasonable
            unicode_version = "latest"

    if unicode_version == "latest":
        version = VERSIONS[-1]
    else:
        try:
            version_numbers = _parse_version(unicode_version)
        except ValueError:
            version_numbers = _parse_version(VERSIONS[-1])
        major, minor, patch = version_numbers
        version = f"{major}.{minor}.{patch}"
        if version not in VERSION_SET:
            insert_position = bisect.bisect_left(VERSION_ORDER, version_numbers)
            version = VERSIONS[max(0, insert_position - 1)]

    version_path_component = version.replace(".", "-")
    module_name = f".unicode{version_path_component}"
    module = import_module(module_name, "rich._unicode_data")
    if TYPE_CHECKING:
        assert isinstance(module.cell_table, CellTable)
    return module.cell_table


def load(__fp: BinaryIO, *, parse_float: ParseFloat = float) -> dict[str, Any]:
    """Parse TOML from a binary file object."""
    b = __fp.read()
    try:
        s = b.decode()
    except AttributeError:
        raise TypeError(
            "File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`"
        ) from None
    return loads(s, parse_float=parse_float)


def load(__fp: IO[bytes], *, parse_float: ParseFloat = float) -> dict[str, Any]:
    """Parse TOML from a binary file object."""
    b = __fp.read()
    try:
        s = b.decode()
    except AttributeError:
        raise TypeError(
            "File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`"
        ) from None
    return loads(s, parse_float=parse_float)


def load(
    path: path_types.PathLike,
    abstract_state: (
        AbstractPyTree | CheckpointMetadata[AbstractPyTree] | None
    ) = None,
    *,
    checkpointable_name: str | None = AUTO_CHECKPOINTABLE_KEY,
) -> tree_types.PyTreeOf[tree_types.Leaf]:
  """Loads a PyTree.

  Loads from a `PyTree` checkpoint. A `PyTree` checkpoint must be a path
  containing a subdirectory with the name provided by `checkpointable_name`,
  with default value `AUTO`. See `checkpointable_name` for more details.

  This function must be called on all available controller processes.

  The operation blocks until complete. For improved performance, consider using
  :py:func:`.load_async` instead.

  If `abstract_state` is not provided, the `PyTree` will be loaded exactly as
  saved.

  IMPORTANT: Loading is more brittle and error-prone when not providing
  `abstract_state`. Always provide `abstract_state` if possible. Note that
  you can always obtain the tree structure from a saved checkpoint using
  :py:func:`.metadata`.

  Providing the `abstract_state` guarantees two things:

  1. The restored tree will exactly match the structure of `abstract_state` (or
  raise an error if it is impossible to guarantee this). For example, if
  `abstract_state` is a custom object registered as a `PyTree`, the checkpoint
  will be restored as the same object, if possible.

  2. The leaves of the restored tree will be restored with the properties
  indicated by the abstract leaves. For example, if a leaf in `abstract_state`
  is a `jax.ShapeDtypeStruct`, the restored leaf will be a `jax.Array` with the
  same shape and `dtype`. Each `AbstractLeaf` has a corresponding `Leaf`
  that is restored. See `orbax.checkpoint.v1.tree` for a table
  of standard supported leaf types.

  Example Usage:

    Load a saved PyTree with and without providing its abstract structure::

      path = '/tmp/my_checkpoint'

      # Save a checkpoint
      state = {'a': jnp.arange(8), 'b': jnp.zeros(4)}
      ocp.save(path, state)

      # Load the checkpoint
      # Highly recommended to provide the abstract pytree (structure/shapes)
      abstract_state = jax.eval_shape(lambda: state)

      # Method A: Load using the abstract structure.
      # This automatically looks for the 'pytree' subdirectory inside 'path'.
      restored = ocp.load(path, abstract_state)

      # Method B: Infer structure from file (Not recommended for production use)
      # cases or for complex trees.
      restored_inferred = ocp.load(path)

  Args:
    path: The path to load the checkpoint from. This path must contain a
      subdirectory with name provided by `checkpointable_name`. See
      `checkpointable_name` for more details.
    abstract_state: Provides a tree structure for the checkpoint to be restored
      into. May be omitted to load exactly as saved, but this is much more
      brittle than providing the tree.
    checkpointable_name: The name of the checkpointable to load. A subdirectory
      with this name must exist in `path`. If None, then path itself is expected
      to contain all files relevant for loading the PyTree, rather than any
      subdirectory. Such files include, for example, `manifest.ocdbt`,
      `_METADATA`, `ocp.process_X`. Defaults to `AUTO`. Setting to `AUTO` mode
      dynamically discovers and resolves a pytree checkpointable. It prioritizes
      the standard 'pytree' checkpointable name if present, then sorts any other
      valid pytree checkpointable names alphabetically and returns the first
      valid one, and ultimately falls back to interpreting the path as a flat V0
      root layout if no standard pytree exists.

  Returns:
    The restored `PyTree`.
  """
  start_time = time.time()
  event_tracking.OperationRecorder(
      path,
      operation_type=event_tracking.OperationType.LOAD,
      async_origin=False,
  ).record_start(start_time)

  abstract_state = _standardize_abstract_checkpointables(abstract_state)
  validation.validate_state_checkpointable_name(checkpointable_name)
  validation.validate_abstract_state(abstract_state)

  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)

  resolver = asyncio_utils.run_sync(
      layout_registry.CheckpointLayoutResolver.resolve(
          path, ctx.checkpoint_layout, pytree_name=checkpointable_name
      )
  )
  loaded_pytree = _load_impl(
      path,
      functools.partial(
          resolver.layout.load,
          path=path,
          checkpointable_name=resolver.pytree_name,
          abstract_state=abstract_state,
      ),
      start_time=start_time,
  )

  return loaded_pytree


def load(file, mmap_mode=None, allow_pickle=False, fix_imports=True,
         encoding='ASCII', *, max_header_size=_MAX_HEADER_SIZE):
    """
    Load arrays or pickled objects from ``.npy``, ``.npz`` or pickled files.

    .. warning:: Loading files that contain object arrays uses the ``pickle``
                 module, which is not secure against erroneous or maliciously
                 constructed data. Consider passing ``allow_pickle=False`` to
                 load data that is known not to contain object arrays for the
                 safer handling of untrusted sources.

    Parameters
    ----------
    file : file-like object, string, or pathlib.Path
        The file to read. File-like objects must support the
        ``seek()`` and ``read()`` methods and must always
        be opened in binary mode.  Pickled files require that the
        file-like object support the ``readline()`` method as well.
    mmap_mode : {None, 'r+', 'r', 'w+', 'c'}, optional
        If not None, then memory-map the file, using the given mode (see
        `numpy.memmap` for a detailed description of the modes).  A
        memory-mapped array is kept on disk. However, it can be accessed
        and sliced like any ndarray.  Memory mapping is especially useful
        for accessing small fragments of large files without reading the
        entire file into memory.
    allow_pickle : bool, optional
        Allow loading pickled object arrays stored in npy files. Reasons for
        disallowing pickles include security, as loading pickled data can
        execute arbitrary code. If pickles are disallowed, loading object
        arrays will fail. Default: False
    fix_imports : bool, optional
        Only useful when loading Python 2 generated pickled files,
        which includes npy/npz files containing object arrays. If `fix_imports`
        is True, pickle will try to map the old Python 2 names to the new names
        used in Python 3.
    encoding : str, optional
        What encoding to use when reading Python 2 strings. Only useful when
        loading Python 2 generated pickled files, which includes
        npy/npz files containing object arrays. Values other than 'latin1',
        'ASCII', and 'bytes' are not allowed, as they can corrupt numerical
        data. Default: 'ASCII'
    max_header_size : int, optional
        Maximum allowed size of the header.  Large headers may not be safe
        to load securely and thus require explicitly passing a larger value.
        See :py:func:`ast.literal_eval()` for details.
        This option is ignored when `allow_pickle` is passed.  In that case
        the file is by definition trusted and the limit is unnecessary.

    Returns
    -------
    result : array, tuple, dict, etc.
        Data stored in the file. For ``.npz`` files, the returned instance
        of NpzFile class must be closed to avoid leaking file descriptors.

    Raises
    ------
    OSError
        If the input file does not exist or cannot be read.
    UnpicklingError
        If ``allow_pickle=True``, but the file cannot be loaded as a pickle.
    ValueError
        The file contains an object array, but ``allow_pickle=False`` given.
    EOFError
        When calling ``np.load`` multiple times on the same file handle,
        if all data has already been read

    See Also
    --------
    save, savez, savez_compressed, loadtxt
    memmap : Create a memory-map to an array stored in a file on disk.
    lib.format.open_memmap : Create or load a memory-mapped ``.npy`` file.

    Notes
    -----
    - If the file contains pickle data, then whatever object is stored
      in the pickle is returned.
    - If the file is a ``.npy`` file, then a single array is returned.
    - If the file is a ``.npz`` file, then a dictionary-like object is
      returned, containing ``{filename: array}`` key-value pairs, one for
      each file in the archive.
    - If the file is a ``.npz`` file, the returned value supports the
      context manager protocol in a similar fashion to the open function::

        with load('foo.npz') as data:
            a = data['a']

      The underlying file descriptor is closed when exiting the 'with'
      block.

    Examples
    --------
    >>> import numpy as np

    Store data to disk, and load it again:

    >>> np.save('/tmp/123', np.array([[1, 2, 3], [4, 5, 6]]))
    >>> np.load('/tmp/123.npy')
    array([[1, 2, 3],
           [4, 5, 6]])

    Store compressed data to disk, and load it again:

    >>> a=np.array([[1, 2, 3], [4, 5, 6]])
    >>> b=np.array([1, 2])
    >>> np.savez('/tmp/123.npz', a=a, b=b)
    >>> data = np.load('/tmp/123.npz')
    >>> data['a']
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> data['b']
    array([1, 2])
    >>> data.close()

    Mem-map the stored array, and then access the second row
    directly from disk:

    >>> X = np.load('/tmp/123.npy', mmap_mode='r')
    >>> X[1, :]
    memmap([4, 5, 6])

    """
    if encoding not in ('ASCII', 'latin1', 'bytes'):
        # The 'encoding' value for pickle also affects what encoding
        # the serialized binary data of NumPy arrays is loaded
        # in. Pickle does not pass on the encoding information to
        # NumPy. The unpickling code in numpy._core.multiarray is
        # written to assume that unicode data appearing where binary
        # should be is in 'latin1'. 'bytes' is also safe, as is 'ASCII'.
        #
        # Other encoding values can corrupt binary data, and we
        # purposefully disallow them. For the same reason, the errors=
        # argument is not exposed, as values other than 'strict'
        # result can similarly silently corrupt numerical data.
        raise ValueError("encoding must be 'ASCII', 'latin1', or 'bytes'")

    pickle_kwargs = {'encoding': encoding, 'fix_imports': fix_imports}

    with contextlib.ExitStack() as stack:
        if hasattr(file, 'read'):
            fid = file
            own_fid = False
        else:
            fid = stack.enter_context(open(os.fspath(file), "rb"))
            own_fid = True

        # Code to distinguish from NumPy binary files and pickles.
        _ZIP_PREFIX = b'PK\x03\x04'
        _ZIP_SUFFIX = b'PK\x05\x06'  # empty zip files start with this
        N = len(format.MAGIC_PREFIX)
        magic = fid.read(N)
        if not magic:
            raise EOFError("No data left in file")
        # If the file size is less than N, we need to make sure not
        # to seek past the beginning of the file
        fid.seek(-min(N, len(magic)), 1)  # back-up
        if magic.startswith((_ZIP_PREFIX, _ZIP_SUFFIX)):
            # zip-file (assume .npz)
            # Potentially transfer file ownership to NpzFile
            stack.pop_all()
            ret = NpzFile(fid, own_fid=own_fid, allow_pickle=allow_pickle,
                          pickle_kwargs=pickle_kwargs,
                          max_header_size=max_header_size)
            return ret
        elif magic == format.MAGIC_PREFIX:
            # .npy file
            if mmap_mode:
                if allow_pickle:
                    max_header_size = 2**64
                return format.open_memmap(file, mode=mmap_mode,
                                          max_header_size=max_header_size)
            else:
                return format.read_array(fid, allow_pickle=allow_pickle,
                                         pickle_kwargs=pickle_kwargs,
                                         max_header_size=max_header_size)
        else:
            # Try a pickle
            if not allow_pickle:
                raise ValueError(
                    "This file contains pickled (object) data. If you trust "
                    "the file you can load it unsafely using the "
                    "`allow_pickle=` keyword argument or `pickle.load()`.")
            try:
                return pickle.load(fid, **pickle_kwargs)
            except Exception as e:
                raise pickle.UnpicklingError(
                    f"Failed to interpret file {file!r} as a pickle") from e


def load(ptr: _ods_ir.Value, *, mask: _Optional[_ods_ir.Value] = None, other: _Optional[_ods_ir.Value] = None, cache: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, evict: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, is_volatile: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LoadOp(ptr=ptr, mask=mask, other=other, cache=cache, evict=evict, isVolatile=is_volatile, results=results, loc=loc, ip=ip).result


def load(result: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], sublane_mask: _Union[_Sequence[bool], _ods_ir.DenseBoolArrayAttr], *, sublane_stride: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return LoadOp(result=result, base=base, indices=indices, sublane_mask=sublane_mask, sublane_stride=sublane_stride, loc=loc, ip=ip).result


def load(res: _ods_ir.Type, addr: _ods_ir.Value, *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, volatile_: _Optional[bool] = None, nontemporal: _Optional[bool] = None, invariant: _Optional[bool] = None, invariant_group: _Optional[bool] = None, ordering: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, syncscope: _Optional[_Union[str, _ods_ir.StringAttr]] = None, dereferenceable: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, access_groups: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, alias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, noalias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, tbaa: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LoadOp(res=res, addr=addr, alignment=alignment, volatile_=volatile_, nontemporal=nontemporal, invariant=invariant, invariantGroup=invariant_group, ordering=ordering, syncscope=syncscope, dereferenceable=dereferenceable, access_groups=access_groups, alias_scopes=alias_scopes, noalias_scopes=noalias_scopes, tbaa=tbaa, loc=loc, ip=ip).result


def load(memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, nontemporal: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LoadOp(memref=memref, indices=indices, nontemporal=nontemporal, alignment=alignment, results=results, loc=loc, ip=ip).result


def load(tensor: _ods_ir.Value[_ods_ir.RankedTensorType], *, has_inserts: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LoadOp(tensor=tensor, hasInserts=has_inserts, results=results, loc=loc, ip=ip).result


def load(result: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, nontemporal: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return LoadOp(result=result, base=base, indices=indices, nontemporal=nontemporal, alignment=alignment, loc=loc, ip=ip).result


def load(file: IO[bytes] | str | os.PathLike[Any], *args: Any, **kwargs: Any) -> Array:
  """Load JAX arrays from npy files.

  JAX wrapper of :func:`numpy.load`.

  This function is a simple wrapper of :func:`numpy.load`, but in the case of
  ``.npy`` files created with :func:`numpy.save` or :func:`jax.numpy.save`,
  the output will be returned as a :class:`jax.Array`, and ``bfloat16`` data
  types will be restored. For ``.npz`` files, results will be returned as
  normal NumPy arrays.

  This function requires concrete array inputs, and is not compatible with
  transformations like :func:`jax.jit` or :func:`jax.vmap`.

  Args:
    file: string, bytes, or path-like object containing the array data.
    args, kwargs: for additional arguments, see :func:`numpy.load`

  Returns:
    the array stored in the file.

  See also:
    - :func:`jax.numpy.save`: save an array to a file.

  Examples:
    >>> import io
    >>> f = io.BytesIO()  # use an in-memory file-like object.
    >>> x = jnp.array([2, 4, 6, 8], dtype='bfloat16')
    >>> jnp.save(f, x)
    >>> f.seek(0)
    0
    >>> jnp.load(f)
    Array([2, 4, 6, 8], dtype=bfloat16)
  """
  # The main purpose of this wrapper is to recover bfloat16 data types.
  # Note: this will only work for files created via np.save(), not np.savez().
  out = np.load(file, *args, **kwargs)
  if isinstance(out, np.ndarray):
    # numpy does not recognize bfloat16, so arrays are serialized as void16
    if out.dtype == 'V2':
      out = out.view(dtypes.bfloat16)
    try:
      out = asarray(out)
    except (TypeError, AssertionError):  # Unsupported dtype
      pass
  return out


def load(x_ref_or_view, idx, *, mask=None, other=None, cache_modifier=None,
         eviction_policy=None, volatile=False) -> jax_typing.Array:
  """Returns an array loaded from the given index.

  If neither ``mask`` nor ``other`` is specified, this function has the same
  semantics as ``x_ref_or_view[idx]`` in JAX.

  Args:
    x_ref_or_view: The ref to load from.
    idx: The indexer to use.
    mask: An optional boolean mask specifying which indices to load.
      If mask is ``False`` and ``other`` is not given, no assumptions can
      be made about the value in the resulting array.
    other: An optional value to use for indices where mask is ``False``.
    cache_modifier: TO BE DOCUMENTED.
    eviction_policy: TO BE DOCUMENTED.
    volatile: TO BE DOCUMENTED.
  """
  x_ref, transforms = sp.get_ref_and_transforms(x_ref_or_view, idx, "load")
  args_flat, args_tree = tree_util.tree_flatten(
      (x_ref, transforms, mask, other)
  )
  return load_p.bind(
      *args_flat,
      args_tree=args_tree,
      cache_modifier=cache_modifier,
      eviction_policy=eviction_policy,
      is_volatile=volatile,
  )


def load(ref: Ref, *, mask: jax.Array | None = None) -> jax.Array:
  """Loads an array from the given ref.

  If ``mask`` is not specified, this function has the same semantics as
  ``ref[idx]`` in JAX.

  Args:
    ref: The ref to load from.
    mask: An optional boolean mask specifying which indices to load.

  Returns:
    The loaded array.
  """
  return primitives.load(ref, None, mask=mask)


def load(
    src: _Ref,
    idx,
    *,
    layout: SomeLayout | None = None,
    optimized: bool = True,
) -> jax.Array:
  """Loads from a reference into an array with the specified layout.

  Args:
    src: The reference to load from. Can be either in SMEM or GMEM.
    idx: The index to load from.
    layout: The optional layout to use for the resulting array.
    optimized: If True, a compilation error will be raised if no optimized
      implementation for the load is available.

  Returns:
    The loaded array.
  """
  src, src_transforms = state_primitives.get_ref_and_transforms(
      src, idx, "load"
  )
  flat_src_transforms, src_transforms_treedef = tree_util.tree_flatten(
      src_transforms
  )
  result = load_p.bind(
      src,
      *flat_src_transforms,
      tree=src_transforms_treedef,
      optimized=optimized,
  )
  if layout is not None:
    result = gpu_core.layout_cast(result, layout)
  return result


def load(
    ref: Ref,
    *,
    mask: jax.Array | None = None,
    other: jax.typing.ArrayLike | None = None,
    cache_modifier: str | None = None,
    eviction_policy: str | None = None,
    volatile: bool = False,
) -> jax.Array:
  """Loads an array from the given ref.

  If neither ``mask`` nor ``other`` is specified, this function has the same
  semantics as ``ref[idx]`` in JAX.

  Args:
    ref: The ref to load from.
    mask: An optional boolean mask specifying which indices to load. If mask is
      ``False`` and ``other`` is not given, no assumptions can be made about the
      value in the resulting array.
    other: An optional value to use for indices where mask is ``False``.
    cache_modifier: TO BE DOCUMENTED.
    eviction_policy: TO BE DOCUMENTED.
    volatile: TO BE DOCUMENTED.
  """
  return pallas_primitives.load(
      ref,
      None,
      mask=mask,
      other=other,
      cache_modifier=cache_modifier,
      eviction_policy=eviction_policy,
      volatile=volatile,
  )


def load(directory: str | PathLike[str], shardings: PyTreeT, *,
         mask: PyTreeT | None = None, ts_specs: PyTreeT | None = None
         ) -> PyTreeT:
  """Loads and reconstructs a data structure from a directory.

  This is a simple experimental array serialization API, for anything more
  complex and for all checkpointing prefer: https://github.com/google/orbax

  Args:
    directory: Directory path where the data is stored.
    shardings: Sharding strategy for array objects, either a Sharding or a
      ShapeDtypeStruct with a Sharding/Format.
    mask: boolean prefix tree for partial loading, will return None for False
      leaves.
    ts_specs: Optional tensorstore specs to use for deserialization. If None,
      defaults to using the default tensorstore specs.

  Returns:
    Reconstructed data.

  Example:
    >>> save(data, directory)
    >>> restored_data = load(directory, SingleDeviceSharding(jax.devices()[0]))
  """
  assert not _is_remote_path(directory) or pathlib.epath_installed, (
    "For checkpointing using remote URLs (e.g., gs, s3) you need `etils`"
    " module installed. You can install it using `pip install etils`.")

  root = _norm_path(directory)
  assert root.is_dir(), f"Checkpoint directory {root} does not exist"
  is_leaf = lambda x: x is None

  # deserialize PyTreeDef
  pytree = load_pytreedef(directory)
  # broadcast the (prefix) shardings and tensorstore specs to the full pytree
  shardings = _tree_broadcast(shardings, pytree)
  ts_specs = _tree_broadcast(ts_specs, pytree,
                             is_leaf=ts_impl.is_tensorstore_spec_leaf)
  if mask is not None:
    _prefix_mask = lambda m, x: jax.tree.map(lambda _: None, x) if not m else x
    pytree = jax.tree.map(_prefix_mask, mask, pytree)
  pytreedef = jax.tree.structure(pytree, is_leaf=is_leaf)
  leaf_ids_flat = jax.tree.leaves(pytree, is_leaf=is_leaf)
  shardings_flat = jax.tree.leaves(shardings, is_leaf=is_leaf)
  if any(isinstance(shardings, Format) for shardings in shardings_flat):
    raise NotImplementedError(
        "Deserialization with `Format` instead of `Sharding` is not currently"
        " supported. Pass ShapeDtypeStruct(shape, dtype, sharding=format)"
        " instead.")
  ts_specs_flat = jax.tree.leaves(ts_specs,
                                  is_leaf=ts_impl.is_tensorstore_spec_leaf)

  # deserialize array objects
  arr_leaf_ids = [i for i, leaf_id in enumerate(leaf_ids_flat)
                  if leaf_id is not None]
  shardings_flat = [shardings_flat[i] for i in arr_leaf_ids]
  ts_specs_flat = [ts_specs_flat[i] for i in arr_leaf_ids]

  arrs_fut = _serialization_executor.submit(
      _read_arrays, root / _ARRAY_STORE_DIRNAME, arr_leaf_ids, ts_specs_flat,
      shardings_flat)

  arrs = arrs_fut.result()
  filled_values = [arrs.get(i, None) for i, _ in enumerate(leaf_ids_flat)]
  return jax.tree.unflatten(pytreedef, filled_values)


def load(fp: IO, *, parse_float: ParseFloat = float) -> Dict[str, Any]:
    """Parse TOML from a file object."""
    s = fp.read()
    if isinstance(s, bytes):
        s = s.decode()
    else:
        warnings.warn(
            "Text file object support is deprecated in favor of binary file objects."
            ' Use `open("foo.toml", "rb")` to open the file in binary mode.',
            DeprecationWarning,
        )
    return loads(s, parse_float=parse_float)


def load(name: str) -> callable:
    """Loads an environment with name and returns an environment creation function

    Args:
        name: The environment name

    Returns:
        Calls the environment constructor
    """
    mod_name, attr_name = name.split(":")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr_name)
    return fn


def load(
    fp: IO[bytes],
    use_builtin_types: Optional[bool] = None,
    dict_type: Type[MutableMapping[str, Any]] = dict,
) -> Any:
    """Load a plist file into an object.

    Args:
        fp: An opened file.
        use_builtin_types: If True, binary data is deserialized to
            bytes strings. If False, it is wrapped in :py:class:`Data`
            objects. Defaults to True if not provided. Deprecated.
        dict_type: What type to use for dictionaries.

    Returns:
        An object (usually a dictionary) representing the top level of
        the plist file.
    """

    if not hasattr(fp, "read"):
        raise AttributeError("'%s' object has no attribute 'read'" % type(fp).__name__)
    target = PlistTarget(use_builtin_types=use_builtin_types, dict_type=dict_type)
    parser = etree.XMLParser(target=target)
    result = etree.parse(fp, parser=parser)
    # lxml returns the target object directly, while ElementTree wraps
    # it as the root of an ElementTree object
    try:
        return result.getroot()
    except AttributeError:
        return result


def load(fp: t.IO[t.AnyStr], **kwargs: t.Any) -> t.Any:
    """Deserialize data as JSON read from a file.

    If :data:`~flask.current_app` is available, it will use its
    :meth:`app.json.load() <flask.json.provider.JSONProvider.load>`
    method, otherwise it will use :func:`json.load`.

    :param fp: A file opened for reading text or UTF-8 bytes.
    :param kwargs: Arguments passed to the ``load`` implementation.

    .. versionchanged:: 2.3
        The ``app`` parameter was removed.

    .. versionchanged:: 2.2
        Calls ``current_app.json.load``, allowing an app to override
        the behavior.

    .. versionchanged:: 2.2
        The ``app`` parameter will be removed in Flask 2.3.

    .. versionchanged:: 2.0
        ``encoding`` will be removed in Flask 2.1. The file must be text
        mode, or binary mode with UTF-8 bytes.
    """
    if current_app:
        return current_app.json.load(fp, **kwargs)

    return _json.load(fp, **kwargs)

