import os

def venv_python(tmp_path):
    run([*VIRTUALENV, str(tmp_path / ".venv")])
    possible_path = (str(p.parent) for p in tmp_path.glob(".venv/*/python*"))
    return shutil.which("python", path=os.pathsep.join(possible_path))

