
def _parse_nh_sample(text, suffixes):
    """Determines if the line has a native histogram sample, and parses it if so."""
    labels_start = _next_unquoted_char(text, '{')
    labels_end = -1

    # Finding a native histogram sample requires careful parsing of
    # possibly-quoted text, which can appear in metric names, label names, and
    # values.
    # 
    # First, we need to determine if there are metric labels. Find the space
    # between the metric definition and the rest of the line. Look for unquoted
    # space or {.
    i = 0
    has_metric_labels = False
    i = _next_unquoted_char(text, ' {')
    if i == -1:
        return

    # If the first unquoted char was a {, then that is the metric labels (which
    # could contain a UTF-8 metric name).
    if text[i] == '{':
        has_metric_labels = True
        # Consume the labels -- jump ahead to the close bracket.
        labels_end = i = _next_unquoted_char(text, '}', i)
        if labels_end == -1:
            raise ValueError
    
    # If there is no subsequent unquoted {, then it's definitely not a nh.
    nh_value_start = _next_unquoted_char(text, '{', i + 1)
    if nh_value_start == -1:
        return
    
    # Edge case: if there is an unquoted # between the metric definition and the {,
    # then this is actually an exemplar
    exemplar = _next_unquoted_char(text, '#', i + 1)
    if exemplar != -1 and exemplar < nh_value_start:
        return
    
    nh_value_end = _next_unquoted_char(text, '}', nh_value_start)
    if nh_value_end == -1:
        raise ValueError
    
    if has_metric_labels:
        labelstext = text[labels_start + 1:labels_end]
        labels = parse_labels(labelstext, True)
        name_end = labels_start
        name = text[:name_end]
        if name.endswith(suffixes):
            raise ValueError("the sample name of a native histogram with labels should have no suffixes", name)
        if not name:
            # Name might be in the labels
            if '__name__' not in labels:
                raise ValueError
            name = labels['__name__']
            del labels['__name__']
            # Edge case: the only "label" is the name definition.
            if not labels:
                labels = None
             
        nh_value = text[nh_value_start:]
        nat_hist_value = _parse_nh_struct(nh_value)
        return Sample(name, labels, None, None, None, nat_hist_value)
    # check if it's a native histogram
    else:
        nh_value = text[nh_value_start:]
        name_end = nh_value_start - 1
        name = text[:name_end]
        if name.endswith(suffixes):
            raise ValueError("the sample name of a native histogram should have no suffixes", name)
        # Not possible for UTF-8 name here, that would have been caught as having a labelset.
        nat_hist_value = _parse_nh_struct(nh_value)
        return Sample(name, None, None, None, None, nat_hist_value)      

