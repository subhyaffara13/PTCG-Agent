import datetime
from typing import Any

_PROFILE_THRESHOLDS: list[tuple[float, str]] = [
    (7.0, "aggressive"),
    (4.0, "tempo"),
    (0.0, "defensive"),
]

from utils._score_hand import _score_hand

from utils._mean_ev import _mean_ev

from utils._derive_profile import _derive_profile

from utils._best_card import _best_card

from utils._analyse_packet import _analyse_packet

from utils._build_log_entry import _build_log_entry
