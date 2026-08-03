import os
import subprocess

def run_benchmark(name: str, function: object, dtype: torch.dtype, seed: int, device: str, samples: int,
                  probability_regular: float):
    cuda = device == 'cuda'
    spectral_fuzzer = SpectralOpFuzzer(seed=seed, dtype=dtype, cuda=cuda,
                                       probability_regular=probability_regular)
    results = []
    for tensors, tensor_params, params in spectral_fuzzer.take(samples):
        shape = [params['k0'], params['k1'], params['k2']][:params['ndim']]
        str_shape = ' x '.join([f"{s:<4}" for s in shape])
        sub_label = f"{str_shape} {'' if tensor_params['x']['is_contiguous'] else '(discontiguous)'}"
        for dim in _dim_options(params['ndim']):
            for nthreads in (1, 4, 16) if not cuda else (1,):
                measurement = benchmark.Timer(
                    stmt='func(x, dim=dim)',
                    globals={'func': function, 'x': tensors['x'], 'dim': dim},
                    label=f"{name}_{device}",
                    sub_label=sub_label,
                    description=f"dim={dim}",
                    num_threads=nthreads,
                ).blocked_autorange(min_run_time=1)
                measurement.metadata = {
                    'name': name,
                    'device': device,
                    'dim': dim,
                    'shape': shape,
                }
                measurement.metadata.update(tensor_params['x'])
                results.append(measurement)
    return results


def run_benchmark(test_config):
  """Runs a single benchmark test based on the given config.

  Args:
    test_config: A dictionary containing the test configuration.

  Returns:
    True if benchmark ran successfully, False otherwise.
  """
  print(f"Running benchmark: {test_config['name']}")

  # Build command
  output_dir = os.path.join(
      test_config['output_directory'],
      datetime.datetime.now().strftime('%Y%m%d'),
  )

  cmd = [
      'python3',
      'orbax/checkpoint/_src/testing/benchmarks/xpk/launch_xpk.py',
      '--cluster_name',
      test_config['cluster_name'],
      '--tpu_type',
      test_config['tpu_type'],
      '--zone',
      test_config['zone'],
      '--config_file',
      test_config['config_file'],
      '--docker_image',
      test_config['docker_image'],
      '--output_directory',
      output_dir,
      '--num_slices',
      str(test_config['num_slices']),
  ]
  if test_config.get('nodelete_cluster_on_completion'):
    cmd.append('--nodelete_cluster_on_completion')
  if test_config.get('ramdisk_directory'):
    cmd.extend(['--ramdisk_directory', test_config['ramdisk_directory']])
  if test_config.get('test_restart_workflow'):
    cmd.append('--test_restart_workflow')
  if test_config.get('verbose'):
    cmd.append('--verbose')
  if test_config.get('skip_validation'):
    cmd.append('--skip_validation')
  if test_config.get('enable_pathways'):
    cmd.append('--enable_pathways')
  if test_config.get('gcp_region'):
    cmd.extend(['--region', test_config['gcp_region']])

  print(f"Executing command: {' '.join(cmd)}")
  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    print(f'Benchmark script failed: {e}')
    return False

  return True


def run_benchmark(module, function, setup_suffix="", repeat=5, number=1000):
    setup_func = "setup_" + function
    if setup_suffix:
        print("%s with %s:" % (function, setup_suffix), end="")
        setup_func += "_" + setup_suffix
    else:
        print("%s:" % function, end="")

    def wrapper(function, setup_func):
        function = globals()[function]
        setup_func = globals()[setup_func]

        def wrapped():
            return function(*setup_func())

        return wrapped

    results = timeit.repeat(wrapper(function, setup_func), repeat=repeat, number=number)
    print("\t%5.1fus" % (min(results) * 1000000.0 / number))


def run_benchmark(module, function, setup_suffix="", repeat=25, number=1):
    setup_func = "setup_" + function
    if setup_suffix:
        print("%s with %s:" % (function, setup_suffix), end="")
        setup_func += "_" + setup_suffix
    else:
        print("%s:" % function, end="")

    def wrapper(function, setup_func):
        function = globals()[function]
        setup_func = globals()[setup_func]

        def wrapped():
            return function(*setup_func())

        return wrapped

    results = timeit.repeat(wrapper(function, setup_func), repeat=repeat, number=number)
    print("\t%5.1fus" % (min(results) * 1000000.0 / number))

