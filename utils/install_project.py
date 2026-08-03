import subprocess

def install_project(name, venv, tmp_path, files, *opts):
    project = tmp_path / name
    project.mkdir()
    jaraco.path.build(files, prefix=project)
    opts = [*opts, "--no-build-isolation"]  # force current version of setuptools
    out = venv.run(
        ["python", "-m", "pip", "-v", "install", "-e", str(project), *opts],
        stderr=subprocess.STDOUT,
    )
    return project, out

