
def link(obj_files, out_file=None, shared=False, Runner=None,
         cwd=None, cplus=False, fort=False, extra_objs=None, **kwargs):
    """ Link object files.

    Parameters
    ==========

    obj_files: iterable of str
        Paths to object files.
    out_file: str (optional)
        Path to executable/shared library, if ``None`` it will be
        deduced from the last item in obj_files.
    shared: bool
        Generate a shared library?
    Runner: CompilerRunner subclass (optional)
        If not given the ``cplus`` and ``fort`` flags will be inspected
        (fallback is the C compiler).
    cwd: str
        Path to the root of relative paths and working directory for compiler.
    cplus: bool
        C++ objects? default: ``False``.
    fort: bool
        Fortran objects? default: ``False``.
    extra_objs: list
        List of paths to extra object files / static libraries.
    \\*\\*kwargs: dict
        Keyword arguments passed to ``Runner``.

    Returns
    =======

    The absolute path to the generated shared object / executable.

    """
    if out_file is None:
        out_file, ext = os.path.splitext(os.path.basename(obj_files[-1]))
        if shared:
            out_file += get_config_var('EXT_SUFFIX')

    if not Runner:
        if fort:
            Runner, extra_kwargs, vendor = \
                get_mixed_fort_c_linker(
                    vendor=kwargs.get('vendor', None),
                    cplus=cplus,
                    cwd=cwd,
                )
            for k, v in extra_kwargs.items():
                if k in kwargs:
                    kwargs[k].expand(v)
                else:
                    kwargs[k] = v
        else:
            if cplus:
                Runner = CppCompilerRunner
            else:
                Runner = CCompilerRunner

    flags = kwargs.pop('flags', [])
    if shared:
        if '-shared' not in flags:
            flags.append('-shared')
    run_linker = kwargs.pop('run_linker', True)
    if not run_linker:
        raise ValueError("run_linker was set to False (nonsensical).")

    out_file = get_abspath(out_file, cwd=cwd)
    runner = Runner(obj_files+(extra_objs or []), out_file, flags, cwd=cwd, **kwargs)
    runner.run()
    return out_file


def link(state: StateInline, silent: bool) -> bool:
    href = ""
    title = ""
    label = None
    oldPos = state.pos
    maximum = state.posMax
    start = state.pos
    parseReference = True

    if state.src[state.pos] != "[":
        return False

    labelStart = state.pos + 1
    labelEnd = state.md.helpers.parseLinkLabel(state, state.pos, True)

    # parser failed to find ']', so it's not a valid link
    if labelEnd < 0:
        return False

    pos = labelEnd + 1

    if pos < maximum and state.src[pos] == "(":
        #
        # Inline link
        #

        # might have found a valid shortcut link, disable reference parsing
        parseReference = False

        # [link](  <href>  "title"  )
        #        ^^ skipping these spaces
        pos += 1
        while pos < maximum:
            ch = state.src[pos]
            if not isStrSpace(ch) and ch != "\n":
                break
            pos += 1

        if pos >= maximum:
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
            while pos < maximum:
                ch = state.src[pos]
                if not isStrSpace(ch) and ch != "\n":
                    break
                pos += 1

            # [link](  <href>  "title"  )
            #                  ^^^^^^^ parsing link title
            res = state.md.helpers.parseLinkTitle(state.src, pos, state.posMax)
            if pos < maximum and start != pos and res.ok:
                title = res.str
                pos = res.pos

                # [link](  <href>  "title"  )
                #                         ^^ skipping these spaces
                while pos < maximum:
                    ch = state.src[pos]
                    if not isStrSpace(ch) and ch != "\n":
                        break
                    pos += 1

        if pos >= maximum or state.src[pos] != ")":
            # parsing a valid shortcut link failed, fallback to reference
            parseReference = True

        pos += 1

    if parseReference:
        #
        # Link reference
        #
        if "references" not in state.env:
            return False

        if pos < maximum and state.src[pos] == "[":
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
        state.pos = labelStart
        state.posMax = labelEnd

        token = state.push("link_open", "a", 1)
        token.attrs = {"href": href}

        if title:
            token.attrSet("title", title)

        # note, this is not part of markdown-it JS, but is useful for renderers
        if label and state.md.options.get("store_labels", False):
            token.meta["label"] = label

        state.linkLevel += 1
        state.md.inline.tokenize(state)
        state.linkLevel -= 1

        token = state.push("link_close", "a", -1)

    state.pos = pos
    state.posMax = maximum
    return True

