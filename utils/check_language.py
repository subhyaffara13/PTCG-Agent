import os
import subprocess
import sys

def check_language(lang, code_snippet=None):
    if sys.platform == "win32":
        pytest.skip("No Fortran tests on Windows (Issue #25134)", allow_module_level=True)
    tmpdir = tempfile.mkdtemp()
    try:
        meson_file = os.path.join(tmpdir, "meson.build")
        with open(meson_file, "w") as f:
            f.write("project('check_compilers')\n")
            f.write(f"add_languages('{lang}')\n")
            if code_snippet:
                f.write(f"{lang}_compiler = meson.get_compiler('{lang}')\n")
                f.write(f"{lang}_code = '''{code_snippet}'''\n")
                f.write(
                    f"_have_{lang}_feature ="
                    f"{lang}_compiler.compiles({lang}_code,"
                    f" name: '{lang} feature check')\n"
                )
        try:
            runmeson = subprocess.run(
                ["meson", "setup", "btmp"],
                check=False,
                cwd=tmpdir,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            pytest.skip("meson not present, skipping compiler dependent test", allow_module_level=True)
        return runmeson.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

