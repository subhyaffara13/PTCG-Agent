from pathlib import Path


def load_template(name: str, template_dir: Path) -> str:
    """Load a template file and return its content."""
    with open(template_dir / f"{name}.py.jinja") as f:
        return f.read()

