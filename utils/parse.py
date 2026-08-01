
def parse(version: str) -> "LegacyVersion":
    """
    Parse the given version string and return a :class:`LegacyVersion` object
    """
    return LegacyVersion(version)


def parse(
    code: str,
    module_name: str = "",
    path: str | None = None,
    apply_transforms: bool = True,
) -> nodes.Module:
    """Parses a source string in order to obtain an astroid AST from it.

    :param str code: The code for the module.
    :param str module_name: The name for the module, if any
    :param str path: The path for the module
    :param bool apply_transforms:
        Apply the transforms for the give code. Use it if you
        don't want the default transforms to be applied.
    """
    # pylint: disable-next=import-outside-toplevel
    from astroid.manager import AstroidManager

    code = textwrap.dedent(code)
    builder = AstroidBuilder(AstroidManager(), apply_transforms=apply_transforms)
    return builder.string_build(code, modname=module_name, path=path)


def parse(file, namespaces=True, forbid_dtd=False, forbid_entities=True, forbid_external=True):
    """Parse a document, returning the resulting Document node.

    'file' may be either a file name or an open file object.
    """
    if namespaces:
        build_builder = DefusedExpatBuilderNS
    else:
        build_builder = DefusedExpatBuilder
    builder = build_builder(
        forbid_dtd=forbid_dtd, forbid_entities=forbid_entities, forbid_external=forbid_external
    )

    if isinstance(file, str):
        fp = open(file, "rb")
        try:
            result = builder.parseFile(fp)
        finally:
            fp.close()
    else:
        result = builder.parseFile(file)
    return result


def parse(source, parser=None, base_url=None, forbid_dtd=False, forbid_entities=True):
    if parser is None:
        parser = getDefaultParser()
    elementtree = _etree.parse(source, parser, base_url=base_url)
    check_docinfo(elementtree, forbid_dtd, forbid_entities)
    return elementtree


def parse(
    file, parser=None, bufsize=None, forbid_dtd=False, forbid_entities=True, forbid_external=True
):
    """Parse a file into a DOM by filename or file object."""
    if parser is None and not bufsize:
        return _expatbuilder.parse(
            file,
            forbid_dtd=forbid_dtd,
            forbid_entities=forbid_entities,
            forbid_external=forbid_external,
        )
    else:
        return _do_pulldom_parse(
            _pulldom.parse,
            (file,),
            {
                "parser": parser,
                "bufsize": bufsize,
                "forbid_dtd": forbid_dtd,
                "forbid_entities": forbid_entities,
                "forbid_external": forbid_external,
            },
        )


def parse(
    stream_or_string,
    parser=None,
    bufsize=None,
    forbid_dtd=False,
    forbid_entities=True,
    forbid_external=True,
):
    if parser is None:
        parser = make_parser()
        parser.forbid_dtd = forbid_dtd
        parser.forbid_entities = forbid_entities
        parser.forbid_external = forbid_external
    return _parse(stream_or_string, parser, bufsize)


def parse(
    source,
    handler,
    errorHandler=_ErrorHandler(),
    forbid_dtd=False,
    forbid_entities=True,
    forbid_external=True,
):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.forbid_dtd = forbid_dtd
    parser.forbid_entities = forbid_entities
    parser.forbid_external = forbid_external
    parser.parse(source)


def parse(line: str) -> tuple[str, str]:
    """Parses import lines for comments and returns back the
    import statement and the associated comment.
    """
    comment_start = line.find("#")
    if comment_start != -1:
        return (line[:comment_start], line[comment_start + 1 :].strip())

    return (line, "")


