import json
from typing import Optional
from pathlib import Path


def _load_agent_config(agent_path: Optional[str]) -> tuple[AgentConfig, Optional[str]]:
    """Load server config and prompt."""

    def _read_dir(directory: Path) -> tuple[AgentConfig, Optional[str]]:
        cfg_file = directory / FILENAME_CONFIG
        if not cfg_file.exists():
            raise FileNotFoundError(f" Config file not found in {directory}! Please make sure it exists locally")

        config: AgentConfig = json.loads(cfg_file.read_text(encoding="utf-8"))
        prompt: Optional[str] = None
        for filename in PROMPT_FILENAMES:
            prompt_file = directory / filename
            if prompt_file.exists():
                prompt = prompt_file.read_text(encoding="utf-8")
                break
        return config, prompt

    if agent_path is None:
        return DEFAULT_AGENT, None  # type: ignore

    path = Path(agent_path).expanduser()

    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8")), None

    if path.is_dir():
        return _read_dir(path)

    # fetch from the Hub
    try:
        repo_dir = Path(
            snapshot_download(
                repo_id=DEFAULT_REPO_ID,
                allow_patterns=f"{agent_path}/*",
                repo_type="dataset",
            )
        )
        return _read_dir(repo_dir / agent_path)
    except Exception as err:
        raise EntryNotFoundError(
            f" Agent {agent_path} not found in tiny-agents/tiny-agents! Please make sure it exists in https://huggingface.co/datasets/tiny-agents/tiny-agents."
        ) from err

