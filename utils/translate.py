
def translate(
    bindings: Sequence[Expr | Binding],
    goals: Sequence[NamedCType | Binding],
    *,
    method: bool = False,
    allow_expensive_conversions: bool = False,
) -> list[Expr]:
    binding_exprs: list[Expr] = []
    for b in bindings:
        if isinstance(b, Binding):
            binding_exprs.append(
                Expr(
                    expr=b.name,
                    type=b.nctype,
                )
            )
        else:
            binding_exprs.append(b)

    goal_ctypes: list[NamedCType] = []
    for g in goals:
        if isinstance(g, Binding):
            goal_ctypes.append(g.nctype)
        else:
            goal_ctypes.append(g)

    # Add all the bindings to the context
    ctx: dict[NamedCType, str] = {}
    for b in binding_exprs:
        ctx[b.type] = b.expr

        # While we're at it, do some simple forward inference, looking through
        # constructors.
        #
        # NB: When should you do forward inference versus backward inference?
        # The general idea:
        #
        #   - Backward inference WHEN the goal gets smaller
        #   - Forward inference WHEN the hypothesis gets smaller
        #
        # This helps ensure termination: backward inference starts with a goal
        # and tries to make it simpler and simpler until it's trivial; if the
        # goal can grow in size, we blow up to a really huge goal size.
        # Similarly, with forward inference we take hypotheses and decompose
        # them into simpler hypotheses; if hypotheses could expand in size,
        # we also have potential nontermination.  (In the code below, forward
        # inference is only ever carried out at a single step, but you could
        # imagine repeated application of forward inference being profitable.)
        #
        # A good starting point in the literature for exploring more about proof
        # search are these lecture notes
        # https://www.cs.cmu.edu/~fp/courses/oregon-m10/04-focusing.pdf
        #
        # TODO: My kingdom for a pattern matcher
        # https://www.python.org/dev/peps/pep-0634/
        #
        # TODO: This could get us in recomputation trouble if b.expr is nontrivial.
        # Fix this by implementing some sort of sharing so that if multiple
        # goals share the same expression, we only compute it once.  This seems
        # to matter in practice as compiler is often unwilling to CSE nontrivial
        # expressions like scalar.to<scalar_t>()
        t = b.type
        if (
            isinstance(t, ConstRefCType)
            and isinstance(t.elem, OptionalCType)
            and isinstance(t.elem.elem, BaseCType)
            and str(t.elem.elem.type) == "at::Tensor"
        ):
            ctx[NamedCType(t.elem.elem.name, ConstRefCType(BaseCType(tensorT)))] = (
                f"({b.expr}.has_value() ? *{b.expr} : at::Tensor())"
            )

        if t.type == ConstRefCType(OptionalCType(BaseCType(tensorT))):
            ctx[NamedCType(t.name, BaseCType(optionalTensorRefT))] = (
                f"(({b.expr}.has_value() && (*{b.expr}).defined()) ? at::OptionalTensorRef(*{b.expr}) : at::OptionalTensorRef())"
            )

        if t.type == ConstRefCType(BaseCType(scalarT)):
            ctx[NamedCType(t.name, BaseCType(opmath_t))] = f"({b.expr}).to<opmath_t>()"

        if t.type == ConstRefCType(OptionalCType(BaseCType(scalarT))):
            ctx[NamedCType(t.name, BaseCType(optionalScalarRefT))] = (
                f"({b.expr}.has_value() ? at::OptionalScalarRef(&({b.expr}.value())) : at::OptionalScalarRef())"
            )

        if t.type == BaseCType(scalar_t):
            ctx[NamedCType(t.name, BaseCType(opmath_t))] = (
                f"static_cast<opmath_t>({b.expr})"
            )

        # [Note: IOptTensorListRef]
        if t.type == ConstRefCType(ListCType(OptionalCType(BaseCType(tensorT)))):
            ctx[NamedCType(t.name, BaseCType(iOptTensorListRefT))] = (
                f"at::IOptTensorListRef({b.expr})"
            )

    # Add implicit bindings if the generated code is inside a Tensor method
    if method:
        ctx[NamedCType("self", MutRefCType(BaseCType(tensorT)))] = (
            "const_cast<Tensor&>(*this)"
        )
        ctx[NamedCType("self", ConstRefCType(BaseCType(tensorT)))] = (
            "const_cast<Tensor&>(*this)"
        )
        # This is better!  Byte-for-byte compat
        # ctx[NamedCType("self", ConstRefCType(BaseCType(tensorT)))] = "*this"

    def unsat(goal: NamedCType) -> NoReturn:
        ctx_desc = "\n".join(
            f"  {t.cpp_type()} {t.name}; // {e}" for t, e in ctx.items()
        )
        raise UnsatError(
            f"""
Failed to synthesize the expression "{goal.cpp_type()} {goal.name}".
When I failed, the following bindings were available in the context:

{ctx_desc}

This probably means there is a missing rule in the rules of torchgen.api.translate.
Check this module for more information.
"""
        )

    # A shitty backtracking search implementation.  It's shitty because it
    # does backtracking via stack (bad idea!) and for the most part tries to
    # avoid backtracking.  In particular, if
    # direct=True, we won't try to do any fancy synthesis, just trivial
    # conversions (e.g., "T a" is OK for "const T& a").  So all of the
    # existing rules in this function simply try to solve immediately,
    # and bail if things don't work out.
    def solve(goal: NamedCType, *, direct: bool) -> str:
        def direct_solve(goal: NamedCType) -> str:
            return solve(goal, direct=True)

        if goal in ctx:
            # Trivial
            return ctx[goal]

        # const & is satisfied with mutable &
        if isinstance(goal.type, ConstRefCType):
            try:
                # WARNING: not strictly decreasing; be careful not
                # to add a direct conversion that goes satisfies
                # mutable& with const&
                return solve(
                    NamedCType(goal.name, MutRefCType(goal.type.elem)), direct=direct
                )
            except UnsatError:
                pass

        # mutable & is satisfied with value
        if isinstance(goal.type, MutRefCType):
            try:
                return solve(NamedCType(goal.name, goal.type.elem), direct=direct)
            except UnsatError:
                pass

        # TODO: These are referentially equal, shouldn't have to do this;
        # ensuring we don't use type synonym IntArrayRef in codegen would
        # help
        if goal.type == ArrayRefCType(BaseCType(longT)):
            return solve(NamedCType(goal.name, BaseCType(intArrayRefT)), direct=direct)

        if direct:
            unsat(goal)

        # For now, all of these rules are mutually exclusive.
        if goal == NamedCType("memory_format", OptionalCType(BaseCType(memoryFormatT))):
            memory_format = direct_solve(
                NamedCType(
                    SpecialArgName.possibly_redundant_memory_format,
                    OptionalCType(BaseCType(memoryFormatT)),
                )
            )
            # No need to join "memory_format" and "options" if the target API takes "options" directly.
            # Otherwise it will cause the redundant memory_format error.
            if options_ctype in goal_ctypes:
                return memory_format
            try:
                options = direct_solve(options_ctype)
                return f"c10::impl::check_tensor_options_and_extract_memory_format({options}, {memory_format})"
            except UnsatError:
                return memory_format
        elif goal == NamedCType("options", BaseCType(tensorOptionsT)):
            dtype = direct_solve(
                NamedCType("dtype", OptionalCType(BaseCType(scalarTypeT)))
            )
            pin_memory = direct_solve(
                NamedCType("pin_memory", OptionalCType(BaseCType(boolT)))
            )
            device = direct_solve(
                NamedCType("device", OptionalCType(BaseCType(deviceT)))
            )
            layout = direct_solve(
                NamedCType("layout", OptionalCType(BaseCType(layoutT)))
            )
            return f"TensorOptions().dtype({dtype}).layout({layout}).device({device}).pinned_memory({pin_memory})"

        elif goal == NamedCType("dtype", OptionalCType(BaseCType(scalarTypeT))):
            try:
                options = direct_solve(options_ctype)
                return f"c10::optTypeMetaToScalarType({options}.dtype_opt())"
            except UnsatError:
                out_tensor = direct_solve(out_tensor_ctype)
                return f"{out_tensor}.scalar_type()"

        elif goal == NamedCType("layout", OptionalCType(BaseCType(layoutT))):
            try:
                options = direct_solve(options_ctype)
                return f"{options}.layout_opt()"
            except UnsatError:
                out_tensor = direct_solve(out_tensor_ctype)
                return f"{out_tensor}.layout()"

        elif goal == NamedCType("device", OptionalCType(BaseCType(deviceT))):
            try:
                options = direct_solve(options_ctype)
                return f"{options}.device_opt()"
            except UnsatError:
                out_tensor = direct_solve(out_tensor_ctype)
                return f"{out_tensor}.device()"

        elif goal == NamedCType("pin_memory", OptionalCType(BaseCType(boolT))):
            try:
                options = direct_solve(options_ctype)
                return f"{options}.pinned_memory_opt()"
            except UnsatError:
                # If we're calling a factory op from its out= variant,
                # We don't actually care about the value of pin_memory.
                out_tensor = direct_solve(out_tensor_ctype)
                return "::std::nullopt"

        # We can always do translations from value types to reference types, like vector<int> -> IntArrayRef
        elif goal.type == BaseCType(intArrayRefT):
            try:
                return direct_solve(NamedCType(goal.name, longVec_ctype))
            except UnsatError:
                # We can also go SymIntArrayRef -> IntArrayRef
                symIntArrayRef_type = direct_solve(
                    NamedCType(goal.name, BaseCType(symIntArrayRefT))
                )
                return f"C10_AS_INTARRAYREF_SLOW({symIntArrayRef_type})"
        elif goal.type == BaseCType(symIntArrayRefT):
            try:
                r = direct_solve(NamedCType(goal.name, BaseCType(intArrayRefT)))
                return f"c10::fromIntArrayRefSlow({r})"
            except UnsatError:
                return direct_solve(NamedCType(goal.name, longSymVec_ctype))
        elif goal.type == BaseCType(SymIntT):
            return direct_solve(NamedCType(goal.name, BaseCType(longT)))
        elif goal.type == OptionalCType(BaseCType(SymIntT)):
            argname = direct_solve(
                NamedCType(goal.name, OptionalCType(BaseCType(longT)))
            )
            return f"{argname}.has_value() ? ::std::make_optional(c10::SymInt(*{argname})) : ::std::nullopt"
        elif goal.type == BaseCType(longT):
            symInt_type = direct_solve(NamedCType(goal.name, BaseCType(SymIntT)))
            return f"{symInt_type}.guard_int(__FILE__, __LINE__)"
        elif goal.type == OptionalCType(BaseCType(longT)):
            argname = direct_solve(
                NamedCType(goal.name, OptionalCType(BaseCType(SymIntT)))
            )
            return f"{argname}.has_value() ? ::std::make_optional({argname}->guard_int(__FILE__, __LINE__)) : ::std::nullopt"
        elif goal.type == BaseCType(optionalIntArrayRefT):
            try:
                return direct_solve(NamedCType(goal.name, optionalLongVec_ctype))
            except UnsatError:
                argname = direct_solve(
                    NamedCType(goal.name, BaseCType(optionalSymIntArrayRefT))
                )
                return f"{argname}.has_value() ? ::std::make_optional(C10_AS_INTARRAYREF_SLOW(*{argname})) : ::std::nullopt"
        elif goal.type == BaseCType(optionalSymIntArrayRefT):
            # TODO: You might also want to solve this from longSymVec_ctype or
            # an optional version of it
            argname = direct_solve(
                NamedCType(goal.name, BaseCType(optionalIntArrayRefT))
            )
            return f"{argname}.has_value() ? ::std::make_optional(c10::fromIntArrayRefSlow(*{argname})) : ::std::nullopt"
        elif goal.type == BaseCType(optionalScalarRefT):
            return direct_solve(NamedCType(goal.name, optionalScalar_ctype))
        elif goal.type == BaseCType(optionalTensorRefT):
            return direct_solve(NamedCType(goal.name, optionalTensor_ctype))

        # Note [translation from C++ reference to value types]
        # The below cases are all for when we have an argument with a reference type,
        # and a corresponding goal with a value type.
        # These are needed when we populate the inputs to a lambda capture and we need
        # to guarantee the lifetime of each captured argument.
        # We guard it with an explicit kwarg because converting to a value type is expensive
        # (O(n)) to convert from IntArrayRef to vector<int>),
        # so the caller of translate() should be explicit that they need it.
        if allow_expensive_conversions:
            if goal.type == VectorCType(BaseCType(longT)):
                intArrayRef_ctype = NamedCType(goal.name, BaseCType(intArrayRefT))
                argname = direct_solve(intArrayRef_ctype)
                return f"{argname}.vec()"
            if goal.type == VectorCType(BaseCType(SymIntT)):
                symIntArrayRef_ctype = NamedCType(goal.name, BaseCType(symIntArrayRefT))
                argname = direct_solve(symIntArrayRef_ctype)
                return f"{argname}.vec()"
            elif goal.type == OptionalCType(VectorCType(BaseCType(longT))):
                optionalIntArrayRef_ctype = NamedCType(
                    goal.name, BaseCType(optionalIntArrayRefT)
                )
                argname = direct_solve(optionalIntArrayRef_ctype)
                return f"{argname}.has_value() ? ::std::make_optional({argname}->vec()) : ::std::nullopt"
            elif goal.type == OptionalCType(BaseCType(scalarT)):
                optionalScalarRef_ctype = NamedCType(
                    goal.name, BaseCType(optionalScalarRefT)
                )
                argname = direct_solve(optionalScalarRef_ctype)
                return f"{argname}.has_value() ? ::std::make_optional({argname}) : ::std::nullopt"
            elif goal.type == OptionalCType(BaseCType(scalarT)):
                optionalTensorRef_ctype = NamedCType(
                    goal.name, BaseCType(optionalTensorRefT)
                )
                argname = direct_solve(optionalTensorRef_ctype)
                return f"{argname}.has_value() ? ::std::make_optional({argname}) : ::std::nullopt"
            # Technically, we also need to handle cases of C++ containers holding reference types.
            # But there currently aren't any ops that require lambda capture codegen
            # With arguments like ::std::vector<IntArrayRef>.
            # If that changes, we'll have to add the translation here.

        # We allow const casting on tensors, since const-correctness is a bit broken for at::Tensor.
        # We could probably generalize this to non-tensor types too.
        if goal.type == MutRefCType(BaseCType(tensorT)):
            const_ref_tensor_ctype = NamedCType(
                goal.name, ConstRefCType(BaseCType(tensorT))
            )
            argname = direct_solve(const_ref_tensor_ctype)
            return f"const_cast<Tensor&>({argname})"

        unsat(goal)

    return [Expr(solve(g, direct=False), g) for g in goal_ctypes]


