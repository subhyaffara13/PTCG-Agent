from pathlib import Path


def Node_fspath_set(self: Node, value: LEGACY_PATH) -> None:
    self.path = Path(value)

