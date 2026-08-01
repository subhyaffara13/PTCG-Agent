
def _get_call_arguments(code_context):
    """
    Analyze the positional and keyword arguments in a call expression.

    This will extract the expressions of the positional and kwyword arguments, and associate them to the positions and
    the keyword argument names.
    """

    def get_argument_name(node):
        """Extract the name/expression from an AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return ast.unparse(node)
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        else:
            return ast.unparse(node)

    indent = len(code_context) - len(code_context.lstrip())
    code_context = code_context.replace(" " * indent, "")

    try:
        # Parse the line
        tree = ast.parse(code_context, mode="eval")

        assert isinstance(tree.body, ast.Call)
        call_node = tree.body

        if call_node:
            result = {
                "positional_args": [],
                "keyword_args": {},
                "starargs": None,  # *args
                "kwargs": None,  # **kwargs
            }

            # Extract positional arguments
            for arg in call_node.args:
                arg_name = get_argument_name(arg)
                result["positional_args"].append(arg_name)

            # Extract keyword arguments
            for keyword in call_node.keywords:
                if keyword.arg is None:
                    # This is **kwargs
                    result["kwargs"] = get_argument_name(keyword.value)
                else:
                    # Regular keyword argument
                    arg_name = get_argument_name(keyword.value)
                    result["keyword_args"][keyword.arg] = arg_name

            return result

    except (SyntaxError, AttributeError) as e:
        print(f"Error parsing: {e}")

    return None

