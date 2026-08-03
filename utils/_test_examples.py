import os

def _test_examples(in_filename, out_filename, test_name=""):

    in_file_path = os.path.join(FILE_DIR, 'autolev', 'test-examples',
                                in_filename)
    correct_file_path = os.path.join(FILE_DIR, 'autolev', 'test-examples',
                                     out_filename)
    with open(in_file_path) as f:
        generated_code = parse_autolev(f, include_numeric=True)

    with open(correct_file_path) as f:
        for idx, line1 in enumerate(f):
            if line1.startswith("#"):
                break
            try:
                line2 = generated_code.split('\n')[idx]
                assert line1.rstrip() == line2.rstrip()
            except Exception:
                msg = 'mismatch in ' + test_name + ' in line no: {0}'
                raise AssertionError(msg.format(idx+1))

