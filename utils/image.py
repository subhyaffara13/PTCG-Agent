
def image(tag, tensor, rescale=1, dataformats="NCHW"):
    """Output a `Summary` protocol buffer with images.

    The summary has up to `max_images` summary values containing images. The
    images are built from `tensor` which must be 3-D with shape `[height, width,
    channels]` and where `channels` can be:
    *  1: `tensor` is interpreted as Grayscale.
    *  3: `tensor` is interpreted as RGB.
    *  4: `tensor` is interpreted as RGBA.
    The `name` in the outputted Summary.Value protobufs is generated based on the
    name, with a suffix depending on the max_outputs setting:
    *  If `max_outputs` is 1, the summary value tag is '*name*/image'.
    *  If `max_outputs` is greater than 1, the summary value tags are
       generated sequentially as '*name*/image/0', '*name*/image/1', etc.
    Args:
      tag: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      tensor: A 3-D `uint8` or `float32` `Tensor` of shape `[height, width,
        channels]` where `channels` is 1, 3, or 4.
        'tensor' can either have values in [0, 1] (float32) or [0, 255] (uint8).
        The image() function will scale the image values to [0, 255] by applying
        a scale factor of either 1 (uint8) or 255 (float32). Out-of-range values
        will be clipped.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    tensor = make_np(tensor)
    tensor = convert_to_HWC(tensor, dataformats)
    # Do not assume that user passes in values in [0, 255], use data type to detect
    scale_factor = _calc_scale_factor(tensor)
    tensor = tensor.astype(np.float32)
    tensor = (tensor * scale_factor).clip(0, 255).astype(np.uint8)
    image = make_image(tensor, rescale=rescale)
    return Summary(value=[Summary.Value(tag=tag, image=image)])


def image(state: StateInline, silent: bool) -> bool:
    label = None
    href = ""
    oldPos = state.pos
    max = state.posMax

    if state.src[state.pos] != "!":
        return False

    if state.pos + 1 < state.posMax and state.src[state.pos + 1] != "[":
        return False

    labelStart = state.pos + 2
    labelEnd = state.md.helpers.parseLinkLabel(state, state.pos + 1, False)

    # parser failed to find ']', so it's not a valid link
    if labelEnd < 0:
        return False

    pos = labelEnd + 1

    if pos < max and state.src[pos] == "(":
        #
        # Inline link
        #

        # [link](  <href>  "title"  )
        #        ^^ skipping these spaces
        pos += 1
        while pos < max:
            ch = state.src[pos]
            if not isStrSpace(ch) and ch != "\n":
                break
            pos += 1

        if pos >= max:
            return False

        # [link](  <href>  "title"  )
        #          ^^^^^^ parsing link destination
        start = pos
        res = state.md.helpers.parseLinkDestination(state.src, pos, state.posMax)
        if res.ok:
            href = state.md.normalizeLink(res.str)
            if state.md.validateLink(href):
                pos = res.pos
            else:
                href = ""

        # [link](  <href>  "title"  )
        #                ^^ skipping these spaces
        start = pos
        while pos < max:
            ch = state.src[pos]
            if not isStrSpace(ch) and ch != "\n":
                break
            pos += 1

        # [link](  <href>  "title"  )
        #                  ^^^^^^^ parsing link title
        res = state.md.helpers.parseLinkTitle(state.src, pos, state.posMax, None)
        if pos < max and start != pos and res.ok:
            title = res.str
            pos = res.pos

            # [link](  <href>  "title"  )
            #                         ^^ skipping these spaces
            while pos < max:
                ch = state.src[pos]
                if not isStrSpace(ch) and ch != "\n":
                    break
                pos += 1
        else:
            title = ""

        if pos >= max or state.src[pos] != ")":
            state.pos = oldPos
            return False

        pos += 1

    else:
        #
        # Link reference
        #
        if "references" not in state.env:
            return False

        # /* [ */
        if pos < max and state.src[pos] == "[":
            start = pos + 1
            pos = state.md.helpers.parseLinkLabel(state, pos)
            if pos >= 0:
                label = state.src[start:pos]
                pos += 1
            else:
                pos = labelEnd + 1
        else:
            pos = labelEnd + 1

        # covers label == '' and label == undefined
        # (collapsed reference link and shortcut reference link respectively)
        if not label:
            label = state.src[labelStart:labelEnd]

        label = normalizeReference(label)

        ref = state.env["references"].get(label, None)
        if not ref:
            state.pos = oldPos
            return False

        href = ref["href"]
        title = ref["title"]

    #
    # We found the end of the link, and know for a fact it's a valid link
    # so all that's left to do is to call tokenizer.
    #
    if not silent:
        content = state.src[labelStart:labelEnd]

        tokens: list[Token] = []
        state.md.inline.parse(content, state.md, state.env, tokens)

        token = state.push("image", "img", 0)
        token.attrs = {"src": href, "alt": ""}
        token.children = tokens or None
        token.content = content

        if title:
            token.attrSet("title", title)

        # note, this is not part of markdown-it JS, but is useful for renderers
        if label and state.md.options.get("store_labels", False):
            token.meta["label"] = label

    state.pos = pos
    state.posMax = max
    return True

