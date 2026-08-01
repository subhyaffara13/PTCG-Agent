
def deserialize_and_load(serialized,
                         in_tree,
                         out_tree,
                         backend: str | xc.Client | None = None,
                         execution_devices: Sequence[xc.Device] | None = None):
  """Constructs a :class:`jax.stages.Compiled` from a serialized executable.

  .. warning::
     It is not safe to call this API with untrusted inputs. Do not do this.
     Calling this API loads a serialized executable. Even loading such an
     executable may run arbitrary code on your machine. It is not safe to pass
     untrusted data here and likely never will be.
  """

  if backend is None or isinstance(backend, str):
    backend = jax.devices(backend)[0].client

  if execution_devices is None:
    execution_devices = backend.devices()
  else:
    device_backend = execution_devices[0].client
    if device_backend != backend:
      raise ValueError(
          'Execution devices belong to a client other than `backend`. Got '
          f'backend client: {(backend.platform, backend.platform_version)} and '
          'execution devices client: '
          f'{(device_backend.platform, device_backend.platform_version)}')

  (unloaded_executable, args_info_flat,
   no_kwargs) = _JaxPjrtUnpickler(
       io.BytesIO(serialized), backend, execution_devices).load()

  args_info = in_tree.unflatten(args_info_flat)

  loaded_compiled_obj = unloaded_executable.load()
  # TODO(necula): deal with constants in serialized executables
  return jax.stages.Compiled(
      loaded_compiled_obj, [], args_info, out_tree, no_kwargs=no_kwargs)

