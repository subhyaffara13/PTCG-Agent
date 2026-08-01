"""
cb_agents/lethal_detector.py
Handles opponent damage threat scans and retreat scoring.
"""
import logging

logger = logging.getLogger(__name__)

from utils.evaluate_active_danger import evaluate_active_danger
