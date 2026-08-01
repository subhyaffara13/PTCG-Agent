
def _setup_sharding(
    custom_loader: unittest.TestLoader | None = None,
) -> tuple[unittest.TestLoader, int | None]:
  """Implements the bazel sharding protocol.

  The following environment variables are used in this method:

    TEST_SHARD_STATUS_FILE: string, if set, points to a file. We write a blank
      file to tell the test runner that this test implements the test sharding
      protocol.

    TEST_TOTAL_SHARDS: int, if set, sharding is requested.

    TEST_SHARD_INDEX: int, must be set if TEST_TOTAL_SHARDS is set. Specifies
      the shard index for this instance of the test process. Must satisfy:
      0 <= TEST_SHARD_INDEX < TEST_TOTAL_SHARDS.

  Args:
    custom_loader: A TestLoader to be made sharded.

  Returns:
    A tuple of ``(test_loader, shard_index)``. ``test_loader`` is for
    shard-filtering or the standard test loader depending on the sharding
    environment variables. ``shard_index`` is the shard index, or ``None`` when
    sharding is not used.
  """

  # It may be useful to write the shard file even if the other sharding
  # environment variables are not set. Test runners may use this functionality
  # to query whether a test binary implements the test sharding protocol.
  if 'TEST_SHARD_STATUS_FILE' in os.environ:
    try:
      with open(os.environ['TEST_SHARD_STATUS_FILE'], 'w') as f:
        f.write('')
    except OSError:
      sys.stderr.write('Error opening TEST_SHARD_STATUS_FILE (%s). Exiting.'
                       % os.environ['TEST_SHARD_STATUS_FILE'])
      sys.exit(1)

  base_loader = custom_loader or TestLoader()
  if 'TEST_TOTAL_SHARDS' not in os.environ:
    # Not using sharding, use the expected test loader.
    return base_loader, None

  total_shards = int(os.environ['TEST_TOTAL_SHARDS'])
  shard_index = int(os.environ['TEST_SHARD_INDEX'])

  if shard_index < 0 or shard_index >= total_shards:
    sys.stderr.write('ERROR: Bad sharding values. index=%d, total=%d\n' %
                     (shard_index, total_shards))
    sys.exit(1)

  # Replace the original getTestCaseNames with one that returns
  # the test case names for this shard.
  delegate_get_names = base_loader.getTestCaseNames

  bucket_iterator = itertools.cycle(range(total_shards))

  def getSharedTestCaseNames(testCaseClass):
    has_shard_test_case_names = hasattr(base_loader, 'shardTestCaseNames')
    if has_shard_test_case_names:
      sharder = getattr(base_loader, 'shardTestCaseNames')
    else:
      sharder = lambda *args: TestLoader.shardTestCaseNames(base_loader, *args)

    names = sharder(
        bucket_iterator, delegate_get_names(testCaseClass), shard_index
    )
    return names

  base_loader.getTestCaseNames = getSharedTestCaseNames  # type: ignore[method-assign]
  return base_loader, shard_index

