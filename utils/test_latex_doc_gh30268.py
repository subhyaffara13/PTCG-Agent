import subprocess
import sys

def test_latex_doc_gh30268(tmp_path):

    if not util.has_fortran_compiler():
        pytest.skip("No Fortran compiler found")

    fsource = textwrap.dedent("""
        subroutine foo
        end
    """)

    fpath = tmp_path / "test_latex.f90"
    with open(fpath, "w") as f:
        f.write(fsource)

    cmd = [sys.executable, "-m", "numpy.f2py", "-c", str(fpath), "-m", "test_latex", "--latex-doc"]
    subprocess.check_call(cmd, cwd=tmp_path)

