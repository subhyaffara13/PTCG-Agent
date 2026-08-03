import os

def check_test_output_files(
    testcase: DataDrivenTestCase, step: int, strip_prefix: str = ""
) -> None:
    for path, expected_content in testcase.output_files:
        path = path.removeprefix(strip_prefix)
        if not os.path.exists(path):
            raise AssertionError(
                "Expected file {} was not produced by test case{}".format(
                    path, " on step %d" % step if testcase.output2 else ""
                )
            )
        with open(path, encoding="utf8") as output_file:
            actual_output_content = output_file.read()

        if isinstance(expected_content, Pattern):
            if expected_content.fullmatch(actual_output_content) is not None:
                continue
            raise AssertionError(
                "Output file {} did not match its expected output pattern\n---\n{}\n---".format(
                    path, actual_output_content
                )
            )

        normalized_output = normalize_file_output(
            actual_output_content.splitlines(), os.path.abspath(test_temp_dir)
        )
        # We always normalize things like timestamp, but only handle operating-system
        # specific things if requested.
        if testcase.normalize_output:
            if testcase.suite.native_sep and os.path.sep == "\\":
                normalized_output = [fix_cobertura_filename(line) for line in normalized_output]
            normalized_output = normalize_error_messages(normalized_output)
        if os.path.basename(testcase.file) == "reports.test":
            normalized_output = normalize_report_meta(normalized_output)
        assert_string_arrays_equal(
            expected_content.splitlines(),
            normalized_output,
            "Output file {} did not match its expected output{}".format(
                path, " on step %d" % step if testcase.output2 else ""
            ),
        )

