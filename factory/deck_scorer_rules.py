"""
factory/deck_scorer_rules.py

Applies learned do/don't rules to adjust deck scores.
"""

_DRAW_SUPPORTER_NAMES = {"professor's research", "carmine", "lillie",
                         "iono", "judge", "n", "juniper", "sycamore",
                         "colress", "colress's tenacity", "nemona"}


from utils.apply_learned_rules import apply_learned_rules


from utils._deck_out_risk import _deck_out_risk


from utils._matches_condition import _matches_condition
