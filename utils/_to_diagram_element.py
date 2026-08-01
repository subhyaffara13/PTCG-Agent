
def _to_diagram_element(
    element: pyparsing.ParserElement,
    parent: typing.Optional[EditablePartial],
    lookup: ConverterState = None,
    vertical: int = None,
    index: int = 0,
    name_hint: str = None,
    show_results_names: bool = False,
    show_groups: bool = False,
    show_hidden: bool = False,
) -> typing.Optional[EditablePartial]:
    """
    Recursively converts a PyParsing Element to a railroad Element
    :param lookup: The shared converter state that keeps track of useful things
    :param index: The index of this element within the parent
    :param parent: The parent of this element in the output tree
    :param vertical: Controls at what point we make a list of elements vertical. If this is an integer (the default),
    it sets the threshold of the number of items before we go vertical. If True, always go vertical, if False, never
    do so
    :param name_hint: If provided, this will override the generated name
    :param show_results_names: bool flag indicating whether to add annotations for results names
    :param show_groups: bool flag indicating whether to show groups using bounding box
    :param show_hidden: bool flag indicating whether to show elements that are typically hidden
    :returns: The converted version of the input element, but as a Partial that hasn't yet been constructed
    """
    exprs = element.recurse()
    name = name_hint or element.customName or type(element).__name__

    # Python's id() is used to provide a unique identifier for elements
    el_id = id(element)

    element_results_name = element.resultsName

    # Here we basically bypass processing certain wrapper elements if they contribute nothing to the diagram
    if not element.customName:
        if isinstance(
            element,
            (
                # pyparsing.TokenConverter,
                pyparsing.Forward,
                pyparsing.Located,
                pyparsing.AtStringStart,
                pyparsing.AtLineStart,
            ),
        ):
            # However, if this element has a useful custom name, and its child does not, we can pass it on to the child
            if exprs:
                if not exprs[0].customName:
                    propagated_name = name
                else:
                    propagated_name = None

                return _to_diagram_element(
                    element.expr,
                    parent=parent,
                    lookup=lookup,
                    vertical=vertical,
                    index=index,
                    name_hint=propagated_name,
                    show_results_names=show_results_names,
                    show_groups=show_groups,
                    show_hidden=show_hidden,
                )

    # If the element isn't worth extracting, we always treat it as the first time we say it
    if _worth_extracting(element):
        looked_up = lookup.get(el_id)
        if looked_up and looked_up.name is not None:
            # If we've seen this element exactly once before, we are only just now finding out that it's a duplicate,
            # so we have to extract it into a new diagram.
            looked_up.mark_for_extraction(el_id, lookup, name=name_hint)
            href = f"#{_make_bookmark(looked_up.name)}"
            ret = EditablePartial.from_call(railroad.NonTerminal, text=looked_up.name, href=href)
            return ret

        elif el_id in lookup.diagrams:
            # If we have seen the element at least twice before, and have already extracted it into a subdiagram, we
            # just put in a marker element that refers to the sub-diagram
            text = lookup.diagrams[el_id].kwargs["name"]
            ret = EditablePartial.from_call(
                railroad.NonTerminal, text=text, href=f"#{_make_bookmark(text)}"
            )
            return ret

    # Recursively convert child elements
    # Here we find the most relevant Railroad element for matching pyparsing Element
    # We use ``items=[]`` here to hold the place for where the child elements will go once created

    # see if this element is normally hidden, and whether hidden elements are desired
    # if not, just return None
    if not element.show_in_diagram and not show_hidden:
        return None

    if isinstance(element, pyparsing.And):
        # detect And's created with ``expr*N`` notation - for these use a OneOrMore with a repeat
        # (all will have the same name, and resultsName)
        if not exprs:
            return None
        if len(set((e.name, e.resultsName) for e in exprs)) == 1 and len(exprs) > 2:
            ret = EditablePartial.from_call(
                railroad.OneOrMore, item="", repeat=str(len(exprs))
            )
        elif _should_vertical(vertical, exprs):
            ret = EditablePartial.from_call(railroad.Stack, items=[])
        else:
            ret = EditablePartial.from_call(railroad.Sequence, items=[])
    elif isinstance(element, (pyparsing.Or, pyparsing.MatchFirst)):
        if not exprs:
            return None
        if _should_vertical(vertical, exprs):
            ret = EditablePartial.from_call(railroad.Choice, 0, items=[])
        else:
            ret = EditablePartial.from_call(railroad.HorizontalChoice, items=[])
    elif isinstance(element, pyparsing.Each):
        if not exprs:
            return None
        ret = EditablePartial.from_call(EachItem, items=[])
    elif isinstance(element, pyparsing.NotAny):
        ret = EditablePartial.from_call(AnnotatedItem, label="NOT", item="")
    elif isinstance(element, pyparsing.FollowedBy):
        ret = EditablePartial.from_call(AnnotatedItem, label="LOOKAHEAD", item="")
    elif isinstance(element, pyparsing.PrecededBy):
        ret = EditablePartial.from_call(AnnotatedItem, label="LOOKBEHIND", item="")
    elif isinstance(element, pyparsing.Group):
        if show_groups:
            ret = EditablePartial.from_call(AnnotatedItem, label="", item="")
        else:
            ret = EditablePartial.from_call(
                railroad.Group, item=None, label=element_results_name
            )
    elif isinstance(element, pyparsing.TokenConverter):
        label = type(element).__name__.lower()
        if label == "tokenconverter":
            ret = EditablePartial.from_call(railroad.Sequence, items=[])
        else:
            ret = EditablePartial.from_call(AnnotatedItem, label=label, item="")
    elif isinstance(element, pyparsing.Opt):
        ret = EditablePartial.from_call(railroad.Optional, item="")
    elif isinstance(element, pyparsing.OneOrMore):
        if element.not_ender is not None:
            args = [
                parent,
                lookup,
                vertical,
                index,
                name_hint,
                show_results_names,
                show_groups,
                show_hidden,
            ]
            return _to_diagram_element(
                (~element.not_ender.expr + element.expr)[1, ...].set_name(element.name),
                *args,
            )
        ret = EditablePartial.from_call(railroad.OneOrMore, item=None)
    elif isinstance(element, pyparsing.ZeroOrMore):
        if element.not_ender is not None:
            args = [
                parent,
                lookup,
                vertical,
                index,
                name_hint,
                show_results_names,
                show_groups,
                show_hidden,
            ]
            return _to_diagram_element(
                (~element.not_ender.expr + element.expr)[...].set_name(element.name),
                *args,
            )
        ret = EditablePartial.from_call(railroad.ZeroOrMore, item="")
    elif isinstance(element, pyparsing.Empty) and not element.customName:
        # Skip unnamed "Empty" elements
        ret = None
    elif isinstance(element, pyparsing.ParseElementEnhance):
        ret = EditablePartial.from_call(railroad.Sequence, items=[])
    elif len(exprs) > 0 and not element_results_name:
        ret = EditablePartial.from_call(railroad.Group, item="", label=name)
    elif isinstance(element, pyparsing.Regex):
        collapsed_patt = _collapse_verbose_regex(element.pattern)
        ret = EditablePartial.from_call(railroad.Terminal, collapsed_patt)
    elif len(exprs) > 0:
        ret = EditablePartial.from_call(railroad.Sequence, items=[])
    else:
        terminal = EditablePartial.from_call(railroad.Terminal, element.defaultName)
        ret = terminal

    if ret is None:
        return

    # Indicate this element's position in the tree so we can extract it if necessary
    lookup[el_id] = ElementState(
        element=element,
        converted=ret,
        parent=parent,
        parent_index=index,
        number=lookup.generate_index(),
    )
    if element.customName:
        lookup[el_id].mark_for_extraction(el_id, lookup, element.customName)

    i = 0
    for expr in exprs:
        # Add a placeholder index in case we have to extract the child before we even add it to the parent
        if "items" in ret.kwargs:
            ret.kwargs["items"].insert(i, None)

        item = _to_diagram_element(
            expr,
            parent=ret,
            lookup=lookup,
            vertical=vertical,
            index=i,
            show_results_names=show_results_names,
            show_groups=show_groups,
            show_hidden=show_hidden,
        )

        # Some elements don't need to be shown in the diagram
        if item is not None:
            if "item" in ret.kwargs:
                ret.kwargs["item"] = item
            elif "items" in ret.kwargs:
                # If we've already extracted the child, don't touch this index, since it's occupied by a nonterminal
                ret.kwargs["items"][i] = item
                i += 1
        elif "items" in ret.kwargs:
            # If we're supposed to skip this element, remove it from the parent
            del ret.kwargs["items"][i]

    # If all this items children are none, skip this item
    if ret and (
        ("items" in ret.kwargs and len(ret.kwargs["items"]) == 0)
        or ("item" in ret.kwargs and ret.kwargs["item"] is None)
    ):
        ret = EditablePartial.from_call(railroad.Terminal, name)

    # Mark this element as "complete", ie it has all of its children
    if el_id in lookup:
        lookup[el_id].complete = True

    if el_id in lookup and lookup[el_id].extract and lookup[el_id].complete:
        lookup.extract_into_diagram(el_id)
        if ret is not None:
            text = lookup.diagrams[el_id].kwargs["name"]
            href = f"#{_make_bookmark(text)}"
            ret = EditablePartial.from_call(
                railroad.NonTerminal, text=text, href=href
            )

    return ret

