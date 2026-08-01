
def calculate_icm(
        payouts: Iterable[float],
        chips: Iterable[float],
) -> tuple[float, ...]:
    """Calculate the independent chip model (ICM) values.

    >>> calculate_icm([70, 30], [50, 30, 20])  # doctest: +ELLIPSIS
    (45.17..., 32.25, 22.57...)
    >>> calculate_icm([50, 30, 20], [25, 87, 88])  # doctest: +ELLIPSIS
    (25.69..., 37.08..., 37.21...)
    >>> calculate_icm([50, 30, 20], [21, 89, 90])  # doctest: +ELLIPSIS
    (24.85..., 37.51..., 37.63...)
    >>> calculate_icm([50, 30, 20], [198, 1, 1])  # doctest: +ELLIPSIS
    (49.79..., 25.10..., 25.10...)

    :param payouts: The payouts.
    :param chips: The players' chips.
    :return: The ICM values.
    """
    payouts = tuple(payouts)
    chips = tuple(chips)
    chip_sum = sum(chips)
    chip_percentages = [chip / chip_sum for chip in chips]
    icms = [0.0] * len(chips)

    for player_indices in permutations(range(len(chips)), len(payouts)):
        probability = 1.0
        denominator = 1.0

        for player_index in player_indices:
            chip_percentage = chip_percentages[player_index]
            probability *= chip_percentage / denominator
            denominator -= chip_percentage

        for payout, player_index in zip(payouts, player_indices):
            icms[player_index] += payout * probability

    return tuple(icms)

