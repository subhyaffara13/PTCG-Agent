
def _whos_check_case(name, files, case, classes):
    for file_name in files:
        label = f"test {name}; file {file_name}"

        whos = whosmat(file_name)

        expected_whos = [
            (k, expected.shape, classes[k]) for k, expected in case.items()]

        whos.sort()
        expected_whos.sort()
        assert_equal(whos, expected_whos,
                     f"{label}: {whos!r} != {expected_whos!r}"
                     )

