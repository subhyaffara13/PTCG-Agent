"""
factory/inference_server.py

Centralized batched inference server for MCTS workers.
Collects prediction requests from local/remote threads via a TCP socket,
batches them, runs a single forward pass, and distributes results.
"""
import logging
import threading
import time
import socket
import json
from queue import Queue, Empty
from typing import Optional, Tuple
logger = logging.getLogger(__name__)
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

from ._inferencerequest import _InferenceRequest
from .inferenceserver import InferenceServer
