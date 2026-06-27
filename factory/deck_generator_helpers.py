import math

class DeckMathMixin:
    def hypergeometric_setup_prob(self, deck_size: int, basics_count: int, hand_size: int = 7) -> float:
        """Probability of drawing at least one Basic Pokémon in opening hand."""
        if deck_size <= 0 or basics_count <= 0 or hand_size <= 0: return 0.0
        try: return 1.0 - math.comb(deck_size - basics_count, hand_size) / math.comb(deck_size, hand_size)
        except (ValueError, ZeroDivisionError): return 0.0

    def is_supporter(self, card: dict) -> bool:
        return card.get("card_type") == "Trainer" and "Supporter" in card.get("combo_tags", [])
