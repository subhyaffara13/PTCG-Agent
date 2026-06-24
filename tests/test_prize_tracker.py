"""
tests/test_prize_tracker.py
Unit tests for agents/prize_tracker.py.
"""
from agents.prize_tracker import PrizeTracker

def test_prize_tracker_calculation():
    # Deck of 10 cards: 4 Pikachus (721), 2 Raichus (722), 4 Energies (3)
    deck = [721, 721, 721, 721, 722, 722, 3, 3, 3, 3]
    tracker = PrizeTracker(deck)
    
    # Visible cards: 2 Pikachus, 1 Raichu, 2 Energies (total 5 visible cards)
    visible = [721, 721, 722, 3, 3]
    
    # Remaining unseen hidden cards = 10 - 5 = 5 cards
    # Remaining unseen hidden cards composition: 2 Pikachus, 1 Raichu, 2 Energies
    # Prizes remaining = 2
    probs = tracker.calculate_prized_probabilities(visible, prizes_remaining=2)
    
    # P(Pikachu is prized)
    # Total unseen: 5. Unseen Pikachus: 2.
    # Ways to choose 2 prizes from 5 unseen: comb(5, 2) = 10
    # Ways to avoid Pikachus: comb(5 - 2, 2) = comb(3, 2) = 3
    # P(avoid Pikachu prized) = 3/10 = 0.3
    # P(at least 1 Pikachu prized) = 1 - 0.3 = 0.7
    assert round(probs[721], 2) == 0.70
    
    # P(Raichu is prized)
    # Unseen Raichu: 1.
    # Ways to avoid Raichu: comb(5 - 1, 2) = comb(4, 2) = 6
    # P(avoid Raichu prized) = 6/10 = 0.6
    # P(at least 1 Raichu prized) = 1 - 0.6 = 0.4
    assert round(probs[722], 2) == 0.40
