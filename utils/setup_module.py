
def setup_module():
    global old_urlopen

    old_urlopen = urllib_request.urlopen
    urllib_request.urlopen = urlopen_stub


def setup_module():
    """
    Build the required testing extension module

    """
    global wrap

    if wrap is None:
        src = [
            get_testdir() / "wrapmodule.c",
        ]
        wrap = util.build_meson(src, module_name="test_array_from_pyobj_ext")

