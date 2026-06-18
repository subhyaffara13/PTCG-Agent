import math
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BehavioralVector:
    """
    Represents the playstyle and behavioral footprint of an agent during a game.
    Used for automated diversity mapping, anti-pattern extraction, and clustering.
    """
    turn_aggro: float          # Prize differential slope (0=passive, 1=all-out attack)
    energy_accel_rate: float   # Average energy attached per turn
    hand_disruption: float     # Fraction of trainer plays that disrupt opponent
    setup_duration: float      # Number of turns before first attack
    bench_density: float       # Average bench pokemon count across game
    evolution_depth: float     # Maximum evolution stage achieved (0-2)
    consistency: float         # 1 - stddev of hand_scores across turns

    def to_dict(self) -> dict:
        return {
            "turn_aggro": self.turn_aggro,
            "energy_accel_rate": self.energy_accel_rate,
            "hand_disruption": self.hand_disruption,
            "setup_duration": self.setup_duration,
            "bench_density": self.bench_density,
            "evolution_depth": self.evolution_depth,
            "consistency": self.consistency
        }

    def to_tensor(self) -> List[float]:
        return [
            self.turn_aggro, self.energy_accel_rate, self.hand_disruption,
            self.setup_duration, self.bench_density, self.evolution_depth,
            self.consistency
        ]

    def distance(self, other: 'BehavioralVector') -> float:
        """Euclidean distance between two behavioral vectors."""
        t1 = self.to_tensor()
        t2 = other.to_tensor()
        return math.sqrt(sum((a - b)**2 for a, b in zip(t1, t2)))

def compute_from_steps(steps: List[Dict], player_idx: int) -> BehavioralVector:
    """
    Computes a BehavioralVector for a specific player based on game replay steps.
    """
    if not steps:
        return BehavioralVector(0, 0, 0, 0, 0, 0, 0)

    turns = len(steps)
    total_energy_attached = 0
    disruptive_plays = 0
    total_trainer_plays = 0
    setup_duration = turns
    bench_counts = []
    max_evolution = 0
    hand_scores = []
    
    initial_prizes = 6
    final_prizes = 6

    # Track metrics per turn
    for i, step in enumerate(steps):
        try:
            player_state = step["players"][player_idx]
            obs = player_state.get("observation", {}).get("current", {})
            players = obs.get("players", [])
            if len(players) <= player_idx:
                continue
                
            p_data = players[player_idx]
            
            # Prizes
            if i == 0:
                initial_prizes = len(p_data.get("prize", []))
            final_prizes = len(p_data.get("prize", []))
            
            # Bench density
            bench = p_data.get("bench", [])
            bench_counts.append(len(bench))
            
            # Evolution depth (naive approximation: assume basic is 0, stage 1 is 1, etc.)
            # A true implementation would query CardRegistry for the specific card IDs.
            # We'll default to 0 for this simplified version.
            
            # Setup duration: first time an attack action is taken
            action = player_state.get("action", "")
            if action and "attack" in action.lower() and setup_duration == turns:
                setup_duration = i
                
            # Hand consistency (we'll just use hand size as a proxy if scores aren't in steps)
            hand_size = len(p_data.get("hand", []))
            hand_scores.append(hand_size / 7.0)  # rough normalization
            
            # Energy/Trainer plays require parsing the action history more deeply
            # We use placeholder logic here
            if action and "attach" in action.lower():
                total_energy_attached += 1
            if action and "trainer" in action.lower():
                total_trainer_plays += 1
                if "disrupt" in action.lower():
                    disruptive_plays += 1
                    
        except Exception:
            pass

    prize_diff = max(0, initial_prizes - final_prizes)
    turn_aggro = prize_diff / max(1, turns)
    energy_accel = total_energy_attached / max(1, turns)
    hand_disruption = disruptive_plays / max(1, total_trainer_plays)
    bench_density = sum(bench_counts) / max(1, len(bench_counts))
    
    # Consistency calculation
    avg_score = sum(hand_scores) / max(1, len(hand_scores))
    variance = sum((x - avg_score)**2 for x in hand_scores) / max(1, len(hand_scores))
    consistency = max(0.0, 1.0 - math.sqrt(variance))

    return BehavioralVector(
        turn_aggro=turn_aggro,
        energy_accel_rate=energy_accel,
        hand_disruption=hand_disruption,
        setup_duration=setup_duration,
        bench_density=bench_density,
        evolution_depth=float(max_evolution),
        consistency=consistency
    )

class DiversityTracker:
    """
    Maintains a population of BehavioralVectors and computes the population diversity.
    High diversity ensures the RL agent is exploring a wide range of strategies rather
    than collapsing into a single local optimum.
    """
    def __init__(self):
        self.population: List[BehavioralVector] = []
        
    def add(self, vector: BehavioralVector):
        self.population.append(vector)
        
    def average_distance(self) -> float:
        """Computes average pairwise distance in population."""
        if len(self.population) < 2:
            return 0.0
            
        total_dist = 0.0
        pairs = 0
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                total_dist += self.population[i].distance(self.population[j])
                pairs += 1
                
        return total_dist / pairs
