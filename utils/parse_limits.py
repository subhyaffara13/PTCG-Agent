
def parseLimits(limits: Iterable[str]) -> Dict[str, Optional[AxisTriple]]:
    result = {}
    for limitString in limits:
        match = re.match(
            r"^(\w{1,4})=(?:(drop)|(?:([^:]*)(?:[:]([^:]*))?(?:[:]([^:]*))?))$",
            limitString,
        )
        if not match:
            raise ValueError("invalid location format: %r" % limitString)
        tag = match.group(1).ljust(4)

        if match.group(2):  # 'drop'
            result[tag] = None
            continue

        triple = match.group(3, 4, 5)

        if triple[1] is None:  # "value" syntax
            triple = (triple[0], triple[0], triple[0])
        elif triple[2] is None:  # "min:max" syntax
            triple = (triple[0], None, triple[1])

        triple = tuple(float(v) if v else None for v in triple)

        result[tag] = AxisTriple(*triple)

    return result

