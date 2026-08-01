
def _pep621_example_project(
    tmp_path,
    readme="README.rst",
    pyproject_text=PEP621_EXAMPLE,
):
    pyproject = tmp_path / "pyproject.toml"
    text = pyproject_text
    replacements = {'readme = "README.rst"': f'readme = "{readme}"'}
    for orig, subst in replacements.items():
        text = text.replace(orig, subst)
    pyproject.write_text(text, encoding="utf-8")

    (tmp_path / readme).write_text("hello world", encoding="utf-8")
    (tmp_path / "LICENSE.txt").write_text("--- LICENSE stub ---", encoding="utf-8")
    (tmp_path / "spam.py").write_text(PEP621_EXAMPLE_SCRIPT, encoding="utf-8")
    return pyproject

