import os
import sys
from typing import Any, Dict, Optional

def save(tensors: Dict[str, Array], metadata: Optional[Dict[str, str]] = None) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, Array]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.flax import save
    from jax import numpy as jnp

    tensors = {"embedding": jnp.zeros((512, 1024)), "attention": jnp.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    np_tensors = _jnp2np(tensors)
    return numpy.save(np_tensors, metadata=metadata)


def save(
    tensors: Dict[str, mx.array], metadata: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, mx.array]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.mlx import save
    import mlx.core as mx

    tensors = {"embedding": mx.zeros((512, 1024)), "attention": mx.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    np_tensors = _mx2np(tensors)
    return numpy.save(np_tensors, metadata=metadata)


def save(
    tensor_dict: Dict[str, np.ndarray], metadata: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensor_dict (`Dict[str, np.ndarray]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.numpy import save
    import numpy as np

    tensors = {"embedding": np.zeros((512, 1024)), "attention": np.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    keep_alive_buffer = []  # to keep byteswapped tensors alive
    serialized = serialize(_flatten(tensor_dict, keep_alive_buffer), metadata=metadata)
    result = bytes(serialized)
    return result


def save(
    tensors: Dict[str, paddle.Tensor], metadata: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, paddle.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.paddle import save
    import paddle

    tensors = {"embedding": paddle.zeros((512, 1024)), "attention": paddle.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    keep_references_alive = []
    serialized = serialize(_flatten(tensors, keep_references_alive), metadata=metadata)
    result = bytes(serialized)
    return result


def save(
    tensors: Dict[str, tf.Tensor], metadata: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, tf.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.tensorflow import save
    import tensorflow as tf

    tensors = {"embedding": tf.zeros((512, 1024)), "attention": tf.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    np_tensors = _tf2np(tensors)
    return numpy.save(np_tensors, metadata=metadata)


def save(
    tensors: Dict[str, torch.Tensor], metadata: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Saves a dictionary of tensors into raw bytes in safetensors format.

    Args:
        tensors (`Dict[str, torch.Tensor]`):
            The incoming tensors. Tensors need to be contiguous and dense.
        metadata (`Dict[str, str]`, *optional*, defaults to `None`):
            Optional text only metadata you might want to save in your header.
            For instance it can be useful to specify more about the underlying
            tensors. This is purely informative and does not affect tensor loading.

    Returns:
        `bytes`: The raw bytes representing the format

    Example:

    ```python
    from safetensors.torch import save
    import torch

    tensors = {"embedding": torch.zeros((512, 1024)), "attention": torch.zeros((256, 256))}
    byte_data = save(tensors)
    ```
    """
    keep_references_alive = []  # to avoid garbage collection of temporary numpy arrays while we write to disk
    serialized = serialize(
        _flatten_as_ptr(tensors, keep_references_alive), metadata=metadata
    )
    result = bytes(serialized)
    return result


def save(
    obj: object,
    f: FileLike,
    pickle_module: Any = pickle,
    pickle_protocol: int = DEFAULT_PROTOCOL,
    _use_new_zipfile_serialization: bool = True,
    _disable_byteorder_record: bool = False,
) -> None:
    # Reference: https://github.com/pytorch/pytorch/issues/54354
    # The first line of this docstring overrides the one Sphinx generates for the
    # documentation. We need it so that Sphinx doesn't leak `pickle`s path from
    # the build environment (e.g. `<module 'pickle' from '/leaked/path').

    """save(obj, f, pickle_module=pickle, pickle_protocol=2, _use_new_zipfile_serialization=True)

    Saves an object to a disk file.

    See also: :ref:`saving-loading-tensors`

    See :ref:`layout-control` for more advanced tools to manipulate a checkpoint.

    Args:
        obj: saved object
        f: a file-like object (has to implement write and flush) or a string or
           os.PathLike object containing a file name
        pickle_module: module used for pickling metadata and objects
        pickle_protocol: can be specified to override the default protocol

    .. note::
        A common PyTorch convention is to save tensors using .pt file extension.

    .. note::
        PyTorch preserves storage sharing across serialization. See
        :ref:`preserve-storage-sharing` for more details.

    .. note::
        The 1.6 release of PyTorch switched ``torch.save`` to use a new
        zipfile-based file format. ``torch.load`` still retains the ability to
        load files in the old format. If for any reason you want ``torch.save``
        to use the old format, pass the kwarg ``_use_new_zipfile_serialization=False``.

    Example:
        >>> # xdoctest: +SKIP("makes cwd dirty")
        >>> # Save to file
        >>> x = torch.tensor([0, 1, 2, 3, 4])
        >>> torch.save(x, "tensor.pt")
        >>> # Save to io.BytesIO buffer
        >>> buffer = io.BytesIO()
        >>> torch.save(x, buffer)
    """
    torch._C._log_api_usage_once("torch.save")
    _check_dill_version(pickle_module)
    _check_save_filelike(f)

    if isinstance(f, (str, os.PathLike)):
        f = os.fspath(f)

    if _use_new_zipfile_serialization:
        with _open_zipfile_writer(f) as opened_zipfile:
            _save(
                obj,
                opened_zipfile,
                pickle_module,
                pickle_protocol,
                _disable_byteorder_record,
            )
            return
    else:
        global _serialization_tls
        if _serialization_tls.skip_data:
            raise RuntimeError(
                "Cannot use skip_data=True with _use_new_zipfile_serialization=False"
            )
        with _open_file_like(f, "wb") as opened_file:
            _legacy_save(obj, opened_file, pickle_module, pickle_protocol)


def save(
    ep: ExportedProgram,
    f: FileLike,
    *,
    extra_files: dict[str, Any] | None = None,
    opset_version: dict[str, int] | None = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> None:
    """

    .. warning::
        Under active development, saved files may not be usable in newer versions
        of PyTorch.

    Saves an :class:`ExportedProgram` to a file-like object. It can then be
    loaded using the Python API :func:`torch.export.load <torch.export.load>`.

    Args:
        ep (ExportedProgram): The exported program to save.

        f (str | os.PathLike[str] | IO[bytes]) A file-like object (has to
         implement write and flush) or a string containing a file name.

        extra_files (Optional[Dict[str, Any]]): Map from filename to contents
         which will be stored as part of f.

        opset_version (Optional[Dict[str, int]]): A map of opset names
         to the version of this opset

        pickle_protocol: can be specified to override the default protocol

    Example::

        import torch
        import io


        class MyModule(torch.nn.Module):
            def forward(self, x):
                return x + 10


        ep = torch.export.export(MyModule(), (torch.randn(5),))

        # Save to file
        torch.export.save(ep, "exported_program.pt2")

        # Save to io.BytesIO buffer
        buffer = io.BytesIO()
        torch.export.save(ep, buffer)

        # Save with extra files
        extra_files = {"foo.txt": b"bar".decode("utf-8")}
        torch.export.save(ep, "exported_program.pt2", extra_files=extra_files)

    """
    if not isinstance(ep, ExportedProgram):
        raise TypeError(
            f"The 'ep' parameter must be an instance of 'ExportedProgram', got '{type(ep).__name__}' instead."
        )

    from torch.export.pt2_archive._package import package_pt2

    package_pt2(
        f,
        exported_programs={"model": ep},
        extra_files=extra_files,
        pickle_protocol=pickle_protocol,
        opset_version=opset_version,
    )


def save(m, f, _extra_files=None) -> None:
    r"""
    Save an offline version of this module for use in a separate process.

    The saved module serializes all of the methods, submodules, parameters, and
    attributes of this module. It can be loaded into the C++ API using
    ``torch::jit::load(filename)`` or into the Python API with
    :func:`torch.jit.load <torch.jit.load>`.

    To be able to save a module, it must not make any calls to native Python
    functions.  This means that all submodules must be subclasses of
    :class:`ScriptModule` as well.

    .. DANGER::
        All modules, no matter their device, are always loaded onto the CPU
        during loading.  This is different from :func:`torch.load`'s semantics
        and may change in the future.

    Args:
        m: A :class:`ScriptModule` to save.
        f: A file-like object (has to implement write and flush) or a string
           containing a file name.
        _extra_files: Map from filename to contents which will be stored as part of `f`.

    .. note::
        torch.jit.save attempts to preserve the behavior of some operators
        across versions. For example, dividing two integer tensors in
        PyTorch 1.5 performed floor division, and if the module
        containing that code is saved in PyTorch 1.5 and loaded in PyTorch 1.6
        its division behavior will be preserved. The same module saved in
        PyTorch 1.6 will fail to load in PyTorch 1.5, however, since the
        behavior of division changed in 1.6, and 1.5 does not know how to
        replicate the 1.6 behavior.

    Example:
    .. testcode::

        import torch
        import io

        class MyModule(torch.nn.Module):
            def forward(self, x):
                return x + 10

        m = torch.jit.script(MyModule())

        # Save to file
        torch.jit.save(m, 'scriptmodule.pt')
        # This line is equivalent to the previous
        m.save("scriptmodule.pt")

        # Save to io.BytesIO buffer
        buffer = io.BytesIO()
        torch.jit.save(m, buffer)

        # Save with extra files
        extra_files = {'foo.txt': b'bar'}
        torch.jit.save(m, 'scriptmodule.pt', _extra_files=extra_files)
    """
    if sys.version_info >= (3, 14):
        warnings.warn(
            "`torch.jit.save` is not supported in Python 3.14+ and may break. "
            "Please switch to `torch.export`.",
            DeprecationWarning,
        )
    else:
        warnings.warn(
            "`torch.jit.save` is deprecated. Please switch to `torch.export`.",
            DeprecationWarning,
        )
    log_torchscript_usage("save", model_id=_get_model_id(m))
    if _extra_files is None:
        _extra_files = {}
    if isinstance(f, (str, os.PathLike)):
        m.save(f, _extra_files=_extra_files)
    else:
        ret = m.save_to_buffer(_extra_files=_extra_files)
        f.write(ret)


def save(tensors, *args, **kwargs):
    torch.save(to_cpu(tensors), *args, **kwargs)


def save(
    state_dict: STATE_DICT_TYPE,
    *,
    checkpoint_id: str | os.PathLike | None = None,
    storage_writer: StorageWriter | None = None,
    planner: SavePlanner | None = None,
    process_group: dist.ProcessGroup | None = None,
    no_dist: bool = False,
    use_collectives: bool = True,
) -> Metadata:
    """
    Save a distributed model in SPMD style.

    This function is different from ``torch.save()`` as it handles
    ``ShardedTensor`` , and ``DTensor`` by having each rank only save their local shards.

    For each ``Stateful`` object (having both a ``state_dict`` and a ``load_state_dict``),
    save will call ``state_dict`` before serialization.

    .. warning::
        There is no guarantees of Backwards Compatibility across PyTorch versions
        for saved state_dicts.

    .. warning::
        If using the `process_group` argument, make sure that only its ranks
        call `save_state_dict` and that all data in state_dict belong to it.

    .. note::
        When saving checkpoint for FSDP's `ShardingStrategy.HYBRID_SHARD`, only one of
        the shard_group should be calling `save_state_dict` and the corresponding process
        group needs to be passed in.

    .. note::
        If no process group is available, this function assumes the intention is to save the
         state_dict in the local process.

    .. note:
        Rank 0 is assumed to be the coordinator rank.


    Args:
        state_dict (Dict[str, Any]): The state_dict to save.
        checkpoint_id (Union[str, os.PathLike, None]):
            The ID of this checkpoint instance. The meaning of the checkpoint_id
            depends on the storage. It can be a path to a folder or to a file.
            It can also be a key if the storage is a key-value store.
            (Default: ``None``)
        storage_writer (Optional[StorageWriter]):
            Instance of StorageWriter used to perform writes. If this is not
            specified, DCP will automatically infer the writer based on the
            checkpoint_id. If checkpoint_id is also None, an exception will
            be raised. (Default: ``None``)
        planner (Optional[SavePlanner]):
            Instance of SavePlanner. If this is not specified, the default
            planner will be used. (Default: ``None``)
        process_group (Optional[ProcessGroup]):
            ProcessGroup to be used for cross-rank synchronization.
            (Default: ``None``)
        no_dist (bool):
            If ``True``, this function will assume the intent is to load
            a checkpoint on a single rank/process.
            (Default: ``False``)
        use_collectives (bool): If ``False``, this function will assume the intent is to save
            a checkpoint without using cross-rank synchronization.
            (Default: ``True``)
            This configuration is experimental and should be used with caution.
            It will change the format of the saved checkpoint and may not be backward compatible.

    Returns:
        Metadata: Metadata object for the saved checkpoint.

    Example:
        >>> # xdoctest: +SKIP
        >>> my_model = MyModule()

        >>> state_dict = {"model": my_model}

        >>> fs_storage_writer = torch.distributed.checkpoint.FileSystemWriter(
        ...     "/checkpoint/1"
        ... )
        >>> torch.distributed.checkpoint.save(
        >>>     state_dict=state_dict,
        >>>     storage_writer=fs_storage_writer,
        >>> )

    .. note::
        save_state_dict uses collectives to coordinate writes across ranks.
        For NCCL-based process groups, internal tensor representations of
        objects must be moved to the GPU device before communication takes place.
        In this case, the device used is given by ``torch.cuda.current_device()``
        and it is the user's responsibility to ensure that this is set so that
        each rank has an individual GPU, via ``torch.cuda.set_device()``.
    """
    torch._C._log_api_usage_once("torch.distributed.checkpoint.save")

    no_dist = no_dist or (not dist.is_available()) or (not dist.is_initialized())
    if no_dist:
        warnings.warn(
            "torch.distributed is disabled, unavailable or uninitialized, assuming the intent is to save in a single process.",
            stacklevel=2,
        )

    with _profile():
        storage_writer = cast(
            StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)
        )

        return _save_state_dict(
            state_dict=_stateful_to_state_dict(state_dict),
            storage_writer=storage_writer,
            process_group=process_group,
            no_dist=no_dist,
            planner=planner,
            use_collectives=use_collectives,
        )


def save(
    path: path_types.PathLike,
    state: tree_types.PyTreeOf[tree_types.Leaf],
    *,
    custom_metadata: tree_types.JsonType | None = None,
):
  """Partially saves a PyTree.

  This function allows for incrementally updating a checkpoint. It is designed
  to be called multiple times. The first call initiates a new partial save
  "session" in a temporary location. Subsequent calls will update this session
  by modifying the checkpoint in place.

  The operation is atomic; if it is interrupted, the previous version of the
  partial save will be preserved.

  IMPORTANT: The checkpoint is not finalized at the target `path` until
  :py:func:`.finalize` is called. The intermediate checkpoints are
  temporary and should not be used directly.

  ### Workflow

  A typical partial save workflow involves one or more calls to
  :py:func:`.save` followed by a single call to :py:func:`~.finalize`::

    path = '/path/to/my/checkpoint'

    # The first call creates a temporary directory:
    # '/path/to/my/checkpoint.partial_save'
    # Note: the exact temporary directory name is an implementation detail that
    # depends on the file system and should not be relied on.
    ocp.partial.save(path, {'layer1': ..., 'step': 1})

    # A subsequent call reads the previous version and applies new updates
    # to the temporary directory:
    # '/path/to/my/checkpoint.partial_save'
    ocp.partial.save(path, {'layer2': ..., 'metrics': ...})

    # This call commits the latest version to the final destination at
    # '/path/to/my/checkpoint'.
    ocp.partial.finalize(path)

  ### Additions vs. Replacements

  The provided `state` represents a set of updates.
  - If a key in `state` (e.g., 'metrics') does not exist in the on-disk
    checkpoint, it is treated as an **addition**. In other words, the sets of
    keys of the on-disk PyTree and the provided `state` are disjoint.
  - If a key (e.g., 'step') already exists, its value is **replaced**. In other
    words, the sets of keys of the on-disk PyTree and the provided `state`
    overlap. Replacements are currently NOT supported. Please reach out to the
    Orbax team if you need this functionality.

  See :py:func:`~.v1.save` for general
  PyTree saving documentation.

  Args:
    path: The path to save the checkpoint to.
    state: A PyTree representing the additions to be applied to the on-disk
      checkpoint.
    custom_metadata: User-provided custom metadata. This will be merged with any
      existing custom metadata. Values from this dictionary will overwrite
      existing values if keys conflict.
  """
  save_async(
      path,
      state,
      custom_metadata=custom_metadata,
  ).result()


def save(
    path: path_types.PathLike,
    state: tree_types.PyTreeOf[tree_types.Leaf],
    *,
    checkpointable_name: str = STATE_CHECKPOINTABLE_KEY,
    overwrite: bool = False,
    custom_metadata: tree_types.JsonType | None = None,
):
  """Saves a `PyTree`.

  The operation blocks until complete. For improved performance, consider using
  :py:func:`.save_async` instead. This function should be called on
  all available controller processes.

  Example usage:
    Simple save of a dictionary containing JAX arrays::
      state = {
          'params': {
              'w': jnp.ones((8, 8)),
              'b': jnp.zeros(8),
          },
          'step': 100
      }
      # Saves to /tmp/my_checkpoint/
      ocp.save('/tmp/my_checkpoint', state)

  Args:
    path: The path to save the checkpoint to.
    state: The `PyTree` to save. This may be any JAX `PyTree` (including custom
      objects registered as `PyTrees`) consisting of supported leaf types. See
      `orbax.checkpoint.experimental.v1.tree` for a table of standard supported
      leaf types.
    checkpointable_name: The name of the checkpointable to save a pytree under.
      Defaults to 'pytree'.
    overwrite: If True, fully overwrites an existing checkpoint in `path`.
      Otherwise, raises an error if the checkpoint already exists.
    custom_metadata: User-provided custom metadata. An arbitrary
      JSON-serializable dictionary the user can use to store additional
      information. The field is treated as opaque by Orbax.
  """
  validation.validate_state(state)
  execution.save_checkpointables_impl(
      path,
      {checkpointable_name: state},
      overwrite=overwrite,
      custom_metadata=custom_metadata,
      async_origin=False,
  ).result()


def save(file, arr, allow_pickle=True):
    """
    Save an array to a binary file in NumPy ``.npy`` format.

    Parameters
    ----------
    file : file, str, or pathlib.Path
        File or filename to which the data is saved. If file is a file-object,
        then the filename is unchanged.  If file is a string or Path,
        a ``.npy`` extension will be appended to the filename if it does not
        already have one.
    arr : array_like
        Array data to be saved.
    allow_pickle : bool, optional
        Allow saving object arrays using Python pickles. Reasons for
        disallowing pickles include security (loading pickled data can execute
        arbitrary code) and portability (pickled objects may not be loadable
        on different Python installations, for example if the stored objects
        require libraries that are not available, and not all pickled data is
        compatible between different versions of Python).
        Default: True

    See Also
    --------
    savez : Save several arrays into a ``.npz`` archive
    savetxt, load

    Notes
    -----
    For a description of the ``.npy`` format, see :py:mod:`numpy.lib.format`.

    Any data saved to the file is appended to the end of the file.

    Examples
    --------
    >>> import numpy as np

    >>> from tempfile import TemporaryFile
    >>> outfile = TemporaryFile()

    >>> x = np.arange(10)
    >>> np.save(outfile, x)

    >>> _ = outfile.seek(0) # Only needed to simulate closing & reopening file
    >>> np.load(outfile)
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


    >>> with open('test.npy', 'wb') as f:
    ...     np.save(f, np.array([1, 2]))
    ...     np.save(f, np.array([1, 3]))
    >>> with open('test.npy', 'rb') as f:
    ...     a = np.load(f)
    ...     b = np.load(f)
    >>> print(a, b)
    # [1 2] [1 3]
    """
    if hasattr(file, 'write'):
        file_ctx = contextlib.nullcontext(file)
    else:
        file = os.fspath(file)
        if not file.endswith('.npy'):
            file = file + '.npy'
        file_ctx = open(file, "wb")

    with file_ctx as fid:
        arr = np.asanyarray(arr)
        format.write_array(fid, arr, allow_pickle=allow_pickle)


def save(data: PyTreeT, directory: str | PathLike[str], *,
         overwrite: bool = True, ts_specs: PyTreeT | None = None) -> None:
  """Saves the given data structure to the provided directory path.

  This function provides functionality to serialize and save a data structure
  comprising JAX arrays, along with its structure to a given directory. It
  leverages `PyTree` for flattening and reconstructing the data structure.

  This is a simple experimental array serialization API, for anything more
  complex and for all checkpointing prefer: https://github.com/google/orbax

  Args:
    data: The data structure to be saved. Arbitrary composition of JAX arrays,
      including nested structures.
    directory: The directory path where the data will be saved. A local path or
      a remote URL (e.g., gs://, s3://). For remote URLs, `etils` is required.
    overwrite: If True, any existing directory with the same name will be
      overwritten.
    ts_specs: Optional tensorstore specs to use for serialization. If None,
      defaults to using the default tensorstore specs.

  Example:
    >>> data = {"a": jnp.array([1, 2]), "b": None}
    >>> save(data, directory)
  """
  with _THREADING_SAVE_LOCK:
    return _save(data, directory, overwrite=overwrite, ts_specs=ts_specs)

