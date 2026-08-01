
def make_decisions_file(tmp_path):
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n", encoding="utf-8")
    return decisions_file

