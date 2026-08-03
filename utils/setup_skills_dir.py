import json

def setup_skills_dir(tmp_path, filename, content):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / filename).write_text(json.dumps(content), encoding="utf-8")
    return skills_dir

