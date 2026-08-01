
def read_pattern(state: State, data: ReadBuffer) -> Pattern:
    tag = read_tag(data)
    if tag == nodes.AS_PATTERN:
        has_pattern = read_bool(data)
        if has_pattern:
            pattern = read_pattern(state, data)
        else:
            pattern = None
        has_name = read_bool(data)
        if has_name:
            name_str = read_str(data)
            name = NameExpr(name_str)
            read_loc(data, name)
        else:
            name = None
        as_pattern = AsPattern(pattern, name)
        read_loc(data, as_pattern)
        expect_end_tag(data)
        return as_pattern
    elif tag == nodes.OR_PATTERN:
        n = read_int(data)
        patterns = [read_pattern(state, data) for _ in range(n)]
        or_pattern = OrPattern(patterns)
        read_loc(data, or_pattern)
        expect_end_tag(data)
        return or_pattern
    elif tag == nodes.VALUE_PATTERN:
        expr = read_expression(state, data)
        value_pattern = ValuePattern(expr)
        read_loc(data, value_pattern)
        expect_end_tag(data)
        return value_pattern
    elif tag == nodes.SINGLETON_PATTERN:
        singleton_tag = read_tag(data)
        if singleton_tag == LITERAL_NONE:
            value = None
        else:
            # It's a boolean
            value = singleton_tag == 1  # TAG_LITERAL_TRUE
        singleton_pattern = SingletonPattern(value)
        read_loc(data, singleton_pattern)
        expect_end_tag(data)
        return singleton_pattern
    elif tag == nodes.SEQUENCE_PATTERN:
        n = read_int(data)
        patterns = [read_pattern(state, data) for _ in range(n)]
        sequence_pattern = SequencePattern(patterns)
        read_loc(data, sequence_pattern)
        expect_end_tag(data)
        return sequence_pattern
    elif tag == nodes.STARRED_PATTERN:
        has_name = read_bool(data)
        if has_name:
            name_str = read_str(data)
            name = NameExpr(name_str)
            read_loc(data, name)
        else:
            name = None
        starred_pattern = StarredPattern(name)
        read_loc(data, starred_pattern)
        expect_end_tag(data)
        return starred_pattern
    elif tag == nodes.MAPPING_PATTERN:
        n = read_int(data)
        keys = []
        values = []
        for _ in range(n):
            key = read_expression(state, data)
            value = read_pattern(state, data)
            keys.append(key)
            values.append(value)
        has_rest = read_bool(data)
        if has_rest:
            rest_str = read_str(data)
            rest = NameExpr(rest_str)
            read_loc(data, rest)
        else:
            rest = None
        mapping_pattern = MappingPattern(keys, values, rest)
        read_loc(data, mapping_pattern)
        expect_end_tag(data)
        return mapping_pattern
    elif tag == nodes.CLASS_PATTERN:
        class_ref = cast(RefExpr, read_expression(state, data))
        n_positional = read_int(data)
        positionals = [read_pattern(state, data) for _ in range(n_positional)]
        n_keywords = read_int(data)
        keyword_keys = []
        keyword_values = []
        for _ in range(n_keywords):
            key = read_str(data)
            value = read_pattern(state, data)
            keyword_keys.append(key)
            keyword_values.append(value)
        class_pattern = ClassPattern(class_ref, positionals, keyword_keys, keyword_values)
        read_loc(data, class_pattern)
        expect_end_tag(data)
        return class_pattern
    else:
        assert False, f"Unknown pattern tag: {tag}"

