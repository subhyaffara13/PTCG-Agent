from typing import Any, Optional

def pprint(
    _object: Any,
    *,
    console: Optional["Console"] = None,
    indent_guides: bool = True,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
) -> None:
    """A convenience function for pretty printing.

    Args:
        _object (Any): Object to pretty print.
        console (Console, optional): Console instance, or None to use default. Defaults to None.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of strings before truncating, or None to disable. Defaults to None.
        max_depth (int, optional): Maximum depth for nested data structures, or None for unlimited depth. Defaults to None.
        indent_guides (bool, optional): Enable indentation guides. Defaults to True.
        expand_all (bool, optional): Expand all containers. Defaults to False.
    """
    _console = get_console() if console is None else console
    _console.print(
        Pretty(
            _object,
            max_length=max_length,
            max_string=max_string,
            max_depth=max_depth,
            indent_guides=indent_guides,
            expand_all=expand_all,
            overflow="ignore",
        ),
        soft_wrap=True,
    )


def pprint(
    _object: Any,
    *,
    console: Optional["Console"] = None,
    indent_guides: bool = True,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
) -> None:
    """A convenience function for pretty printing.

    Args:
        _object (Any): Object to pretty print.
        console (Console, optional): Console instance, or None to use default. Defaults to None.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of strings before truncating, or None to disable. Defaults to None.
        max_depth (int, optional): Maximum depth for nested data structures, or None for unlimited depth. Defaults to None.
        indent_guides (bool, optional): Enable indentation guides. Defaults to True.
        expand_all (bool, optional): Expand all containers. Defaults to False.
    """
    _console = get_console() if console is None else console
    _console.print(
        Pretty(
            _object,
            max_length=max_length,
            max_string=max_string,
            max_depth=max_depth,
            indent_guides=indent_guides,
            expand_all=expand_all,
            overflow="ignore",
        ),
        soft_wrap=True,
    )


def pprint(obj: Any) -> None:
  """Pretty print `obj`."""
  print(pretty_repr(obj))


def pprint(walker):
    """Pretty printer for tree walkers

    Takes a TreeWalker instance and pretty prints the output of walking the tree.

    :arg walker: a TreeWalker instance

    """
    output = []
    indent = 0
    for token in concatenateCharacterTokens(walker):
        type = token["type"]
        if type in ("StartTag", "EmptyTag"):
            # tag name
            if token["namespace"] and token["namespace"] != constants.namespaces["html"]:
                if token["namespace"] in constants.prefixes:
                    ns = constants.prefixes[token["namespace"]]
                else:
                    ns = token["namespace"]
                name = "%s %s" % (ns, token["name"])
            else:
                name = token["name"]
            output.append("%s<%s>" % (" " * indent, name))
            indent += 2
            # attributes (sorted for consistent ordering)
            attrs = token["data"]
            for (namespace, localname), value in sorted(attrs.items()):
                if namespace:
                    if namespace in constants.prefixes:
                        ns = constants.prefixes[namespace]
                    else:
                        ns = namespace
                    name = "%s %s" % (ns, localname)
                else:
                    name = localname
                output.append("%s%s=\"%s\"" % (" " * indent, name, value))
            # self-closing
            if type == "EmptyTag":
                indent -= 2

        elif type == "EndTag":
            indent -= 2

        elif type == "Comment":
            output.append("%s<!-- %s -->" % (" " * indent, token["data"]))

        elif type == "Doctype":
            if token["name"]:
                if token["publicId"]:
                    output.append("""%s<!DOCTYPE %s "%s" "%s">""" %
                                  (" " * indent,
                                   token["name"],
                                   token["publicId"],
                                   token["systemId"] if token["systemId"] else ""))
                elif token["systemId"]:
                    output.append("""%s<!DOCTYPE %s "" "%s">""" %
                                  (" " * indent,
                                   token["name"],
                                   token["systemId"]))
                else:
                    output.append("%s<!DOCTYPE %s>" % (" " * indent,
                                                       token["name"]))
            else:
                output.append("%s<!DOCTYPE >" % (" " * indent,))

        elif type == "Characters":
            output.append("%s\"%s\"" % (" " * indent, token["data"]))

        elif type == "SpaceCharacters":
            assert False, "concatenateCharacterTokens should have got rid of all Space tokens"

        else:
            raise ValueError("Unknown token type, %s" % type)

    return "\n".join(output)

