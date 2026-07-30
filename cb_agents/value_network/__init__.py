import random, logging
from abc import ABC, abstractmethod
from typing import List, Any
from dataclasses import dataclass
from pathlib import Path
import os
from cb_agents.state_cache import gs_hash
try:
    import torch
except ImportError:
    class MockNoGrad:
        def __enter__(self): return self
        def __exit__(self, *args): pass
    class MockTorch:
        no_grad = MockNoGrad
        def __getattr__(self, name):
            raise ImportError(f"PyTorch is not installed. Cannot access torch.{name}")
    torch = MockTorch()
logger = logging.getLogger(__name__)

from .__getattr___actionprior_basevaluenetwork import __getattr__
from .__getattr___actionprior_basevaluenetwork import ActionPrior
from .__getattr___actionprior_basevaluenetwork import BaseValueNetwork
from .neuralvaluenetwork import NeuralValueNetwork
from .basepolicynetwork_heuristicpolicynetwork import BasePolicyNetwork
from .basepolicynetwork_heuristicpolicynetwork import HeuristicPolicyNetwork
from .ppopolicynetwork import PPOPolicyNetwork
from .ppovaluenetwork import PPOValueNetwork
