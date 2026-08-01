
def _make_iterencode(markers, _default, _encoder, _indent, _floatstr,
        _key_separator, _item_separator, _sort_keys, _skipkeys,
        _use_decimal, _namedtuple_as_object, _tuple_as_array,
        _int_as_string_bitcount, _item_sort_key,
        _encoding,_for_json,
        _iterable_as_array,
        ## HACK: hand-optimized bytecode; turn globals into locals
        _PY3=PY3,
        ValueError=ValueError,
        string_types=string_types,
        Decimal=None,
        dict=dict,
        _dict_types=_dict_types,
        float=float,
        id=id,
        integer_types=integer_types,
        isinstance=isinstance,
        list=list,
        str=str,
        tuple=tuple,
        iter=iter,
    ):
    if _use_decimal and Decimal is None:
        Decimal = decimal.Decimal
    if _item_sort_key and not callable(_item_sort_key):
        raise TypeError("item_sort_key must be None or callable")
    elif _sort_keys and not _item_sort_key:
        _item_sort_key = itemgetter(0)

    if (_int_as_string_bitcount is not None and
        (_int_as_string_bitcount <= 0 or
         not isinstance(_int_as_string_bitcount, integer_types))):
        raise TypeError("int_as_string_bitcount must be a positive integer")

    def call_method(obj, method_name):
        method = getattr(obj, method_name, None)
        if callable(method):
            try:
                return (method(),)
            except TypeError:
                pass
        return None

    def _encode_int(value):
        skip_quoting = (
            _int_as_string_bitcount is None
            or
            _int_as_string_bitcount < 1
        )
        if type(value) not in integer_types:
            # See #118, do not trust custom str/repr
            value = int(value)
        if (
            skip_quoting or
            (-1 << _int_as_string_bitcount)
            < value <
            (1 << _int_as_string_bitcount)
        ):
            return str(value)
        return '"' + str(value) + '"'

    def _iterencode_list(lst, _current_indent_level):
        if not lst:
            yield '[]'
            return
        if markers is not None:
            markerid = id(lst)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = lst
        buf = '['
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + (_indent * _current_indent_level)
            separator = _item_separator + newline_indent
            buf += newline_indent
        else:
            newline_indent = None
            separator = _item_separator
        first = True
        for i, value in enumerate(lst):
            if first:
                first = False
            else:
                buf = separator
            try:
                if isinstance(value, string_types):
                    yield buf + _encoder(value)
                elif _PY3 and isinstance(value, bytes) and _encoding is not None:
                    yield buf + _encoder(value)
                elif isinstance(value, RawJSON):
                    yield buf + value.encoded_json
                elif value is None:
                    yield buf + 'null'
                elif value is True:
                    yield buf + 'true'
                elif value is False:
                    yield buf + 'false'
                elif isinstance(value, integer_types):
                    yield buf + _encode_int(value)
                elif isinstance(value, float):
                    yield buf + _floatstr(value)
                elif _use_decimal and isinstance(value, Decimal):
                    yield buf + str(value)
                else:
                    yield buf
                    for_json = _for_json and call_method(value, 'for_json')
                    if for_json:
                        chunks = _iterencode(for_json[0], _current_indent_level)
                    else:
                        _asdict = _namedtuple_as_object and call_method(value, '_asdict')
                        if _asdict:
                            dct = _asdict[0]
                            if not isinstance(dct, dict):
                                raise TypeError("_asdict() must return a dict, not %s" % (type(dct).__name__,))
                            chunks = _iterencode_dict(dct,
                                                      _current_indent_level)
                        elif isinstance(value, list):
                            chunks = _iterencode_list(value, _current_indent_level)
                        elif _tuple_as_array and isinstance(value, tuple):
                            chunks = _iterencode_list(value, _current_indent_level)
                        elif isinstance(value, _dict_types):
                            chunks = _iterencode_dict(value, _current_indent_level)
                        else:
                            chunks = _iterencode(value, _current_indent_level)
                    for chunk in chunks:
                        yield chunk
            except BaseException as exc:
                if _HAS_ADD_NOTE:
                    exc.add_note(
                        'when serializing %s item %d'
                        % (type(lst).__name__, i))
                raise
        if first:
            # iterable_as_array misses the fast path at the top
            yield '[]'
        else:
            if newline_indent is not None:
                _current_indent_level -= 1
                yield '\n' + (_indent * _current_indent_level)
            yield ']'
        if markers is not None:
            del markers[markerid]

    def _stringify_key(key):
        if isinstance(key, string_types): # pragma: no cover
            pass
        elif _PY3 and isinstance(key, bytes) and _encoding is not None:
            key = str(key, _encoding)
        elif isinstance(key, float):
            key = _floatstr(key)
        elif key is True:
            key = 'true'
        elif key is False:
            key = 'false'
        elif key is None:
            key = 'null'
        elif isinstance(key, integer_types):
            if type(key) not in integer_types:
                # See #118, do not trust custom str/repr
                key = int(key)
            key = str(key)
        elif _use_decimal and isinstance(key, Decimal):
            key = str(key)
        elif _skipkeys:
            key = None
        else:
            raise TypeError('keys must be str, int, float, bool or None, '
                            'not %s' % key.__class__.__name__)
        return key

    def _iterencode_dict(dct, _current_indent_level):
        if not dct:
            yield '{}'
            return
        if markers is not None:
            markerid = id(dct)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = dct
        yield '{'
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + (_indent * _current_indent_level)
            item_separator = _item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = _item_separator
        first = True
        if _PY3:
            iteritems = dct.items()
        else:
            iteritems = dct.iteritems()
        if _item_sort_key:
            items = []
            for k, v in dct.items():
                if not isinstance(k, string_types):
                    k = _stringify_key(k)
                    if k is None:
                        continue
                items.append((k, v))
            items.sort(key=_item_sort_key)
        else:
            items = iteritems
        for key, value in items:
            if not (_item_sort_key or isinstance(key, string_types)):
                key = _stringify_key(key)
                if key is None:
                    # _skipkeys must be True
                    continue
            if first:
                first = False
            else:
                yield item_separator
            yield _encoder(key)
            yield _key_separator
            try:
                if isinstance(value, string_types):
                    yield _encoder(value)
                elif _PY3 and isinstance(value, bytes) and _encoding is not None:
                    yield _encoder(value)
                elif isinstance(value, RawJSON):
                    yield value.encoded_json
                elif value is None:
                    yield 'null'
                elif value is True:
                    yield 'true'
                elif value is False:
                    yield 'false'
                elif isinstance(value, integer_types):
                    yield _encode_int(value)
                elif isinstance(value, float):
                    yield _floatstr(value)
                elif _use_decimal and isinstance(value, Decimal):
                    yield str(value)
                else:
                    for_json = _for_json and call_method(value, 'for_json')
                    if for_json:
                        chunks = _iterencode(for_json[0], _current_indent_level)
                    else:
                        _asdict = _namedtuple_as_object and call_method(value, '_asdict')
                        if _asdict:
                            dct = _asdict[0]
                            if not isinstance(dct, dict):
                                raise TypeError("_asdict() must return a dict, not %s" % (type(dct).__name__,))
                            chunks = _iterencode_dict(dct,
                                                      _current_indent_level)
                        elif isinstance(value, list):
                            chunks = _iterencode_list(value, _current_indent_level)
                        elif _tuple_as_array and isinstance(value, tuple):
                            chunks = _iterencode_list(value, _current_indent_level)
                        elif isinstance(value, _dict_types):
                            chunks = _iterencode_dict(value, _current_indent_level)
                        else:
                            chunks = _iterencode(value, _current_indent_level)
                    for chunk in chunks:
                        yield chunk
            except BaseException as exc:
                if _HAS_ADD_NOTE:
                    exc.add_note(
                        'when serializing %s item %r'
                        % (type(dct).__name__, key))
                raise
        if newline_indent is not None:
            _current_indent_level -= 1
            yield '\n' + (_indent * _current_indent_level)
        yield '}'
        if markers is not None:
            del markers[markerid]

    def _iterencode(o, _current_indent_level):
        if isinstance(o, string_types):
            yield _encoder(o)
        elif _PY3 and isinstance(o, bytes) and _encoding is not None:
            yield _encoder(o)
        elif isinstance(o, RawJSON):
            yield o.encoded_json
        elif o is None:
            yield 'null'
        elif o is True:
            yield 'true'
        elif o is False:
            yield 'false'
        elif isinstance(o, integer_types):
            yield _encode_int(o)
        elif isinstance(o, float):
            yield _floatstr(o)
        else:
            for_json = _for_json and call_method(o, 'for_json')
            if for_json:
                for chunk in _iterencode(for_json[0], _current_indent_level):
                    yield chunk
            else:
                _asdict = _namedtuple_as_object and call_method(o, '_asdict')
                if _asdict:
                    dct = _asdict[0]
                    if not isinstance(dct, dict):
                        raise TypeError("_asdict() must return a dict, not %s" % (type(dct).__name__,))
                    for chunk in _iterencode_dict(dct, _current_indent_level):
                        yield chunk
                elif isinstance(o, list):
                    for chunk in _iterencode_list(o, _current_indent_level):
                        yield chunk
                elif (_tuple_as_array and isinstance(o, tuple)):
                    for chunk in _iterencode_list(o, _current_indent_level):
                        yield chunk
                elif isinstance(o, _dict_types):
                    for chunk in _iterencode_dict(o, _current_indent_level):
                        yield chunk
                elif _use_decimal and isinstance(o, Decimal):
                    yield str(o)
                else:
                    while _iterable_as_array:
                        # Markers are not checked here because it is valid for
                        # an iterable to return self.
                        try:
                            o = iter(o)
                        except TypeError:
                            break
                        for chunk in _iterencode_list(o, _current_indent_level):
                            yield chunk
                        return
                    if markers is not None:
                        markerid = id(o)
                        if markerid in markers:
                            raise ValueError("Circular reference detected")
                        markers[markerid] = o
                    try:
                        o = _default(o)
                        for chunk in _iterencode(o, _current_indent_level):
                            yield chunk
                    except BaseException as exc:
                        if _HAS_ADD_NOTE:
                            exc.add_note(
                                'when serializing %s object'
                                % type(o).__name__)
                        raise
                    if markers is not None:
                        del markers[markerid]

    return _iterencode

