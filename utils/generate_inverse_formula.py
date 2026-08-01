
def generate_inverse_formula(expr: sympy.Expr, var: sympy.Symbol) -> sympy.Expr | None:
    """
     Analyze an expression to see if it matches a specific invertible pattern that we
     know how to reverse.

     We're looking for expressions that are sums of terms where each term extracts a
     distinct bounded range from the input variable, like:

         y = c₀*a₀ + c₁*a₁ + c₂*a₂ + ... + cₙ*aₙ

     where each aᵢ must be one of these specific patterns:
     - ModularIndexing(var, divisor, modulo)
     - FloorDiv(ModularIndexing(var, 1, modulo), divisor)
     - FloorDiv(var, divisor)
     - var (the variable itself)

     The key pattern we need is:
     - Coefficients are strictly decreasing: c₀ > c₁ > c₂ > ... > cₙ
     - Each coefficient matches the product of ranges of later terms (mixed-radix property)
     - Each term extracts a bounded range, creating non-overlapping "slots"

     If we find this pattern, we can generate the reconstruction transformation that
     decomposes the variable and rebuilds it using the correct multipliers.

     EXAMPLE:
     Input: 100*((p//100)) + 10*((p%100)//10) + (p%10)

     Returns the reconstruction expression:
         remainder₀ = p
         component₀ = remainder₀ // 100          # hundreds digit
         remainder₁ = remainder₀ % 100
         component₁ = remainder₁ // 10           # tens digit
         remainder₂ = remainder₁ % 10
         component₂ = remainder₂                 # ones digit
         result = component₀*100 + component₁*10 + component₂*1

    This decomposes p into its components and rebuilds it using the original
     multipliers, which should equal the input expression.

     Args:
         expr: Expression to analyze (sum of terms with ModularIndexing, FloorDiv, etc.)
         var: The variable being decomposed

     Returns:
         None if not invertible, or the reconstruction expression

     References:
         Mixed-radix systems: https://en.wikipedia.org/wiki/Mixed_radix
    """
    # Step 1: Parse all terms
    terms = parse_terms(expr, var)
    if not terms:
        return None

    # Step 2: Sort by coefficient (descending)
    coeffs = [t.coefficient for t in terms]
    idxs = reversed(argsort_sym(V.graph.sizevars.shape_env, coeffs))
    terms = [terms[i] for i in idxs]

    # Step 3: Check invertibility conditions
    if not check_invertibility(terms):
        return None

    return generate_reconstruction_expr(terms, var)

