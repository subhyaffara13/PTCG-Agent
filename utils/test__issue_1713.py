
def test_Issue_1713(tmp_path):
    rcpath = tmp_path / 'test_rcparams.rc'
    rcpath.write_text('timezone: UTC', encoding='utf-8')
    with mock.patch('locale.getpreferredencoding', return_value='UTF-32-BE'):
        rc = mpl.rc_params_from_file(rcpath, True, False)
    assert rc.get('timezone') == 'UTC'

