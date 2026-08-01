
def question(q):
    return input(f"\n{q.rstrip(' ')} (y/n): ").lower().strip() == "y"

