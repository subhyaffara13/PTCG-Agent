import json
import pickle
import base64
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class WorkOrder:
    job_id: str
    iteration: int
    worker_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    deck_base: Optional[list] = None
    deck_new: Optional[list] = None

    def serialize(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def deserialize(data: str) -> 'WorkOrder':
        return WorkOrder(**json.loads(data))


@dataclass
class GameResult:
    job_id: str
    iteration: int
    worker_id: str
    metrics: Dict[str, float]
    # We can store larger objects like serialized replays via pickle + base64 if needed
    replay_data_b64: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None

    def serialize(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def deserialize(data: str) -> 'GameResult':
        return GameResult(**json.loads(data))

    def set_replay(self, replay_obj: Any):
        self.replay_data_b64 = base64.b64encode(pickle.dumps(replay_obj)).decode('utf-8')

    def get_replay(self) -> Any:
        if self.replay_data_b64:
            return pickle.loads(base64.b64decode(self.replay_data_b64.encode('utf-8')))
        return None
