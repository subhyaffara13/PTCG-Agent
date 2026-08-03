import sys
import os
import time
import math
import random
import logging

logger = logging.getLogger(__name__)

def agent(observation, configuration=None):
    """
    Main agent entry point for Kaggle environment evaluation.
    """
    DEFAULT_DECK = [
        957, 957, 957, 979, 979, 979, 37, 37, 37, 210,
        210, 210, 1121, 1227, 1227, 1227, 1227, 1152, 1152, 1152,
        1152, 1210, 1210, 1210, 1194, 1194, 1194, 1211, 1198, 1256,
        1097, 1097, 1097, 1097, 1182, 1182, 1182, 1182, 1102, 1086,
        1086, 1086, 1086, 1123, 1081, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]
    if observation is None:
        return DEFAULT_DECK

    if hasattr(observation, "step") and getattr(observation, "step") == 0:
        return DEFAULT_DECK

    return [0]
