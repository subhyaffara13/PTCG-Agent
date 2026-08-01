
def _cases(version, filt='test%(name)s_*.mat'):
    if version == '4':
        cases = case_table4
    elif version == '5':
        cases = case_table5
    else:
        assert version == '5_rt'
        cases = case_table5_rt
    for case in cases:
        name = case['name']
        expected = case['expected']
        if filt is None:
            files = None
        else:
            use_filt = pjoin(test_data_path, filt % dict(name=name))
            files = glob(use_filt)
            assert len(files) > 0, \
                f"No files for test {name} using filter {filt}"
        classes = case['classes']
        yield name, files, expected, classes

