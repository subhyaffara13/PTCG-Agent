"""
tests/test_deck_architect.py

Unit tests for factory/deck_architect.py.
"""
import json
import csv
import pytest
from factory.deck_architect import DeckArchitect
from test_deck_architect_helpers import (
    CARD_POOL_BASIC, CARD_POOL_REALISTIC, CSV_DATA, ARCHETYPES_DATA,
    make_skills_dir, make_decisions_file, make_staging_dir
)

from utils.test_deck_architect_build_fallback import test_deck_architect_build_fallback

from utils.test_supercharged_deck_rules import test_supercharged_deck_rules

from utils.test_genetic_mutation_copy_limits import test_genetic_mutation_copy_limits
