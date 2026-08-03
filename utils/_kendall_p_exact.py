import math


def _kendall_p_exact(n, c, alternative='two-sided'):

    # Use the fact that distribution is symmetric: always calculate a CDF in
    # the left tail.
    # This will be the one-sided p-value if `c` is on the side of
    # the null distribution predicted by the alternative hypothesis.
    # The two-sided p-value will be twice this value.
    # If `c` is on the other side of the null distribution, we'll need to
    # take the complement and add back the probability mass at `c`.
    in_right_tail = (c >= (n*(n-1))//2 - c)
    alternative_greater = (alternative == 'greater')
    c = int(min(c, (n*(n-1))//2 - c))

    # Exact p-value, see Maurice G. Kendall, "Rank Correlation Methods"
    # (4th Edition), Charles Griffin & Co., 1970.
    if n <= 0:
        raise ValueError(f'n ({n}) must be positive')
    elif c < 0 or 4*c > n*(n-1):
        raise ValueError(f'c ({c}) must satisfy 0 <= 4c <= n(n-1) = {n*(n-1)}.')
    elif n == 1:
        prob = 1.0
        p_mass_at_c = 1
    elif n == 2:
        prob = 1.0
        p_mass_at_c = 0.5
    elif c == 0:
        prob = 2.0/math.factorial(n) if n < 171 else 0.0
        p_mass_at_c = prob/2
    elif c == 1:
        prob = 2.0/math.factorial(n-1) if n < 172 else 0.0
        p_mass_at_c = (n-1)/math.factorial(n)
    elif 4*c == n*(n-1) and alternative == 'two-sided':
        # I'm sure there's a simple formula for p_mass_at_c in this
        # case, but I don't know it. Use generic formula for one-sided p-value.
        prob = 1.0
    elif n < 171:
        new = np.zeros(c+1)
        new[0:2] = 1.0
        for j in range(3,n+1):
            new = np.cumsum(new)
            if j <= c:
                new[j:] -= new[:c+1-j]
        prob = 2.0*np.sum(new)/math.factorial(n)
        p_mass_at_c = new[-1]/math.factorial(n)
    else:
        new = np.zeros(c+1)
        new[0:2] = 1.0
        for j in range(3, n+1):
            new = np.cumsum(new)/j
            if j <= c:
                new[j:] -= new[:c+1-j]
        prob = np.sum(new)
        p_mass_at_c = new[-1]/2

    if alternative != 'two-sided':
        # if the alternative hypothesis and alternative agree,
        # one-sided p-value is half the two-sided p-value
        if in_right_tail == alternative_greater:
            prob /= 2
        else:
            prob = 1 - prob/2 + p_mass_at_c

    prob = np.clip(prob, 0, 1)

    return prob