def parse(
    source: str | bytes,
    fnam: str,
    module: str | None,
    errors: Errors,
    options: Options | None = None,
) -> MypyFile:
    """Parse a source file, without doing any semantic analysis.

    Return the parse tree. If errors is not provided, raise ParseError
    on failure. Otherwise, use the errors object to report parse errors.
    """
    ignore_errors = (options is not None and options.ignore_errors) or (
        fnam in errors.ignored_files
    )
    # If errors are ignored, we can drop many function bodies to speed up type checking.
    strip_function_bodies = ignore_errors and (options is None or not options.preserve_asts)

    if options is None:
        options = Options()
    errors.set_file(fnam, module, options=options)
    is_stub_file = fnam.endswith(".pyi")
    if is_stub_file:
        feature_version = defaults.PYTHON3_VERSION[1]
        if options.python_version[0] == 3 and options.python_version[1] > feature_version:
            feature_version = options.python_version[1]
    else:
        assert options.python_version[0] >= 3
        feature_version = options.python_version[1]
    try:
        # Disable
        # - deprecation warnings for 'invalid escape sequence' (Python 3.11 and below)
        # - syntax warnings for 'invalid escape sequence' (3.12+) and 'return in finally' (3.14+)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings("ignore", category=SyntaxWarning)
            ast = ast3_parse(source, fnam, "exec", feature_version=feature_version)

        tree = ASTConverter(
            options=options,
            is_stub=is_stub_file,
            errors=errors,
            strip_function_bodies=strip_function_bodies,
            path=fnam,
        ).visit(ast)

    except RecursionError as e:
        # For very complex expressions it is possible to hit recursion limit
        # before reaching a leaf node.
        # Should reject at top level instead at bottom, since bottom would already
        # be at the threshold of the recursion limit, and may fail again later.
        # E.G. x1+x2+x3+...+xn -> BinOp(left=BinOp(left=BinOp(left=...
        try:
            # But to prove that is the cause of this particular recursion error,
            # try to walk the tree using builtin visitor
            ast3.NodeVisitor().visit(ast)
        except RecursionError:
            errors.report(
                -1, -1, "Source expression too complex to parse", blocker=False, code=codes.MISC
            )

            tree = MypyFile([], [], False, {})

        else:
            # re-raise original recursion error if it *can* be unparsed,
            # maybe this is some other issue that shouldn't be silenced/misdirected
            raise e

    except SyntaxError as e:
        message = e.msg
        if feature_version > sys.version_info.minor and message.startswith("invalid syntax"):
            python_version_str = f"{options.python_version[0]}.{options.python_version[1]}"
            message += f"; you likely need to run mypy using Python {python_version_str} or newer"
        errors.report(
            e.lineno if e.lineno is not None else -1,
            e.offset,
            re.sub(
                r"^(\s*\w)", lambda m: m.group(1).upper(), message
            ),  # Standardizing error message
            blocker=True,
            code=codes.SYNTAX,
        )
        tree = MypyFile([], [], False, {})

    assert isinstance(tree, MypyFile)
    return tree


def parse(
    source: str | bytes | None,
    fnam: str,
    module: str | None,
    errors: Errors,
    options: Options,
    eager: bool = False,
) -> MypyFile:
    """Parse a source file, without doing any semantic analysis.

    Return the parse tree, use the errors object to report parse errors.
    The python_version (major, minor) option determines the Python syntax variant.

    New parser returns empty tree with serialized data. To get the full tree and
    the parse errors, use eager=True.

    `source` must not be `None` if the old parser is used. The new parser will read and
    parse contents from path `fnam` if `source` is `None`.
    """
    if options.native_parser:
        import mypy.nativeparse

        ignore_errors = options.ignore_errors or fnam in errors.ignored_files
        # If errors are ignored, we can drop many function bodies to speed up type checking.
        strip_function_bodies = ignore_errors and not options.preserve_asts
        tree, _, _ = mypy.nativeparse.native_parse(
            fnam, options, source, skip_function_bodies=strip_function_bodies
        )
        # Set is_stub based on file extension
        tree.is_stub = fnam.endswith(".pyi")
        # Note: tree.imports is populated directly by load_from_raw() with deserialized
        # import metadata, so we don't need to collect imports via AST traversal
        if eager and tree.raw_data is not None:
            tree = load_from_raw(fnam, module, tree.raw_data, errors, options)
        return tree

    if source is None:
        raise ValueError("Source cannot be `None` when using the old parser")
    if options.transform_source is not None:
        source = options.transform_source(source)
    import mypy.fastparse

    return mypy.fastparse.parse(source, fnam=fnam, module=module, errors=errors, options=options)