def translate(x, y):
    """Return the matrix to translate a 2-D point by x and y."""
    rv = eye(3)
    rv[2, 0] = x
    rv[2, 1] = y
    return rv


def translate(s: str) -> str:
    r'''
    Check for a modifier ending the string.  If present, convert the
    modifier to latex and translate the rest recursively.

    Given a description of a Greek letter or other special character,
    return the appropriate latex.

    Let everything else pass as given.

    >>> from sympy.printing.latex import translate
    >>> translate('alphahatdotprime')
    "{\\dot{\\hat{\\alpha}}}'"
    '''
    # Process the rest
    tex = tex_greek_dictionary.get(s)
    if tex:
        return tex
    elif s.lower() in greek_letters_set:
        return "\\" + s.lower()
    elif s in other_symbols:
        return "\\" + s
    else:
        # Process modifiers, if any, and recurse
        for key in sorted(modifier_dict.keys(), key=len, reverse=True):
            if s.lower().endswith(key) and len(s) > len(key):
                return modifier_dict[key](translate(s[:-len(key)]))
        return s


def translate(s, a, b=None, c=None):
    """Return ``s`` where characters have been replaced or deleted.

    SYNTAX
    ======

    translate(s, None, deletechars):
        all characters in ``deletechars`` are deleted
    translate(s, map [,deletechars]):
        all characters in ``deletechars`` (if provided) are deleted
        then the replacements defined by map are made; if the keys
        of map are strings then the longer ones are handled first.
        Multicharacter deletions should have a value of ''.
    translate(s, oldchars, newchars, deletechars)
        all characters in ``deletechars`` are deleted
        then each character in ``oldchars`` is replaced with the
        corresponding character in ``newchars``

    Examples
    ========

    >>> from sympy.utilities.misc import translate
    >>> abc = 'abc'
    >>> translate(abc, None, 'a')
    'bc'
    >>> translate(abc, {'a': 'x'}, 'c')
    'xb'
    >>> translate(abc, {'abc': 'x', 'a': 'y'})
    'x'

    >>> translate('abcd', 'ac', 'AC', 'd')
    'AbC'

    There is no guarantee that a unique answer will be
    obtained if keys in a mapping overlap are the same
    length and have some identical sequences at the
    beginning/end:

    >>> translate(abc, {'ab': 'x', 'bc': 'y'}) in ('xc', 'ay')
    True
    """

    mr = {}
    if a is None:
        if c is not None:
            raise ValueError('c should be None when a=None is passed, instead got %s' % c)
        if b is None:
            return s
        c = b
        a = b = ''
    else:
        if isinstance(a, dict):
            short = {}
            for k in list(a.keys()):
                if len(k) == 1 and len(a[k]) == 1:
                    short[k] = a.pop(k)
            mr = a
            c = b
            if short:
                a, b = [''.join(i) for i in list(zip(*short.items()))]
            else:
                a = b = ''
        elif len(a) != len(b):
            raise ValueError('oldchars and newchars have different lengths')

    if c:
        val = str.maketrans('', '', c)
        s = s.translate(val)
    s = replace(s, mr)
    n = str.maketrans(a, b)
    return s.translate(n)


