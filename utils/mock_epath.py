
def mock_epath(
    *,
    copy: Optional[_MockFn] = None,
    exists: Optional[_MockFn] = None,
    glob: Optional[_MockFn] = None,
    isdir: Optional[_MockFn] = None,
    listdir: Optional[_MockFn] = None,
    makedirs: Optional[_MockFn] = None,
    mkdir: Optional[_MockFn] = None,
    open: Optional[_MockFn] = None,  # pylint: disable=redefined-builtin
    remove: Optional[_MockFn] = None,
    rename: Optional[_MockFn] = None,
    replace: Optional[_MockFn] = None,
    rmtree: Optional[_MockFn] = None,
    stat: Optional[_MockFn] = None,
    walk: Optional[_MockFn] = None,
) -> Iterator[None]:
  """Mock epath.

  Mock the file system by replacing the given function by their mock.
  Only the function passed are mocked.
  The mock function should have signature: `(original_fn, path)` + eventual
    args/kwargs for specific functions.

  Args:
    copy: New function (after mocking)
    exists: New function (after mocking)
    glob: New function (after mocking)
    isdir: New function (after mocking)
    listdir: New function (after mocking)
    makedirs: New function (after mocking)
    mkdir: New function (after mocking)
    open: New function (after mocking)
    remove: New function (after mocking)
    rename: New function (after mocking)
    replace: New function (after mocking)
    rmtree: New function (after mocking)
    stat: New function (after mocking)
    walk: New function (after mocking)

  Yields:
    None
  """
  mock_fns = dict(
      open=open,
      copy=copy,
      rename=rename,
      exists=exists,
      glob=glob,
      walk=walk,
      isdir=isdir,
      listdir=listdir,
      makedirs=makedirs,
      mkdir=mkdir,
      remove=remove,
      replace=replace,
      rmtree=rmtree,
      stat=stat,
  )
  mock_backend = _MockBackend(mock_fns=mock_fns)

  # Replace all backend by the mock backend
  new_prefix_to_backend = {k: mock_backend for k in gpath._PREFIX_TO_BACKEND}  # pylint: disable=protected-access
  with mock.patch.object(gpath, '_PREFIX_TO_BACKEND', new_prefix_to_backend):
    yield