def parse(version: str) -> Version:
    """Parse the given version string.

    This is identical to the :class:`Version` constructor.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def parse(strs: _StrOrIter) -> Iterator[Requirement]: ...


def parse(strs: _StrOrIter, parser: Callable[[str], _T]) -> Iterator[_T]: ...


def parse(strs: _StrOrIter, parser: Callable[[str], _T] = parse_req) -> Iterator[_T]:  # type: ignore[assignment]
    """
    Parse requirements.
    """
    return map(parser, parse_strings(strs))


def parse(string: str | bytes) -> TOMLDocument:
    """
    Parses a string or bytes into a TOMLDocument.
    """
    return Parser(string).parse()


def parse(stream, Loader=Loader):
    """
    Parse a YAML stream and produce parsing events.
    """
    loader = Loader(stream)
    try:
        while loader.check_event():
            yield loader.get_event()
    finally:
        loader.dispose()


def parse(version: str) -> "Version":
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def parse(graph):
    nodes = []
    import itertools

    nodes_proto = list(itertools.chain(graph.input, graph.output))

    for node in nodes_proto:
        print(node.name)
        shapeproto = TensorShapeProto(
            dim=[
                TensorShapeProto.Dim(size=d.dim_value)
                for d in node.type.tensor_type.shape.dim
            ]
        )
        nodes.append(
            NodeDef(
                name=node.name.encode(encoding="utf_8"),
                op="Variable",
                input=[],
                attr={
                    "dtype": AttrValue(type=node.type.tensor_type.elem_type),
                    "shape": AttrValue(shape=shapeproto),
                },
            )
        )

    for node in graph.node:
        _attr = [" = ".join([str(f[1]) for f in s.ListFields()]) for s in node.attribute]
        attr = ", ".join(_attr).encode(encoding="utf_8")
        print(node.output[0])
        nodes.append(
            NodeDef(
                name=node.output[0].encode(encoding="utf_8"),
                op=node.op_type,
                input=node.input,
                attr={"parameters": AttrValue(s=attr)},
            )
        )

    # two pass token replacement, appends opname to object id
    mapping = {}
    for node in nodes:
        mapping[node.name] = node.op + "_" + node.name

    return GraphDef(node=nodes, versions=VersionDef(producer=22))


def parse(graph, trace, args=None, omit_useless_nodes=True):
    """Parse an optimized PyTorch model graph and produces a list of nodes and node stats.

    Useful for eventual conversion to TensorBoard protobuf format.

    Args:
      graph (PyTorch module): The model graph to be parsed.
      trace (PyTorch JIT TracedModule): The model trace to be parsed.
      args (tuple): input tensor[s] for the model.
      omit_useless_nodes (boolean): Whether to remove nodes from the graph.
    """
    nodes_py = GraphPy()
    for node in graph.inputs():
        if omit_useless_nodes:
            if (
                len(node.uses()) == 0
            ):  # number of user of the node (= number of outputs/ fanout)
                continue

        if node.type().kind() != CLASSTYPE_KIND:
            nodes_py.append(NodePyIO(node, "input"))

    attr_to_scope: dict[Any, str] = {}
    for node in graph.nodes():
        if node.kind() == GETATTR_KIND:
            attr_name = node.s("name")
            attr_key = node.output().debugName()
            parent = node.input().node()
            if (
                parent.kind() == GETATTR_KIND
            ):  # If the parent node is not the top-level "self" node
                parent_attr_key = parent.output().debugName()
                parent_scope = attr_to_scope[parent_attr_key]
                attr_scope = parent_scope.split("/")[-1]
                attr_to_scope[attr_key] = f"{parent_scope}/{attr_scope}.{attr_name}"
            else:
                attr_to_scope[attr_key] = f"__module.{attr_name}"
            # We don't need classtype nodes; scope will provide this information
            if node.output().type().kind() != CLASSTYPE_KIND:
                node_py = NodePyOP(node)
                node_py.scopeName = attr_to_scope[attr_key]  # type: ignore[attr-defined]
                nodes_py.append(node_py)
        else:
            nodes_py.append(NodePyOP(node))

    for i, node in enumerate(graph.outputs()):  # Create sink nodes for output ops
        node_pyio = NodePyIO(node, "output")
        node_pyio.debugName = f"output.{i + 1}"
        node_pyio.inputs = [node.debugName()]
        nodes_py.append(node_pyio)

    def parse_traced_name(module):
        if isinstance(module, torch.jit.TracedModule):
            module_name = module._name
        else:
            module_name = getattr(module, "original_name", "Module")
        return module_name

    alias_to_name = {}
    base_name = parse_traced_name(trace)
    for name, module in trace.named_modules(prefix="__module"):
        mod_name = parse_traced_name(module)
        attr_name = name.split(".")[-1]
        alias_to_name[name] = f"{mod_name}[{attr_name}]"

    for node in nodes_py.nodes_op:
        module_aliases = node.scopeName.split("/")
        replacements = [
            alias_to_name[alias] if alias in alias_to_name else alias.split(".")[-1]
            for alias in module_aliases
        ]
        node.scopeName = base_name
        if any(replacements):
            node.scopeName += "/" + "/".join(replacements)

    nodes_py.populate_namespace_from_OP_to_IO()
    return nodes_py.to_proto()


def parse(version: str) -> Version:
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def parse(version: str) -> Version:
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def parse(version: str) -> Union["LegacyVersion", "Version"]:
    """
    Parse the given version string and return either a :class:`Version` object
    or a :class:`LegacyVersion` object depending on if the given version is
    a valid PEP 440 version or a legacy version.
    """
    try:
        return Version(version)
    except InvalidVersion:
        return LegacyVersion(version)


def parse(version: str) -> Version:
    """Parse the given version string.

    This is identical to the :class:`Version` constructor.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def parse(version: str) -> Version:
    return Version(version)


