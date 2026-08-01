
def _group_parentheses(recursor: TRANS):
    def _inner(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT):
        """Group tokens between parentheses with ParenthesisGroup.

        Also processes those tokens recursively.

        """
        result: list[TOKEN | ParenthesisGroup] = []
        stacks: list[ParenthesisGroup] = []
        stacklevel = 0
        for token in tokens:
            if token[0] == OP:
                if token[1] == '(':
                    stacks.append(ParenthesisGroup([]))
                    stacklevel += 1
                elif token[1] == ')':
                    stacks[-1].append(token)
                    stack = stacks.pop()

                    if len(stacks) > 0:
                        # We don't recurse here since the upper-level stack
                        # would reprocess these tokens
                        stacks[-1].extend(stack)
                    else:
                        # Recurse here to handle nested parentheses
                        # Strip off the outer parentheses to avoid an infinite loop
                        inner = stack[1:-1]
                        inner = recursor(inner,
                                         local_dict,
                                         global_dict)
                        parenGroup = [stack[0]] + inner + [stack[-1]]
                        result.append(ParenthesisGroup(parenGroup))
                    stacklevel -= 1
                    continue
            if stacklevel:
                stacks[-1].append(token)
            else:
                result.append(token)
        if stacklevel:
            raise TokenError("Mismatched parentheses")
        return result
    return _inner

