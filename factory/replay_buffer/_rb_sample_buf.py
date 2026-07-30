from . import random

def _sample_buf(self, buffer, k, name):
    if not buffer or k == 0: return [], [], []
    priorities = [item[3] for item in buffer]; total_p = sum(priorities)
    probs = [p / total_p for p in priorities]
    indices = random.choices(range(len(buffer)), weights=probs, k=k)
    samples = [buffer[i] for i in indices]; N = len(buffer)
    weights = [(N * (priorities[idx] / total_p)) ** (-self.beta) for idx in indices]
    max_w = max(weights) if weights else 1.0
    return samples, [w / max_w for w in weights], [(name, idx) for idx in indices]