def parse(version):
    """
    Parse the given version string and return either a :class:`Version` object
    or a :class:`LegacyVersion` object depending on if the given version is
    a valid PEP 440 version or a legacy version.
    """
    try:
        return Version(version)
    except InvalidVersion:
        return LegacyVersion(version)


def parse(string: str) -> tuple[int, dict[str, str]]:
    """Parse attributes from start of string.

    :returns: (length of parsed string, dict of attributes)
    """
    pos = 0
    state: State = State.START
    tokens = TokenState()
    while pos < len(string):
        state = HANDLERS[state](string[pos], pos, tokens)
        if state == State.DONE:
            return pos, tokens.compile(string)
        pos = pos + 1

    return pos, tokens.compile(string)


def parse(string):
    time_formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ"]
    for t in time_formats:
        try:
            result = datetime.strptime(string[:26], t).replace(microsecond=0)
            return result
        except:
            pass
    return string


def Parse(
    text,
    message,
    ignore_unknown_fields=False,
    descriptor_pool=None,
    max_recursion_depth=100,
):
  """Parses a JSON representation of a protocol message into a message.

  Args:
    text: Message JSON representation.
    message: A protocol buffer message to merge into.
    ignore_unknown_fields: If True, do not raise errors for unknown fields.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.
    max_recursion_depth: max recursion depth of JSON message to be deserialized.
      JSON messages over this depth will fail to be deserialized. Default value
      is 100.

  Returns:
    The same message passed as argument.

  Raises::
    ParseError: On JSON parsing problems.
  """
  if not isinstance(text, str):
    text = text.decode('utf-8')

  try:
    js = json.loads(text, object_pairs_hook=_DuplicateChecker)
  except Exception as e:
    raise ParseError('Failed to load JSON: {0}.'.format(str(e))) from e

  try:
    return ParseDict(
        js, message, ignore_unknown_fields, descriptor_pool, max_recursion_depth
    )
  except ParseError as e:
    raise e
  except Exception as e:
    raise ParseError(
        'Failed to parse JSON: {0}: {1}.'.format(type(e).__name__, str(e))
    ) from e


