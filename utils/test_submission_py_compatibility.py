from pathlib import Path


def test_submission_py_compatibility():
    # Verify that all Python files inside the submission/ directory are Python 3.11 compatible (no PEP 701 nested quotes in f-strings)
    sub_dir = Path(__file__).parent.parent / "submission"
    if sub_dir.exists():
        import ast
        for py_file in sub_dir.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.JoinedStr):
                    for val in node.values:
                        if isinstance(val, ast.FormattedValue):
                            expr_str = ast.unparse(val.value)
                            assert "'" not in expr_str and '"' not in expr_str, f"PEP 701 f-string compatibility error in {py_file.name}: f-string expression contains quotes: {{{expr_str}}}"