def translate(input, translation):
    """
    >>> translate('dvorak', to_dvorak)
    'ekrpat'
    >>> translate('qwerty', to_qwerty)
    'x,dokt'
    """
    return input.translate(translation)


def translate(matrix, x=0.0, y=0.0, z=0.0):
    """
    Translate (move) a matrix in the x, y and z axes.

    :param matrix: Matrix to translate.
    :param x: direction and magnitude to translate in x axis. Defaults to 0.
    :param y: direction and magnitude to translate in y axis. Defaults to 0.
    :param z: direction and magnitude to translate in z axis. Defaults to 0.
    :return: The translated matrix.
    """
    translation_matrix = array(
        [
            [1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, z],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=matrix.dtype,
    ).T
    matrix[...] = dot(matrix, translation_matrix)
    return matrix


def translate(a, table, deletechars=None):
    """
    For each element in `a`, return a copy of the string where all
    characters occurring in the optional argument `deletechars` are
    removed, and the remaining characters have been mapped through the
    given translation table.

    Calls :meth:`str.translate` element-wise.

    Parameters
    ----------
    a : array-like, with ``bytes_`` or ``str_`` dtype

    table : str of length 256

    deletechars : str

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See Also
    --------
    str.translate

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['a1b c', '1bca', 'bca1'])
    >>> table = a[0].maketrans('abc', '123')
    >>> deletechars = ' '
    >>> np.char.translate(a, table, deletechars)
    array(['112 3', '1231', '2311'], dtype='<U5')

    """
    a_arr = np.asarray(a)
    if issubclass(a_arr.dtype.type, np.str_):
        return _vec_string(
            a_arr, a_arr.dtype, 'translate', (table,))
    else:
        return _vec_string(
            a_arr,
            a_arr.dtype,
            'translate',
            [table] + _clean_args(deletechars)
        )


def translate(position: int, direction: Action, columns: int, rows: int) -> int:
    row, column = row_col(position, columns)
    row_offset, column_offset = direction.to_row_col()
    row = (row + row_offset) % rows
    column = (column + column_offset) % columns
    return row * columns + column

