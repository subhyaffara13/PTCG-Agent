
def _load_check_case(name, files, case):
    for file_name in files:
        matdict = loadmat(file_name, struct_as_record=True, spmatrix=False)
        label = f"test {name}; file {file_name}"
        for k, expected in case.items():
            k_label = f"{label}, variable {k}"
            assert_(k in matdict, f"Missing key at {k_label}")
            _check_level(k_label, expected, matdict[k])

