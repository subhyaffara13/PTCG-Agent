
def _get_unbacked_replacements(shape_env: ShapeEnv) -> dict[sympy.Expr, sympy.Expr]:
    """Builds a mapping from unbacked expressions to canonical equivalents
    using a union-find algorithm over deferred runtime asserts.
    Used by optimization_hint to resolve unbacked symbols to consistent values."""
    from collections import defaultdict

    from torch.fx.experimental.symbolic_shapes import has_free_unbacked_symbols
    from torch.utils._ordered_set import OrderedSet

    if shape_env._unbacked_replacements is not None:
        return shape_env._unbacked_replacements

    class CanonicalExprFinder:
        """
        A disjoint-set/union-find data structure that can return the
        "canonical" expression for a group of equivalent expressions.
        - The canonical expression must come from the input eq_graph.
        - The heuristics used to choose a leader determines which
        expression becomes the canonical expression.
        """

        def __init__(self, eq_graph: dict[sympy.Expr, OrderedSet[sympy.Expr]]):
            self.eq_graph = eq_graph
            self.expressions = list(eq_graph.keys())
            self.reverse_expressions = {
                expr: i for i, expr in enumerate(self.expressions)
            }
            self.leader = list(range(len(self.expressions)))
            self.size = [1] * len(self.expressions)
            self._build_canonical_expr_mapping()

        def _build_canonical_expr_mapping(self):
            for expr, edges in self.eq_graph.items():
                for adj in edges:
                    self.union_expr(expr, adj)

        def union_expr(self, a: sympy.Expr, b: sympy.Expr):
            return self.union(self.reverse_expressions[a], self.reverse_expressions[b])

        def union(self, a: int, b: int):
            rootA = self.find(a)
            rootB = self.find(b)
            if rootA == rootB:
                return False
            leader, other = self.choose_leader(rootA, rootB)
            self.leader[other] = leader
            self.size[leader] += self.size[other]
            return True

        def find_expr(self, expr: sympy.Expr):
            parent = self.find(self.reverse_expressions[expr])
            return self.expressions[parent]

        def find(self, x: int):
            if self.leader[x] != x:
                self.leader[x] = self.find(self.leader[x])
            return self.leader[x]

        def choose_leader(self, a: int, b: int):
            """
            The leader will become the canonical expression.
            Returns a (leader, follower) tuple.

            Heuristics:
            1. Backed expression or constants preferred over unbacked expr
            2. Simpler sub-expr when one contains the other
            3. Higher frequency across equalities from deferred runtime assertions
            4. Size of the set
            5. Fallback to sympy.Basic.compare
            """

            def _choose(x: int, y: int) -> bool:
                lhs, rhs = self.expressions[x], self.expressions[y]

                any_unbacked_lhs = has_free_unbacked_symbols(lhs)
                any_unbacked_rhs = has_free_unbacked_symbols(rhs)
                if any_unbacked_lhs != any_unbacked_rhs:
                    return bool(any_unbacked_rhs)

                if lhs.has(rhs):
                    return False
                elif rhs.has(lhs):
                    return True

                degrees_lhs = len(self.eq_graph[lhs])
                degrees_rhs = len(self.eq_graph[rhs])
                if degrees_lhs != degrees_rhs:
                    return degrees_lhs > degrees_rhs

                if self.size[x] != self.size[y]:
                    return self.size[x] > self.size[y]

                return lhs.compare(rhs) == -1

            if _choose(a, b):
                return a, b
            return b, a

    # Build an undirected graph using ShapeEnv's deferred runtime assertions.
    shape_env._equality_graph = defaultdict(OrderedSet)
    for assertions in shape_env.deferred_runtime_asserts.values():
        for assertion in assertions:
            if not isinstance(assertion.expr, sympy.Equality):
                continue
            lhs = sympy.sympify(assertion.expr.lhs)
            rhs = sympy.sympify(assertion.expr.rhs)
            shape_env._equality_graph[lhs].add(rhs)
            shape_env._equality_graph[rhs].add(lhs)

    uf = CanonicalExprFinder(shape_env._equality_graph)

    shape_env._unbacked_replacements = {}
    for expr in shape_env._equality_graph:
        canonical_expr = uf.find_expr(expr)
        if expr != canonical_expr:
            shape_env._unbacked_replacements[expr] = canonical_expr

    return shape_env._unbacked_replacements

