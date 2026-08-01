import os
import logging
from typing import List

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.distributions import Categorical
except ImportError:
    pass

from factory.ppo_trainer_network import TORCH_AVAILABLE


from utils._compute_gae import _compute_gae


from utils.run_ppo_update import run_ppo_update
