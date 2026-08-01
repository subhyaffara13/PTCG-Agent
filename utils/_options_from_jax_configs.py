
def _options_from_jax_configs(plugin_name):
  options = {}

  pjrt_client_options = config.jax_pjrt_client_create_options.value
  if isinstance(pjrt_client_options, str):
    pjrt_client_option_list = []
    if pjrt_client_options:
      pjrt_client_option_list = pjrt_client_options.split(";")

    for option in pjrt_client_option_list:
      option_list = option.split(":")
      if (len(option_list) != 2):
        raise RuntimeError(
            "Multiple ':' separators for option in "
            f"jax_pjrt_client_create_options: '{option}'. "
            "Should be in format 'key:value'")
      options[option_list[0]] = option_list[1]
  elif isinstance(pjrt_client_options, dict):
    options.update(pjrt_client_options)

  _visible_device_configs = {
      "cuda": CUDA_VISIBLE_DEVICES,
      "rocm": _ROCM_VISIBLE_DEVICES,
      "oneapi": _ONEAPI_VISIBLE_DEVICES,
  }
  if plugin_name in _visible_device_configs:
    visible_devices = _visible_device_configs[plugin_name].value
    if visible_devices != 'all':
      options['visible_devices'] = [int(x) for x in visible_devices.split(',')]
    mock_gpu_topology = MOCK_GPU_TOPOLOGY.value or None
    mock_num_processes = (get_num_nodes_from_gpu_topology(mock_gpu_topology) if
        mock_gpu_topology else MOCK_NUM_GPU_PROCESSES.value)
    options['enable_mock_nccl'] = mock_num_processes > 0
    if mock_num_processes > 0:
      options['num_nodes'] = mock_num_processes
      if mock_gpu_topology:
        options['mock_gpu_topology'] = mock_gpu_topology

  return options

