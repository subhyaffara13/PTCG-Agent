
def cumulative_distribution(distribution):
    """Returns normalized cumulative distribution from discrete distribution."""

    cdf = [0.0]
    cumulative = 0.0
    for element in distribution:
        cumulative += element
        cdf.append(cumulative)
    return [element / cumulative for element in cdf]