def parse(message_class: Type[_MESSAGE], payload: bytes) -> _MESSAGE:
  """Given a serialized data in binary form, deserialize it into a Message.

  Args:
    message_class: The message meta class.
    payload: A serialized bytes in binary form.

  Returns:
    A new message deserialized from payload.
  """
  new_message = message_class()
  new_message.ParseFromString(payload)
  return new_message


def parse(
    message_class: Type[Message],
    js_dict: dict,
    ignore_unknown_fields: bool=False,
    descriptor_pool: Optional[DescriptorPool]=None,
    max_recursion_depth: int=100
) -> Message:
  """Parses a JSON dictionary representation into a message.

  Args:
    message_class: The message meta class.
    js_dict: Dict representation of a JSON message.
    ignore_unknown_fields: If True, do not raise errors for unknown fields.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.
    max_recursion_depth: max recursion depth of JSON message to be deserialized.
      JSON messages over this depth will fail to be deserialized. Default value
      is 100.

  Returns:
    A new message passed from json_dict.
  """
  new_message = message_class()
  json_format.ParseDict(
      js_dict=js_dict,
      message=new_message,
      ignore_unknown_fields=ignore_unknown_fields,
      descriptor_pool=descriptor_pool,
      max_recursion_depth=max_recursion_depth,
  )
  return new_message


def parse(
    message_class: Type[Message],
    text: AnyStr,
    allow_unknown_extension: bool = False,
    allow_field_number: bool = False,
    descriptor_pool: Optional[DescriptorPool] = None,
    allow_unknown_field: bool = False,
) -> Message:
  """Parses a text representation of a protocol message into a message.

  Args:
    message_class: The message meta class.
    text (str): Message text representation.
    message (Message): A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
    allow_unknown_field: if True, skip over unknown field and keep parsing.
      Avoid to use this option if possible. It may hide some errors (e.g.
      spelling error on field name)

  Returns:
    Message: A new message passed from text.

  Raises:
    ParseError: On text parsing problems.
  """
  new_message = message_class()
  text_format.Parse(
      text=text,
      message=new_message,
      allow_unknown_extension=allow_unknown_extension,
      allow_field_number=allow_field_number,
      descriptor_pool=descriptor_pool,
      allow_unknown_field=allow_unknown_field,
  )
  return new_message


