"""Helper: rewrite strategy_agent.py with the correct content."""
import pathlib

from rewrite_strategy_cfg_a import STRATEGY_AGENT_CONTENT_A
from rewrite_strategy_cfg_b import STRATEGY_AGENT_CONTENT_B

target = pathlib.Path("agents/strategy_agent.py")
target.write_text(STRATEGY_AGENT_CONTENT_A + STRATEGY_AGENT_CONTENT_B, encoding="utf-8")
print(f"Written {target}  ({target.stat().st_size} bytes)")
