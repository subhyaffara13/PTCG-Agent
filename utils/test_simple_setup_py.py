import os
import subprocess
import sys

def test_simple_setup_py(monkeypatch, tmpdir, parallel, std):
    monkeypatch.chdir(tmpdir)
    monkeypatch.syspath_prepend(MAIN_DIR)

    (tmpdir / "setup.py").write_text(
        dedent(
            f"""\
            import sys
            sys.path.append({MAIN_DIR!r})

            from setuptools import setup, Extension
            from pybind11.setup_helpers import build_ext, Pybind11Extension

            std = {std}

            ext_modules = [
                Pybind11Extension(
                    "simple_setup",
                    sorted(["main.cpp"]),
                    cxx_std=std,
                ),
            ]

            cmdclass = dict()
            if std == 0:
                cmdclass["build_ext"] = build_ext


            parallel = {parallel}
            if parallel:
                from pybind11.setup_helpers import ParallelCompile
                ParallelCompile().install()

            setup(
                name="simple_setup_package",
                cmdclass=cmdclass,
                ext_modules=ext_modules,
            )
            """
        ),
        encoding="ascii",
    )

    (tmpdir / "main.cpp").write_text(
        dedent(
            """\
            #include <pybind11/pybind11.h>

            int f(int x) {
                return x * 3;
            }
            PYBIND11_MODULE(simple_setup, m) {
                m.def("f", &f);
            }
            """
        ),
        encoding="ascii",
    )

    out = subprocess.check_output(
        [sys.executable, "setup.py", "build_ext", "--inplace"],
    )
    if not WIN:
        assert b"-g0" in out
    out = subprocess.check_output(
        [sys.executable, "setup.py", "build_ext", "--inplace", "--force"],
        env=dict(os.environ, CFLAGS="-g"),
    )
    if not WIN:
        assert b"-g0" not in out

    # Debug helper printout, normally hidden
    print(out)
    for item in tmpdir.listdir():
        print(item.basename)

    assert (
        len([f for f in tmpdir.listdir() if f.basename.startswith("simple_setup")]) == 1
    )
    assert len(list(tmpdir.listdir())) == 4  # two files + output + build_dir

    (tmpdir / "test.py").write_text(
        dedent(
            """\
            import simple_setup
            assert simple_setup.f(3) == 9
            """
        ),
        encoding="ascii",
    )

    subprocess.check_call(
        [sys.executable, "test.py"], stdout=sys.stdout, stderr=sys.stderr
    )

