
def _construct_algebraic(coeffs, opt):
    """We know that coefficients are algebraic so construct the extension. """
    from sympy.polys.numberfields import primitive_element

    exts = set()

    def build_trees(args):
        trees = []
        for a in args:
            if a.is_Rational:
                tree = ('Q', QQ.from_sympy(a))
            elif a.is_Add:
                tree = ('+', build_trees(a.args))
            elif a.is_Mul:
                tree = ('*', build_trees(a.args))
            else:
                tree = ('e', a)
                exts.add(a)
            trees.append(tree)
        return trees

    trees = build_trees(coeffs)
    exts = list(ordered(exts))

    g, span, H = primitive_element(exts, ex=True, polys=True)
    root = sum(s*ext for s, ext in zip(span, exts))

    domain, g = QQ.algebraic_field((g, root)), g.rep.to_list()

    exts_dom = [domain.dtype.from_list(h, g, QQ) for h in H]
    exts_map = dict(zip(exts, exts_dom))

    def convert_tree(tree):
        op, args = tree
        if op == 'Q':
            return domain.dtype.from_list([args], g, QQ)
        elif op == '+':
            return sum((convert_tree(a) for a in args), domain.zero)
        elif op == '*':
            return prod(convert_tree(a) for a in args)
        elif op == 'e':
            return exts_map[args]
        else:
            raise RuntimeError

    result = [convert_tree(tree) for tree in trees]

    return domain, result

