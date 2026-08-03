from typing import Any

def __parse_range(
        raw_range: str,
        rank_order: RankOrder,
) -> Iterator[frozenset[Card]]:

    def index(r: str) -> int:
        return rank_order.index(r)

    def iterate(ss: Any) -> Iterator[frozenset[Card]]:
        for s0, s1 in ss:
            yield frozenset(Card.parse(f'{r0}{s0}{r1}{s1}'))

    def iterate_plus(s: str) -> Iterator[frozenset[Card]]:
        if r0 == r1:
            r = rank_order[-1]

            yield from __parse_range(f'{r0}{r1}{s}-{r}{r}{s}', rank_order)
        else:
            i0 = index(r0)
            i1 = index(r1)

            if i0 > i1:
                i0, i1 = i1, i0

            for r in rank_order[i0:i1]:
                yield from __parse_range(f'{rank_order[i1]}{r}{s}', rank_order)

    def iterate_interval(s: str) -> Iterator[frozenset[Card]]:
        i0 = index(r0)
        i1 = index(r1)
        i2 = index(r2)
        i3 = index(r3)

        if i1 - i0 != i3 - i2:
            raise ValueError(
                (
                    f'Pattern {repr(raw_range)} is invalid because the two'
                    ' pairs of ranks that bounds the dash-separated notation'
                    ' must be a shifted version of the other.'
                ),
            )

        if i0 > i2:
            i0, i1, i2, i3 = i2, i3, i0, i1

        for ra, rb in zip(
                rank_order[i0:i2 + 1],
                rank_order[i1:i3 + 1],
        ):
            yield from __parse_range(f'{ra}{rb}{s}', rank_order)

    match tuple(raw_range):
        case r0, r1:
            if r0 == r1:
                yield from iterate(combinations(__SUITS, 2))
            else:
                yield from iterate(product(__SUITS, repeat=2))
        case r0, r1, 's':
            if r0 != r1:
                yield from iterate(zip(__SUITS, __SUITS))
        case r0, r1, 'o':
            if r0 == r1:
                yield from __parse_range(f'{r0}{r1}', rank_order)
            else:
                yield from iterate(permutations(__SUITS, 2))
        case r0, r1, '+':
            yield from iterate_plus('')
        case r0, r1, 's', '+':
            yield from iterate_plus('s')
        case r0, r1, 'o', '+':
            yield from iterate_plus('o')
        case r0, r1, '-', r2, r3:
            yield from iterate_interval('')
        case r0, r1, 's', '-', r2, r3, 's':
            yield from iterate_interval('s')
        case r0, r1, 'o', '-', r2, r3, 'o':
            yield from iterate_interval('o')
        case _:
            yield frozenset(Card.parse(raw_range))

