
def sync_do_slice(
    value: "t.Collection[V]", slices: int, fill_with: "t.Optional[V]" = None
) -> "t.Iterator[t.List[V]]":
    """Slice an iterator and return a list of lists containing
    those items. Useful if you want to create a div containing
    three ul tags that represent columns:

    .. sourcecode:: html+jinja

        <div class="columnwrapper">
          {%- for column in items|slice(3) %}
            <ul class="column-{{ loop.index }}">
            {%- for item in column %}
              <li>{{ item }}</li>
            {%- endfor %}
            </ul>
          {%- endfor %}
        </div>

    If you pass it a second argument it's used to fill missing
    values on the last iteration.
    """
    seq = list(value)
    length = len(seq)
    items_per_slice = length // slices
    slices_with_extra = length % slices
    offset = 0

    for slice_number in range(slices):
        start = offset + slice_number * items_per_slice

        if slice_number < slices_with_extra:
            offset += 1

        end = offset + (slice_number + 1) * items_per_slice
        tmp = seq[start:end]

        if fill_with is not None and slice_number >= slices_with_extra:
            tmp.append(fill_with)

        yield tmp

