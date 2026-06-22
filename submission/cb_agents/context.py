"""
agents/context.py

Provides SharedContext, a singleton cache manager for configuration files
(priority_rules.json, strategy_profiles.json, card_scoring.json) to eliminate
redundant, high-frequency disk I/O.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class SharedContext:
    _instance = None
    _caches: Dict[str, Dict[str, Any]] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SharedContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_config(self, skills_dir: str, config_name: str) -> dict:
        """
        Retrieves a loaded config dictionary from the cache, or loads it from disk if not cached.
        
        Parameters
        ----------
        skills_dir : str
            Directory path to the skills configuration directory.
        config_name : str
            Filename of the config (e.g. 'priority_rules.json', 'strategy_profiles.json', 'card_scoring.json').
        """
        resolved_dir = str(Path(skills_dir).resolve())
        
        if resolved_dir not in self._caches:
            self._caches[resolved_dir] = {}
            
        cache = self._caches[resolved_dir]
        
        if config_name not in cache:
            config_path = Path(resolved_dir) / config_name
            loaded_data = {}
            
            if config_path.exists():
                try:
                    loaded_data = json.loads(config_path.read_text(encoding="utf-8"))
                    logger.info(f"Loaded config {config_name} from disk into SharedContext cache for {resolved_dir}")
                except Exception as e:
                    logger.error(f"SharedContext failed to load config {config_name} from {config_path}: {e}")
            else:
                logger.warning(f"SharedContext could not find config {config_name} at {config_path}")
                
            cache[config_name] = loaded_data
            
        return cache[config_name]
