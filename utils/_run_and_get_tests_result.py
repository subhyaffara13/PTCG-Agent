import os
import sys
from typing import Any

def _run_and_get_tests_result(
    argv: abc.MutableSequence[str],
    args: abc.Sequence[Any],
    kwargs: abc.MutableMapping[str, Any],
    xml_test_runner_class: type[unittest.TextTestRunner],
) -> tuple[unittest.TestResult, bool]:
  """Same as run_tests, but it doesn't exit.

  Args:
    argv: sys.argv with the command-line flags removed from the front, i.e. the
      argv with which :func:`app.run()<absl.app.run>` has called
      ``__main__.main``. It is passed to
      ``unittest.TestProgram.__init__(argv=)``, which does its own flag parsing.
      It is ignored if kwargs contains an argv entry.
    args: Positional arguments passed through to
      ``unittest.TestProgram.__init__``.
    kwargs: Keyword arguments passed through to
      ``unittest.TestProgram.__init__``.
    xml_test_runner_class: The type of the test runner class.

  Returns:
    A tuple of ``(test_result, fail_when_no_tests_ran)``.
    ``fail_when_no_tests_ran`` indicates whether the test should fail when
    no tests ran.
  """

  # The entry from kwargs overrides argv.
  argv = kwargs.pop('argv', argv)

  if sys.version_info[:2] >= (3, 12):
    # Python 3.12 unittest changed the behavior from PASS to FAIL in
    # https://github.com/python/cpython/pull/102051. absltest follows this.
    fail_when_no_tests_ran = True
  else:
    # Historically, absltest and unittest before Python 3.12 passes if no tests
    # ran.
    fail_when_no_tests_ran = False

  # Set up test filtering if requested in environment.
  if _setup_filtering(argv):
    # When test filtering is requested, ideally we also want to fail when no
    # tests ran. However, the test filters are usually done when running bazel.
    # When you run multiple targets, e.g. `bazel test //my_dir/...
    # --test_filter=MyTest`, you don't necessarily want individual tests to fail
    # because no tests match in that particular target.
    # Due to this use case, we don't fail when test filtering is requested via
    # the environment variable from bazel.
    fail_when_no_tests_ran = False

  # Set up --failfast as requested in environment
  _setup_test_runner_fail_fast(argv)

  # Shard the (default or custom) loader if sharding is turned on.
  kwargs['testLoader'], shard_index = _setup_sharding(
      kwargs.get('testLoader', None)
  )
  if shard_index is not None and shard_index > 0:
    # When sharding is requested, all the shards except the first one shall not
    # fail when no tests ran. This happens when the shard count is greater than
    # the test case count.
    fail_when_no_tests_ran = False

  # XML file name is based upon (sorted by priority):
  # --xml_output_file flag, XML_OUTPUT_FILE variable,
  # TEST_XMLOUTPUTDIR variable or RUNNING_UNDER_TEST_DAEMON variable.
  if FLAGS.xml_output_file:
    xml_output_file = FLAGS.xml_output_file
  else:
    xml_output_file = get_default_xml_output_filename()
    if xml_output_file:
      FLAGS.xml_output_file = xml_output_file  # type: ignore[assignment]

  xml_buffer = None
  if xml_output_file:
    xml_output_dir = os.path.dirname(xml_output_file)
    if xml_output_dir and not os.path.isdir(xml_output_dir):
      try:
        os.makedirs(xml_output_dir)
      except OSError as e:
        # File exists error can occur with concurrent tests
        if e.errno != errno.EEXIST:
          raise
    # Fail early if we can't write to the XML output file. This is so that we
    # don't waste people's time running tests that will just fail anyways.
    with _open(xml_output_file, 'w'):
      pass

    # We can reuse testRunner if it supports XML output (e. g. by inheriting
    # from xml_reporter.TextAndXMLTestRunner). Otherwise we need to use
    # xml_reporter.TextAndXMLTestRunner.
    if (kwargs.get('testRunner') is not None
        and not hasattr(kwargs['testRunner'], 'set_default_xml_stream')):
      sys.stderr.write('WARNING: XML_OUTPUT_FILE or --xml_output_file setting '
                       'overrides testRunner=%r setting (possibly from --pdb)'
                       % (kwargs['testRunner']))
      # Passing a class object here allows TestProgram to initialize
      # instances based on its kwargs and/or parsed command-line args.
      kwargs['testRunner'] = xml_test_runner_class
    if kwargs.get('testRunner') is None:
      kwargs['testRunner'] = xml_test_runner_class
    # Use an in-memory buffer (not backed by the actual file) to store the XML
    # report, because some tools modify the file (e.g., create a placeholder
    # with partial information, in case the test process crashes).
    xml_buffer = io.StringIO()
    kwargs['testRunner'].set_default_xml_stream(xml_buffer)  # pytype: disable=attribute-error

    # If we've used a seed to randomize test case ordering, we want to record it
    # as a top-level attribute in the `testsuites` section of the XML output.
    randomize_ordering_seed = getattr(
        kwargs['testLoader'], '_randomize_ordering_seed', None)
    setter = getattr(kwargs['testRunner'], 'set_testsuites_property', None)
    if randomize_ordering_seed and setter:
      setter('test_randomize_ordering_seed', randomize_ordering_seed)
  elif kwargs.get('testRunner') is None:
    kwargs['testRunner'] = _pretty_print_reporter.TextTestRunner

  if FLAGS.pdb_post_mortem:
    runner = kwargs['testRunner']
    # testRunner can be a class or an instance, which must be tested for
    # differently.
    # Overriding testRunner isn't uncommon, so only enable the debugging
    # integration if the runner claims it does; we don't want to accidentally
    # clobber something on the runner.
    if ((isinstance(runner, type) and
         issubclass(runner, _pretty_print_reporter.TextTestRunner)) or
        isinstance(runner, _pretty_print_reporter.TextTestRunner)):
      runner.run_for_debugging = True

  # Make sure tmpdir exists.
  if not os.path.isdir(TEST_TMPDIR.value):
    try:
      os.makedirs(TEST_TMPDIR.value)
    except OSError as e:
      # Concurrent test might have created the directory.
      if e.errno != errno.EEXIST:
        raise

  # Let unittest.TestProgram.__init__ do its own argv parsing, e.g. for '-v',
  # on argv, which is sys.argv without the command-line flags.
  kwargs['argv'] = argv

  # Request unittest.TestProgram to not exit. The exit will be handled by
  # `absltest.run_tests`.
  kwargs['exit'] = False

  try:
    test_program = unittest.TestProgram(*args, **kwargs)
    return test_program.result, fail_when_no_tests_ran
  finally:
    if xml_buffer:
      try:
        with _open(xml_output_file, 'w') as f:
          f.write(xml_buffer.getvalue())
      finally:
        xml_buffer.close()

