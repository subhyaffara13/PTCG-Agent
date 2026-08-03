from pathlib import Path


def _get_token_from_file() -> str | None:
    try:
        return _clean_token(Path(constants.HF_TOKEN_PATH).read_text())
    except FileNotFoundError:
        return None

