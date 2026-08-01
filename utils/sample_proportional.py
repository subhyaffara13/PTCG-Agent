
def sample_proportional(buffer: deque, k: int) -> List[Any]:
    if not buffer:
        return []
    priorities = [item[3] for item in buffer]
    total_p = sum(priorities)
    probs = [p / total_p for p in priorities]
    
    indices = random.choices(range(len(buffer)), weights=probs, k=k)
    return [buffer[i] for i in indices]

