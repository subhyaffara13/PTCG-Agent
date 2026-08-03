import json
import os
import subprocess
import sys
from typing import Any

def run_tests(needs: str | tuple[str, ...] = ()) -> None:
    from torch.testing._internal.common_utils import run_tests

    if TEST_WITH_TORCHDYNAMO or TEST_WITH_CROSSREF:
        return  # skip testing

    if (
        not torch.xpu.is_available()
        and IS_WINDOWS
        and os.environ.get("TORCHINDUCTOR_WINDOWS_TESTS", "0") == "0"
    ):
        return

    if isinstance(needs, str):
        needs = (needs,)
    for need in needs:
        if need == "cuda":
            if not torch.cuda.is_available():
                return
        else:
            try:
                importlib.import_module(need)
            except ImportError:
                return

    run_tests()


def run_tests(needs: str | tuple[str, ...] = ()) -> None:
    dynamo_run_tests(needs)


def run_tests(argv=None):
    parse_cmd_line_args()
    if argv is None:
        argv = UNITTEST_ARGS

    # import test files.
    if SLOW_TESTS_FILE:
        if os.path.exists(SLOW_TESTS_FILE):
            with open(SLOW_TESTS_FILE) as fp:
                global slow_tests_dict
                slow_tests_dict = json.load(fp)
                # use env vars so pytest-xdist subprocesses can still access them
                os.environ['SLOW_TESTS_FILE'] = SLOW_TESTS_FILE
        else:
            warnings.warn(f'slow test file provided but not found: {SLOW_TESTS_FILE}', stacklevel=2)
    if DISABLED_TESTS_FILE:
        if os.path.exists(DISABLED_TESTS_FILE):
            with open(DISABLED_TESTS_FILE) as fp:
                global disabled_tests_dict
                disabled_tests_dict = json.load(fp)
                os.environ['DISABLED_TESTS_FILE'] = DISABLED_TESTS_FILE
        else:
            warnings.warn(f'disabled test file provided but not found: {DISABLED_TESTS_FILE}', stacklevel=2)
    # Determine the test launch mechanism
    if TEST_DISCOVER:
        _print_test_names()
        return

    # Before running the tests, lint to check that every test class extends from TestCase
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    if not lint_test_case_extension(suite):
        sys.exit(1)

    if SHOWLOCALS:
        argv = [
            argv[0],
            *(["--showlocals", "--tb=long", "--color=yes"] if USE_PYTEST else ["--locals"]),
            *argv[1:],
        ]

    if TEST_IN_SUBPROCESS:
        other_args = []
        if DISABLED_TESTS_FILE:
            other_args.append("--import-disabled-tests")
        if SLOW_TESTS_FILE:
            other_args.append("--import-slow-tests")
        if USE_PYTEST:
            other_args.append("--use-pytest")
        if RERUN_DISABLED_TESTS:
            other_args.append("--rerun-disabled-tests")
        if TEST_SAVE_XML:
            other_args += ['--save-xml', TEST_SAVE_XML]

        test_cases = (
            get_pytest_test_cases(argv) if USE_PYTEST else
            [case.id().split('.', 1)[1] for case in discover_test_cases_recursively(suite)]
        )

        failed_tests = []

        for test_case_full_name in test_cases:

            cmd = (
                [sys.executable] + [argv[0]] + other_args + argv[1:] +
                (["--pytest-single-test"] if USE_PYTEST else []) +
                [test_case_full_name]
            )
            string_cmd = " ".join(cmd)

            timeout = None if RERUN_DISABLED_TESTS else 15 * 60

            exitcode, _ = retry_shell(cmd, timeout=timeout, retries=0 if RERUN_DISABLED_TESTS else 1)

            if exitcode != 0:
                # This is sort of hacky, but add on relevant env variables for distributed tests.
                if 'TestDistBackendWithSpawn' in test_case_full_name:
                    backend = os.environ.get("BACKEND", "")
                    world_size = os.environ.get("WORLD_SIZE", "")
                    env_prefix = f"BACKEND={backend} WORLD_SIZE={world_size}"
                    string_cmd = env_prefix + " " + string_cmd
                # Log the command to reproduce the failure.
                print(f"Test exited with non-zero exitcode {exitcode}. Command to reproduce: {string_cmd}")
                failed_tests.append(test_case_full_name)

        if len(failed_tests) != 0:
            raise AssertionError(
                "{} unit test(s) failed:\n\t{}".format(
                    len(failed_tests), '\n\t'.join(failed_tests)
                )
            )

    elif RUN_PARALLEL > 1:
        test_cases = discover_test_cases_recursively(suite)
        test_batches = chunk_list(get_test_names(test_cases), RUN_PARALLEL)
        processes = []
        for i in range(RUN_PARALLEL):
            command = [sys.executable] + argv + [f'--log-suffix=-shard-{i + 1}'] + test_batches[i]
            processes.append(subprocess.Popen(command, universal_newlines=True))
        failed = False
        for p in processes:
            failed |= wait_for_process(p) != 0
        if failed:
            raise AssertionError("Some test shards have failed")
    elif USE_PYTEST:
        pytest_args = argv + ["--use-main-module"]
        test_report_path = ""
        if TEST_SAVE_XML:
            test_report_path = get_report_path(pytest=True)
            print(f'Test results will be stored in {test_report_path}')
            pytest_args.append(f'--junit-xml-reruns={test_report_path}')
        if PYTEST_SINGLE_TEST:
            pytest_args = PYTEST_SINGLE_TEST + pytest_args[1:]

        import pytest
        os.environ["NO_COLOR"] = "1"
        exit_code = pytest.main(args=pytest_args)
        if TEST_SAVE_XML:
            sanitize_pytest_xml(test_report_path)

        # exitcode of 5 means no tests were found, which happens since some test configs don't
        # run tests from certain files
        sys.exit(0 if exit_code == 5 else exit_code)
    elif TEST_SAVE_XML:
        # import here so that non-CI doesn't need xmlrunner installed
        import xmlrunner  # type: ignore[import]
        from xmlrunner.result import _XMLTestResult  # type: ignore[import]

        class XMLTestResultVerbose(_XMLTestResult):
            """
            Adding verbosity to test outputs:
            by default test summary prints 'skip',
            but we want to also print the skip reason.
            GH issue: https://github.com/pytorch/pytorch/issues/69014

            This works with unittest_xml_reporting<=3.2.0,>=2.0.0
            (3.2.0 is latest at the moment)
            """

            def addSkip(self, test, reason):
                super().addSkip(test, reason)
                for c in self.callback.__closure__:
                    if isinstance(c.cell_contents, str) and c.cell_contents == 'skip':
                        # this message is printed in test summary;
                        # it stands for `verbose_str` captured in the closure
                        c.cell_contents = f"skip: {reason}"

            def printErrors(self) -> None:
                super().printErrors()
                self.printErrorList("XPASS", self.unexpectedSuccesses)
        test_report_path = get_report_path()
        verbose = '--verbose' in argv or '-v' in argv
        if verbose:
            print(f'Test results will be stored in {test_report_path}')
        unittest.main(argv=argv, testRunner=xmlrunner.XMLTestRunner(
            output=test_report_path,
            verbosity=2 if verbose else 1,
            resultclass=XMLTestResultVerbose))
    elif REPEAT_COUNT > 1:
        for _ in range(REPEAT_COUNT):
            if not unittest.main(exit=False, argv=argv).result.wasSuccessful():
                sys.exit(-1)
    else:
        unittest.main(argv=argv)


