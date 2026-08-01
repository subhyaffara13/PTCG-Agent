
def test_single_path(tmp_path):
    mpl.rcParams[PARAM] = 'gray'
    path = tmp_path / 'text.mplstyle'
    path.write_text(f'{PARAM} : {VALUE}', encoding='utf-8')
    with style.context(path):
        assert mpl.rcParams[PARAM] == VALUE
    assert mpl.rcParams[PARAM] == 'gray'

