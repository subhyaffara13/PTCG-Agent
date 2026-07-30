"""
Lightweight pure-NumPy forward pass for PTCGValueMLP.
Loads PyTorch .pth/.pt checkpoints without importing torch.

Usage:
    python numpy_forward.py                          # try logs/model_weights.pth
    python numpy_forward.py path/to/model_weights.pth # custom path
"""
import zipfile, pickle, io, collections
from pathlib import Path
import numpy as np

from .load_pth import load_pth
from ._load_zip_state import _load_zip_state
from ._load_pickle_state_relu_tanh import _load_pickle_state
from ._load_pickle_state_relu_tanh import relu
from ._load_pickle_state_relu_tanh import tanh
from ._load_pickle_state_relu_tanh import linear
from .ptcgvaluemlpnumpy import PTCGValueMLPNumpy
from .actorcriticnumpy import ActorCriticNumpy
from .state_to_tensor import state_to_tensor
from .main import main
from . import _setup
