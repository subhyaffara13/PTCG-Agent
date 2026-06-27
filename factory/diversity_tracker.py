from typing import List
from factory.behavioral_features import BehavioralVector

class DiversityTracker:
    def __init__(self):
        self.population: List[BehavioralVector] = []
        
    def add(self, vector: BehavioralVector):
        self.population.append(vector)
        
    def average_distance(self) -> float:
        if len(self.population) < 2:
            return 0.0
            
        total_dist = 0.0
        pairs = 0
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                total_dist += self.population[i].distance(self.population[j])
                pairs += 1
                
        return total_dist / pairs
