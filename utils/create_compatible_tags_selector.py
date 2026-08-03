from typing import Callable

def create_compatible_tags_selector(
    tags: Iterable[Tag],
) -> Callable[[Iterable[tuple[_T, AbstractSet[Tag]]]], Iterator[_T]]:
    """Create a callable to select things compatible with supported tags.

    This function accepts an ordered sequence of tags, with the preferred
    tags first.

    The returned callable accepts an iterable of tuples (thing, set[Tag]),
    and returns an iterator of things, with the things with the best
    matching tags first.

    Example to select compatible wheel filenames:

    >>> from packaging import tags
    >>> from packaging.utils import parse_wheel_filename
    >>> selector = tags.create_compatible_tags_selector(tags.sys_tags())
    >>> filenames = ["foo-1.0-py3-none-any.whl", "foo-1.0-py2-none-any.whl"]
    >>> list(selector([
    ...     (filename, parse_wheel_filename(filename)[-1]) for filename in filenames
    ... ]))
    ['foo-1.0-py3-none-any.whl']

    .. versionadded:: 26.1
    """
    tag_ranks: dict[Tag, int] = {}
    for rank, tag in enumerate(tags):
        tag_ranks.setdefault(tag, rank)  # ignore duplicate tags, keep first
    supported_tags = tag_ranks.keys()

    def selector(
        tagged_things: Iterable[tuple[_T, AbstractSet[Tag]]],
    ) -> Iterator[_T]:
        ranked_things: list[tuple[_T, int]] = []
        for thing, thing_tags in tagged_things:
            supported_thing_tags = thing_tags & supported_tags
            if supported_thing_tags:
                thing_rank = min(tag_ranks[t] for t in supported_thing_tags)
                ranked_things.append((thing, thing_rank))
        return iter(
            thing for thing, _ in sorted(ranked_things, key=operator.itemgetter(1))
        )

    return selector


def create_compatible_tags_selector(
    tags: Iterable[Tag],
) -> Callable[[Iterable[tuple[_T, AbstractSet[Tag]]]], Iterator[_T]]:
    """Create a callable to select things compatible with supported tags.

    This function accepts an ordered sequence of tags, with the preferred
    tags first.

    The returned callable accepts an iterable of tuples (thing, set[Tag]),
    and returns an iterator of things, with the things with the best
    matching tags first.

    Example to select compatible wheel filenames:

    >>> from packaging import tags
    >>> from packaging.utils import parse_wheel_filename
    >>> selector = tags.create_compatible_tags_selector(tags.sys_tags())
    >>> filenames = ["foo-1.0-py3-none-any.whl", "foo-1.0-py2-none-any.whl"]
    >>> list(selector([
    ...     (filename, parse_wheel_filename(filename)[-1]) for filename in filenames
    ... ]))
    ['foo-1.0-py3-none-any.whl']

    .. versionadded:: 26.1
    """
    tag_ranks: dict[Tag, int] = {}
    for rank, tag in enumerate(tags):
        tag_ranks.setdefault(tag, rank)  # ignore duplicate tags, keep first
    supported_tags = tag_ranks.keys()

    def selector(
        tagged_things: Iterable[tuple[_T, AbstractSet[Tag]]],
    ) -> Iterator[_T]:
        ranked_things: list[tuple[_T, int]] = []
        for thing, thing_tags in tagged_things:
            supported_thing_tags = thing_tags & supported_tags
            if supported_thing_tags:
                thing_rank = min(tag_ranks[t] for t in supported_thing_tags)
                ranked_things.append((thing, thing_rank))
        return iter(
            thing for thing, _ in sorted(ranked_things, key=operator.itemgetter(1))
        )

    return selector

