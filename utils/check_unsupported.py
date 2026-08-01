
def check_unsupported(
    packages: Iterable[BaseDistribution],
    supported_tags: Iterable[Tag],
) -> Generator[BaseDistribution, None, None]:
    for p in packages:
        with suppress(FileNotFoundError):
            wheel_file = p.read_text("WHEEL")
            wheel_tags: frozenset[Tag] = reduce(
                frozenset.union,
                map(parse_tag, Parser().parsestr(wheel_file).get_all("Tag", [])),
                frozenset(),
            )
            if wheel_tags.isdisjoint(supported_tags):
                yield p