def run_tests(
    use_compact_memory=True,
    run_torch=False,
    run_memory=True,
    use_io_binding=True,
    use_fp16=True,
    use_merged_qkv_weights=True,
    use_half4=True,
    batch_size=1,
):
    compact_memory = "1" if use_compact_memory else "0"
    os.environ["ORT_LONGFORMER_COMPACT_MEMORY"] = compact_memory
    logger.info(f"ORT_LONGFORMER_COMPACT_MEMORY={compact_memory}")

    os.environ["ORT_LONGFORMER_USE_HALF4"] = "1" if use_half4 else "0"
    logger.info("ORT_LONGFORMER_USE_HALF4={}".format("1" if use_half4 else "0"))  # noqa: G001

    results = []
    test_times = 1000
    sequence_lengths = [4096, 2048, 1024, 512]
    batch_sizes = [batch_size]
    for model_name in ["longformer-base-4096"]:
        for batch_size in batch_sizes:
            for sequence_length in sequence_lengths:
                for global_length in [16]:
                    if run_torch:
                        engine_name = "torch"
                        args = parse_arguments(
                            f"-e {engine_name} -t {test_times} -b {batch_size} -s {sequence_length} -g {global_length} "
                            f"-t {test_times} -m {model_name}".split(" ")
                        )
                        results += run(args)

                    engine_name = "onnxruntime"
                    file_format = 1 if use_merged_qkv_weights else 0
                    onnx_path = (
                        f"{model_name}_f{file_format}_fp16.onnx"
                        if use_fp16
                        else f"{model_name}_f{file_format}_fp32.onnx"
                    )
                    if not os.path.exists(onnx_path):
                        raise RuntimeError(f"onnx file not exists:{onnx_path}")

                    arguments = (
                        f"-e {engine_name} --onnx {onnx_path} "
                        f"-b {batch_size} -s {sequence_length} -g {global_length} -m {model_name}"
                    )

                    if not use_io_binding:
                        arguments += " --disable_io_binding"

                    if use_half4:
                        arguments += " --use_half4"

                    # Disable parity test to avoid out of memory for large batch size
                    if batch_size >= 4:
                        arguments += " --disable_parity"

                    memory_results = None
                    try:
                        if run_memory:
                            args = parse_arguments(f"{arguments} -t 10 --memory".split(" "))
                            memory_results = launch_test(args)

                        args = parse_arguments(f"{arguments} -t {test_times}".split(" "))
                        latency_results = launch_test(args)
                    except KeyboardInterrupt as exc:
                        raise RuntimeError("Keyboard Interrupted") from exc
                    except Exception:
                        traceback.print_exc()
                        continue

                    if len(latency_results) == 1:
                        latency_results[0]["memory"] = memory_results[0]["memory"] if memory_results else "N/A"
                    else:
                        raise RuntimeError("length of latency_results should be 1")

                    logger.info("%s", latency_results)

                    results += latency_results
    return results


def run_tests(
    argv: abc.MutableSequence[str],
    args: abc.Sequence[Any],
    kwargs: abc.MutableMapping[str, Any],
) -> None:
  """Executes a set of Python unit tests.

  Most users should call absltest.main() instead of run_tests.

  Please note that run_tests should be called from app.run.
  Calling absltest.main() would ensure that.

  Please note that run_tests is allowed to make changes to kwargs.

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
  """
  result, fail_when_no_tests_ran = _run_and_get_tests_result(
      argv, args, kwargs, xml_reporter.TextAndXMLTestRunner
  )
  if fail_when_no_tests_ran and result.testsRun == 0 and not result.skipped:
    # Python 3.12 unittest exits with 5 when no tests ran. The exit code 5 comes
    # from pytest which does the same thing.
    sys.exit(5)
  sys.exit(not result.wasSuccessful())

