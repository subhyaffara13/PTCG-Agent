from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from collections.abc import Mapping

logger = logging.getLogger(__name__)

class LazyDict(Mapping):
    """A proxy dictionary that defers loading from disk until a key is accessed."""
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._data: Optional[Dict[Any, Any]] = None

    def _load(self) -> Dict[Any, Any]:
        if self._data is None:
            if self._file_path.exists():
                try:
                    self._data = json.loads(self._file_path.read_text(encoding="utf-8"))
                    logger.debug(f"LazyDict dynamically loaded: {self._file_path.name}")
                except Exception as e:
                    logger.error(f"LazyDict failed to load {self._file_path.name}: {e}")
                    self._data = {}
            else:
                self._data = {}
        return self._data or {}

    def __getitem__(self, key: Any) -> Any:
        return self._load()[key]

    def __iter__(self):
        return iter(self._load())

    def __len__(self) -> int:
        return len(self._load())
        
    def get(self, key: Any, default: Any = None) -> Any:
        return self._load().get(key, default)

class SharedContext:
    _instance: Optional[SharedContext] = None
    _caches: Dict[str, Dict[str, Any]] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> SharedContext:
        if not cls._instance:
            cls._instance = super(SharedContext, cls).__new__(cls, *args, **kwargs)
            cls._instance._caches = {}
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
            cache[config_name] = LazyDict(config_path)
            
        return cache[config_name]