def Parse(text,
          message,
          allow_unknown_extension=False,
          allow_field_number=False,
          descriptor_pool=None,
          allow_unknown_field=False,
          max_recursion_depth=None):
  """Parses a text representation of a protocol message into a message.

  NOTE: for historical reasons this function does not clear the input
  message. This is different from what the binary msg.ParseFrom(...) does.
  If text contains a field already set in message, the value is appended if the
  field is repeated. Otherwise, an error is raised.

  Example::

    a = MyProto()
    a.repeated_field.append('test')
    b = MyProto()

    # Repeated fields are combined
    text_format.Parse(repr(a), b)
    text_format.Parse(repr(a), b) # repeated_field contains ["test", "test"]

    # Non-repeated fields cannot be overwritten
    a.singular_field = 1
    b.singular_field = 2
    text_format.Parse(repr(a), b) # ParseError

    # Binary version:
    b.ParseFromString(a.SerializeToString()) # repeated_field is now "test"

  Caller is responsible for clearing the message as needed.

  Args:
    text (str): Message text representation.
    message (Message): A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
    allow_unknown_field: if True, skip over unknown field and keep
      parsing. Avoid to use this option if possible. It may hide some
      errors (e.g. spelling error on field name)
    max_recursion_depth: Optional maximum recursion depth of a text proto
      message to be deserialized. Text proto messages over this depth will
      fail to parse. ``None`` keeps the historical unbounded behavior.

  Returns:
    Message: The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
  return ParseLines(text.split(b'\n' if isinstance(text, bytes) else u'\n'),
                    message,
                    allow_unknown_extension,
                    allow_field_number,
                    descriptor_pool=descriptor_pool,
                    allow_unknown_field=allow_unknown_field,
                    max_recursion_depth=max_recursion_depth)


def parse(timestr, parserinfo=None, **kwargs):
    """

    Parse a string in one of the supported formats, using the
    ``parserinfo`` parameters.

    :param timestr:
        A string containing a date/time stamp.

    :param parserinfo:
        A :class:`parserinfo` object containing parameters for the parser.
        If ``None``, the default arguments to the :class:`parserinfo`
        constructor are used.

    The ``**kwargs`` parameter takes the following keyword arguments:

    :param default:
        The default datetime object, if this is a datetime object and not
        ``None``, elements specified in ``timestr`` replace elements in the
        default object.

    :param ignoretz:
        If set ``True``, time zones in parsed strings are ignored and a naive
        :class:`datetime` object is returned.

    :param tzinfos:
        Additional time zone names / aliases which may be present in the
        string. This argument maps time zone names (and optionally offsets
        from those time zones) to time zones. This parameter can be a
        dictionary with timezone aliases mapping time zone names to time
        zones or a function taking two parameters (``tzname`` and
        ``tzoffset``) and returning a time zone.

        The timezones to which the names are mapped can be an integer
        offset from UTC in seconds or a :class:`tzinfo` object.

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> from dateutil.parser import parse
            >>> from dateutil.tz import gettz
            >>> tzinfos = {"BRST": -7200, "CST": gettz("America/Chicago")}
            >>> parse("2012-01-19 17:21:00 BRST", tzinfos=tzinfos)
            datetime.datetime(2012, 1, 19, 17, 21, tzinfo=tzoffset(u'BRST', -7200))
            >>> parse("2012-01-19 17:21:00 CST", tzinfos=tzinfos)
            datetime.datetime(2012, 1, 19, 17, 21,
                              tzinfo=tzfile('/usr/share/zoneinfo/America/Chicago'))

        This parameter is ignored if ``ignoretz`` is set.

    :param dayfirst:
        Whether to interpret the first value in an ambiguous 3-integer date
        (e.g. 01/05/09) as the day (``True``) or month (``False``). If
        ``yearfirst`` is set to ``True``, this distinguishes between YDM and
        YMD. If set to ``None``, this value is retrieved from the current
        :class:`parserinfo` object (which itself defaults to ``False``).

    :param yearfirst:
        Whether to interpret the first value in an ambiguous 3-integer date
        (e.g. 01/05/09) as the year. If ``True``, the first number is taken to
        be the year, otherwise the last number is taken to be the year. If
        this is set to ``None``, the value is retrieved from the current
        :class:`parserinfo` object (which itself defaults to ``False``).

    :param fuzzy:
        Whether to allow fuzzy parsing, allowing for string like "Today is
        January 1, 2047 at 8:21:00AM".

    :param fuzzy_with_tokens:
        If ``True``, ``fuzzy`` is automatically set to True, and the parser
        will return a tuple where the first element is the parsed
        :class:`datetime.datetime` datetimestamp and the second element is
        a tuple containing the portions of the string which were ignored:

        .. doctest::

            >>> from dateutil.parser import parse
            >>> parse("Today is January 1, 2047 at 8:21:00AM", fuzzy_with_tokens=True)
            (datetime.datetime(2047, 1, 1, 8, 21), (u'Today is ', u' ', u'at '))

    :return:
        Returns a :class:`datetime.datetime` object or, if the
        ``fuzzy_with_tokens`` option is ``True``, returns a tuple, the
        first element being a :class:`datetime.datetime` object, the second
        a tuple containing the fuzzy tokens.

    :raises ParserError:
        Raised for invalid or unknown string formats, if the provided
        :class:`tzinfo` is not in a valid format, or if an invalid date would
        be created.

    :raises OverflowError:
        Raised if the parsed date exceeds the largest valid C integer on
        your system.
    """
    if parserinfo:
        return parser(parserinfo).parse(timestr, **kwargs)
    else:
        return DEFAULTPARSER.parse(timestr, **kwargs)


def parse(doc, treebuilder="etree", namespaceHTMLElements=True, **kwargs):
    """Parse an HTML document as a string or file-like object into a tree

    :arg doc: the document to parse as a string or file-like object

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5parser import parse
    >>> parse('<html><body><p>This is a doc</p></body></html>')
    <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

    """
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return p.parse(doc, **kwargs)

