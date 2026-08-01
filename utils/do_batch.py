
def do_batch(
    value: "t.Iterable[V]", linecount: int, fill_with: "t.Optional[V]" = None
) -> "t.Iterator[t.List[V]]":
    """
    A filter that batches items. It works pretty much like `slice`
    just the other way round. It returns a list of lists with the
    given number of items. If you provide a second parameter this
    is used to fill up missing items. See this example:

    .. sourcecode:: html+jinja

        <table>
        {%- for row in items|batch(3, '&nbsp;') %}
          <tr>
          {%- for column in row %}
            <td>{{ column }}</td>
          {%- endfor %}
          </tr>
        {%- endfor %}
        </table>
    """
    tmp: t.List[V] = []

    for item in value:
        if len(tmp) == linecount:
            yield tmp
            tmp = []

        tmp.append(item)

    if tmp:
        if fill_with is not None and len(tmp) < linecount:
            tmp += [fill_with] * (linecount - len(tmp))

        yield tmp

