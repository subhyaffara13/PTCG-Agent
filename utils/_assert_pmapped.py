
def _assert_pmapped(fn, fn_input, is_pmapped, should_jit=False):
  """Asserts whether a function can be pmapped or not.

  Args:
    fn: The function to be tested
    fn_input: Input to pass to the function
    is_pmapped: Assert that the function can be pmapped with jax.pmap (True) or
    cannot be pmapped (False), i.e. the fake pmap is working correctly.
    should_jit: if True, asserts that the function is jitted, regardless of it
    being pmapped or not.
  """
  num_devices = len(jax.devices())
  if should_jit:
    asserts.clear_trace_counter()
    fn = asserts.assert_max_traces(fn, n=1)
  wrapped_fn = jax.pmap(fn, axis_size=num_devices)

  fn_input = jnp.broadcast_to(fn_input, (num_devices,) + fn_input.shape)
  output = wrapped_fn(fn_input)

  # We test whether the function has been pmapped by inspecting the type of
  # the function output, if it is a sharded array type then the function has
  # been pmapped
  if is_pmapped:
    expected_type = jax.Array
    assert_message = f'Output is type {type(output)}, expected {expected_type}'
    assert isinstance(output, expected_type), assert_message
  else:
    expected_type = 'DeviceArray'
    assert_message = f'Output is type {type(output)}, expected {expected_type}'
    # ShardedDeviceArray is a subclass of DeviceArray. So, to enforce we have
    # a DeviceArray, we also check it's not a sharded one.
    assert (isinstance(output, jax.Array) and
            len(output.sharding.device_set) == 1), assert_message

