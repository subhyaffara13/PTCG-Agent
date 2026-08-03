from typing import Callable

def anchors_plugin(
    md: MarkdownIt,
    min_level: int = 1,
    max_level: int = 2,
    slug_func: Callable[[str], str] | None = None,
    permalink: bool = False,
    permalinkSymbol: str = "¶",
    permalinkBefore: bool = False,
    permalinkSpace: bool = True,
) -> None:
    """Plugin for adding header anchors, based on
    `markdown-it-anchor <https://github.com/valeriangalliat/markdown-it-anchor>`__

    .. code-block:: md

        # Title String

    renders as:

    .. code-block:: html

        <h1 id="title-string">Title String <a class="header-anchor" href="#title-string">¶</a></h1>

    :param min_level: minimum header level to apply anchors
    :param max_level: maximum header level to apply anchors
    :param slug_func: function to convert title text to id slug.
    :param permalink: Add a permalink next to the title
    :param permalinkSymbol: the symbol to show
    :param permalinkBefore: Add the permalink before the title, otherwise after
    :param permalinkSpace: Add a space between the permalink and the title

    Note, the default slug function aims to mimic the GitHub Markdown format, see:

    - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb
    - https://gist.github.com/asabaylus/3071099

    """
    selected_levels = list(range(min_level, max_level + 1))
    md.core.ruler.push(
        "anchor",
        _make_anchors_func(
            selected_levels,
            slug_func or slugify,
            permalink,
            permalinkSymbol,
            permalinkBefore,
            permalinkSpace,
        ),
    )

