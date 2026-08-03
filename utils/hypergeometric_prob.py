import math


def hypergeometric_prob(N: int, K: int, n: int) -> float:
    """
    Probability of exactly 1 success in n draws from N total with K successes.
    Returns the probability of drawing AT LEAST ONE.
    """
    if N <= 0 or K <= 0 or n <= 0 or N < K:
        return 0.0
    if N <= n:
        return 1.0
    
    try:
        prob_zero = math.comb(N - K, n) / math.comb(N, n)
        return 1.0 - prob_zero
    except ValueError:
        if N - K < n:
            return 1.0
        return 0.0


def hypergeometric_prob(N: int, K: int, n: int) -> float:
    """
    Probability of exactly 1 success in n draws from N total with K successes.
    Returns the probability of drawing AT LEAST ONE.
    """
    if N <= 0 or K <= 0 or n <= 0 or N < K:
        return 0.0
    if N <= n:
        return 1.0
    
    try:
        prob_zero = math.comb(N - K, n) / math.comb(N, n)
        return 1.0 - prob_zero
    except ValueError:
        if N - K < n:
            return 1.0
        return 0.0


def hypergeometric_prob(N: int, K: int, n: int) -> float:
    """
    Probability of exactly 1 success in n draws from N total with K successes.
    Returns the probability of drawing AT LEAST ONE.
    """
    if N <= 0 or K <= 0 or n <= 0 or N < K:
        return 0.0
    if N <= n:
        return 1.0
    
    try:
        prob_zero = math.comb(N - K, n) / math.comb(N, n)
        return 1.0 - prob_zero
    except ValueError:
        if N - K < n:
            return 1.0
        return 0.0

