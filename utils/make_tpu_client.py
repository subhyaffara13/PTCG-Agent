
def make_tpu_client(
    library_path: str | None = None, options: _NameValueMapping | None = None
):
  """Returns a TPU client. Defaults to allowing 32 in-flight computations."""
  if not _jax.pjrt_plugin_loaded('tpu'):
    c_api = xla_client.load_pjrt_plugin_dynamically(
        "tpu", library_path or "libtpu.so"
    )
    _profiler.register_plugin_profiler(c_api)
    assert _jax.pjrt_plugin_loaded('tpu')
  if not _jax.pjrt_plugin_initialized('tpu'):
    _jax.initialize_pjrt_plugin('tpu')
  if options is None:
    options = {}
  return _jax.get_c_api_client(
      "tpu",
      options,
      distributed.global_state.client,
      _make_transfer_server_factory(),
      FORCE_DCN_CROSS_HOST_TRANSFERS.value,
      SORT_DEVICES_BY_PROCESS_INDEX.value,
  )

