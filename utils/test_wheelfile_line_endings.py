
def test_wheelfile_line_endings(wheel_paths):
    for path in wheel_paths:
        with ZipFile(path) as wf:
            wheelfile = next(fn for fn in wf.filelist if fn.filename.endswith("WHEEL"))
            wheelfile_contents = wf.read(wheelfile)
            assert b"\r" not in wheelfile_contents

