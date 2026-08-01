
def canonicalize(
    ep: ExportedProgram, constants: set[str] | None = None
) -> ExportedProgram:
    """
    Normalize a serialized ExportedProgram, so that different eager program which
    shares the same semantics can get a single representation on disk.

    This function canonicalizes an ExportedProgram by:

    1. Sorting nodes in topological order.
    2. Rename nodes to have unique names.
    3. Remove unstable fields.
    4. Aggregate the above program fields.
    5. Recurse in subgraphs.

    Args:
        ep (ExportedProgram): The ExportedProgram to canonicalize.
        constants (Optional[set[str]]): Set of constants names

    Returns:
        ExportedProgram: The canonicalized exported program.
    """
    ep = copy.deepcopy(ep)
    # pyrefly: ignore [annotation-mismatch, redefinition]
    constants: set[str] = constants or set()

    opset_version = dict(sorted(ep.opset_version.items(), key=operator.itemgetter(0)))
    range_constraints = dict(
        sorted(ep.range_constraints.items(), key=operator.itemgetter(0))
    )
    guards_code = sorted(ep.guards_code)
    module_call_graph = sorted(ep.graph_module.module_call_graph, key=lambda x: x.fqn)
    signature = ep.graph_module.signature
    graph = ep.graph_module.graph

    if len(graph.inputs) != len(signature.input_specs):
        raise AssertionError(
            f"graph.inputs length {len(graph.inputs)} != signature.input_specs length {len(signature.input_specs)}"
        )
    if len(graph.outputs) != len(signature.output_specs):
        raise AssertionError(
            f"graph.outputs length {len(graph.outputs)} != signature.output_specs length {len(signature.output_specs)}"
        )

    def rank_input(inp) -> tuple[int, str | None, int]:
        idx, (_arg, spec) = inp
        if not isinstance(spec, InputSpec):
            raise AssertionError(f"expected InputSpec, got {type(spec).__name__}")
        if spec.type == "user_input":
            return 5, None, idx
        elif spec.type == "parameter":
            return 1, spec.parameter.parameter_name, idx
        elif spec.type == "buffer":
            return 2, spec.buffer.buffer_name, idx
        elif spec.type == "tensor_constant":
            return 3, spec.tensor_constant.tensor_constant_name, idx
        elif spec.type == "custom_obj":
            return 4, spec.custom_obj.custom_obj_name, idx
        elif spec.type == "token":
            return 0, None, idx
        elif spec.type == "constant_input":
            return 6, spec.constant_input.name, idx
        else:
            raise AssertionError(f"Unknown input type: {spec}")

    def rank_output(out) -> tuple[int, str | None, int]:
        idx, (_arg, spec) = out
        if not isinstance(spec, OutputSpec):
            raise AssertionError(f"expected OutputSpec, got {type(spec).__name__}")
        if spec.type == "user_output":
            return 4, None, idx
        elif spec.type == "loss_output":
            return 4, None, idx
        elif spec.type == "parameter_mutation":
            return 1, spec.parameter_mutation.parameter_name, idx
        elif spec.type == "buffer_mutation":
            return 2, spec.buffer_mutation.buffer_name, idx
        elif spec.type == "gradient_to_parameter":
            return 5, spec.gradient_to_parameter.parameter_name, idx
        elif spec.type == "gradient_to_user_input":
            return 6, None, idx
        elif spec.type == "user_input_mutation":
            return 3, None, idx
        elif spec.type == "token":
            return 0, None, idx
        else:
            raise AssertionError(f"Unknown output type: {spec}")

    sorted_ins = sorted(
        enumerate(zip(graph.inputs, signature.input_specs)), key=rank_input
    )

    if len(sorted_ins) > 0:
        sorted_inputs, input_specs = zip(*(i for idx, i in sorted_ins))  # type: ignore[assignment]
    else:
        sorted_inputs = ()
        input_specs = ()

    sorted_outs = sorted(
        enumerate(zip(graph.outputs, signature.output_specs)), key=rank_output
    )
    sorted_outputs, output_specs = zip(*(i for idx, i in sorted_outs))  # type: ignore[assignment]

    sorted_graph, replace_table = _canonicalize_graph(
        sorted_inputs, sorted_outputs, graph, constants
    )

    def replace_input(spec):
        if not isinstance(spec, InputSpec):
            raise AssertionError(f"expected InputSpec, got {type(spec).__name__}")
        if spec.type == "user_input":
            arg = spec.user_input.arg
            if arg.type == "as_tensor":
                t = arg.as_tensor
                t.name = replace_table[t.name]
            elif arg.type == "as_sym_int":
                s = arg.as_sym_int
                if s.type == "as_name":
                    s.as_name = replace_table[s.as_name]
                elif s.type == "as_int":
                    pass
                else:
                    raise AssertionError(f"Unknown sym_int type: {s}")
            elif arg.type == "as_sym_float":
                f = arg.as_sym_float
                if f.type == "as_name":
                    f.as_name = replace_table[f.as_name]
                elif f.type == "as_float":
                    pass
                else:
                    raise AssertionError(f"Unknown sym_float type: {f}")
            elif arg.type in (
                "as_none",
                "as_bool",
                "as_int",
                "as_float",
                "as_string",
                "as_custom_obj",
            ):
                return
            else:
                raise AssertionError(f"Unknown input type: {arg}")
        elif spec.type == "parameter":
            t = spec.parameter.arg
            t.name = replace_table[t.name]
        elif spec.type == "buffer":
            t = spec.buffer.arg
            t.name = replace_table[t.name]
        elif spec.type == "tensor_constant":
            t = spec.tensor_constant.arg
            t.name = replace_table[t.name]
        elif spec.type == "custom_obj":
            t_custom_obj = spec.custom_obj.arg
            t_custom_obj.name = replace_table[t_custom_obj.name]
            return
        elif spec.type == "token":
            tok = spec.token.arg
            tok.name = replace_table[tok.name]
        elif spec.type == "constant_input":
            return
        else:
            raise AssertionError(f"Unknown input type: {spec}")

    def replace_output(out):
        if not isinstance(spec, OutputSpec):
            raise AssertionError(f"expected OutputSpec, got {type(spec).__name__}")
        if spec.type == "user_output":
            arg = spec.user_output.arg
            if arg.type == "as_tensor":
                t = arg.as_tensor
                t.name = replace_table[t.name]
            elif arg.type == "as_sym_int":
                s = arg.as_sym_int
                if s.type == "as_name":
                    s.as_name = replace_table[s.as_name]
                elif s.type == "as_int":
                    pass
                else:
                    raise AssertionError(f"Unknown sym_int type: {s}")
            elif arg.type == "as_sym_float":
                f = arg.as_sym_float
                if f.type == "as_name":
                    f.as_name = replace_table[f.as_name]
                elif f.type == "as_float":
                    pass
                else:
                    raise AssertionError(f"Unknown sym_float type: {f}")
            elif arg.type in ("as_none", "as_bool", "as_int", "as_float", "as_string"):
                return
            else:
                raise AssertionError(f"Unknown input type: {arg}")
        elif spec.type == "loss_output":
            t = spec.loss_output.arg
            t.name = replace_table[t.name]
        elif spec.type == "buffer_mutation":
            t = spec.buffer_mutation.arg
            t.name = replace_table[t.name]
        elif spec.type == "parameter_mutation":
            t = spec.parameter_mutation.arg
            t.name = replace_table[t.name]
        elif spec.type == "gradient_to_parameter":
            t = spec.gradient_to_parameter.arg
            t.name = replace_table[t.name]
        elif spec.type == "gradient_to_user_input":
            g = spec.gradient_to_user_input
            g.arg.name = replace_table[g.arg.name]
            g.user_input_name = replace_table[g.user_input_name]
        elif spec.type == "user_input_mutation":
            u = spec.user_input_mutation
            u.arg.name = replace_table[u.arg.name]
            u.user_input_name = replace_table[u.user_input_name]
        elif spec.type == "token":
            tok = spec.token.arg
            tok.name = replace_table[tok.name]
        else:
            raise AssertionError(f"Unknown output type: {spec}")

    for spec in input_specs:
        replace_input(spec)

    for spec in output_specs:
        replace_output(spec)

    return ExportedProgram(
        graph_module=GraphModule(
            graph=sorted_graph,
            signature=GraphSignature(
                input_specs=list(input_specs),
                output_specs=list(output_specs),
            ),
            module_call_graph=module_call_graph,
        ),
        opset_version=opset_version,
        range_constraints=range_constraints,
        schema_version=ep.schema_version,
        verifiers=ep.verifiers,
        torch_version=ep.torch_version,
        guards_code=guards_code,
    )


def canonicalize(g, dummies, msym, *v):
    """
    canonicalize tensor formed by tensors

    Parameters
    ==========

    g : permutation representing the tensor

    dummies : list representing the dummy indices
      it can be a list of dummy indices of the same type
      or a list of lists of dummy indices, one list for each
      type of index;
      the dummy indices must come after the free indices,
      and put in order contravariant, covariant
      [d0, -d0, d1,-d1,...]

    msym :  symmetry of the metric(s)
        it can be an integer or a list;
        in the first case it is the symmetry of the dummy index metric;
        in the second case it is the list of the symmetries of the
        index metric for each type

    v : list, (base_i, gens_i, n_i, sym_i) for tensors of type `i`

    base_i, gens_i : BSGS for tensors of this type.
        The BSGS should have minimal base under lexicographic ordering;
        if not, an attempt is made do get the minimal BSGS;
        in case of failure,
        canonicalize_naive is used, which is much slower.

    n_i :    number of tensors of type `i`.

    sym_i :  symmetry under exchange of component tensors of type `i`.

        Both for msym and sym_i the cases are
            * None  no symmetry
            * 0     commuting
            * 1     anticommuting

    Returns
    =======

    0 if the tensor is zero, else return the array form of
    the permutation representing the canonical form of the tensor.

    Algorithm
    =========

    First one uses canonical_free to get the minimum tensor under
    lexicographic order, using only the slot symmetries.
    If the component tensors have not minimal BSGS, it is attempted
    to find it; if the attempt fails canonicalize_naive
    is used instead.

    Compute the residual slot symmetry keeping fixed the free indices
    using tensor_gens(base, gens, list_free_indices, sym).

    Reduce the problem eliminating the free indices.

    Then use double_coset_can_rep and lift back the result reintroducing
    the free indices.

    Examples
    ========

    one type of index with commuting metric;

    `A_{a b}` and `B_{a b}` antisymmetric and commuting

    `T = A_{d0 d1} * B^{d0}{}_{d2} * B^{d2 d1}`

    `ord = [d0,-d0,d1,-d1,d2,-d2]` order of the indices

    g = [1, 3, 0, 5, 4, 2, 6, 7]

    `T_c = 0`

    >>> from sympy.combinatorics.tensor_can import get_symmetric_group_sgs, canonicalize, bsgs_direct_product
    >>> from sympy.combinatorics import Permutation
    >>> base2a, gens2a = get_symmetric_group_sgs(2, 1)
    >>> t0 = (base2a, gens2a, 1, 0)
    >>> t1 = (base2a, gens2a, 2, 0)
    >>> g = Permutation([1, 3, 0, 5, 4, 2, 6, 7])
    >>> canonicalize(g, range(6), 0, t0, t1)
    0

    same as above, but with `B_{a b}` anticommuting

    `T_c = -A^{d0 d1} * B_{d0}{}^{d2} * B_{d1 d2}`

    can = [0,2,1,4,3,5,7,6]

    >>> t1 = (base2a, gens2a, 2, 1)
    >>> canonicalize(g, range(6), 0, t0, t1)
    [0, 2, 1, 4, 3, 5, 7, 6]

    two types of indices `[a,b,c,d,e,f]` and `[m,n]`, in this order,
    both with commuting metric

    `f^{a b c}` antisymmetric, commuting

    `A_{m a}` no symmetry, commuting

    `T = f^c{}_{d a} * f^f{}_{e b} * A_m{}^d * A^{m b} * A_n{}^a * A^{n e}`

    ord = [c,f,a,-a,b,-b,d,-d,e,-e,m,-m,n,-n]

    g = [0,7,3, 1,9,5, 11,6, 10,4, 13,2, 12,8, 14,15]

    The canonical tensor is
    `T_c = -f^{c a b} * f^{f d e} * A^m{}_a * A_{m d} * A^n{}_b * A_{n e}`

    can = [0,2,4, 1,6,8, 10,3, 11,7, 12,5, 13,9, 15,14]

    >>> base_f, gens_f = get_symmetric_group_sgs(3, 1)
    >>> base1, gens1 = get_symmetric_group_sgs(1)
    >>> base_A, gens_A = bsgs_direct_product(base1, gens1, base1, gens1)
    >>> t0 = (base_f, gens_f, 2, 0)
    >>> t1 = (base_A, gens_A, 4, 0)
    >>> dummies = [range(2, 10), range(10, 14)]
    >>> g = Permutation([0, 7, 3, 1, 9, 5, 11, 6, 10, 4, 13, 2, 12, 8, 14, 15])
    >>> canonicalize(g, dummies, [0, 0], t0, t1)
    [0, 2, 4, 1, 6, 8, 10, 3, 11, 7, 12, 5, 13, 9, 15, 14]
    """
    from sympy.combinatorics.testutil import canonicalize_naive
    if not isinstance(msym, list):
        if msym not in (0, 1, None):
            raise ValueError('msym must be 0, 1 or None')
        num_types = 1
    else:
        num_types = len(msym)
        if not all(msymx in (0, 1, None) for msymx in msym):
            raise ValueError('msym entries must be 0, 1 or None')
        if len(dummies) != num_types:
            raise ValueError(
                'dummies and msym must have the same number of elements')
    size = g.size
    num_tensors = 0
    v1 = []
    for base_i, gens_i, n_i, sym_i in v:
        # check that the BSGS is minimal;
        # this property is used in double_coset_can_rep;
        # if it is not minimal use canonicalize_naive
        if not _is_minimal_bsgs(base_i, gens_i):
            mbsgs = get_minimal_bsgs(base_i, gens_i)
            if not mbsgs:
                can = canonicalize_naive(g, dummies, msym, *v)
                return can
            base_i, gens_i = mbsgs
        v1.append((base_i, gens_i, [[]] * n_i, sym_i))
        num_tensors += n_i

    if num_types == 1 and not isinstance(msym, list):
        dummies = [dummies]
        msym = [msym]
    flat_dummies = []
    for dumx in dummies:
        flat_dummies.extend(dumx)

    if flat_dummies and flat_dummies != list(range(flat_dummies[0], flat_dummies[-1] + 1)):
        raise ValueError('dummies is not valid')

    # slot symmetry of the tensor
    size1, sbase, sgens = gens_products(*v1)
    if size != size1:
        raise ValueError(
            'g has size %d, generators have size %d' % (size, size1))
    free = [i for i in range(size - 2) if i not in flat_dummies]
    num_free = len(free)

    # g1 minimal tensor under slot symmetry
    g1 = canonical_free(sbase, sgens, g, num_free)
    if not flat_dummies:
        return g1
    # save the sign of g1
    sign = 0 if g1[-1] == size - 1 else 1

    # the free indices are kept fixed.
    # Determine free_i, the list of slots of tensors which are fixed
    # since they are occupied by free indices, which are fixed.
    start = 0
    for i, (base_i, gens_i, n_i, sym_i) in enumerate(v):
        free_i = []
        len_tens = gens_i[0].size - 2
        # for each component tensor get a list od fixed islots
        for j in range(n_i):
            # get the elements corresponding to the component tensor
            h = g1[start:(start + len_tens)]
            fr = []
            # get the positions of the fixed elements in h
            for k in free:
                if k in h:
                    fr.append(h.index(k))
            free_i.append(fr)
            start += len_tens
        v1[i] = (base_i, gens_i, free_i, sym_i)
    # BSGS of the tensor with fixed free indices
    # if tensor_gens fails in gens_product, use canonicalize_naive
    size, sbase, sgens = gens_products(*v1)

    # reduce the permutations getting rid of the free indices
    pos_free = [g1.index(x) for x in range(num_free)]
    size_red = size - num_free
    g1_red = [x - num_free for x in g1 if x in flat_dummies]
    if sign:
        g1_red.extend([size_red - 1, size_red - 2])
    else:
        g1_red.extend([size_red - 2, size_red - 1])
    map_slots = _get_map_slots(size, pos_free)
    sbase_red = [map_slots[i] for i in sbase if i not in pos_free]
    sgens_red = [_af_new([map_slots[i] for i in y._array_form if i not in pos_free]) for y in sgens]
    dummies_red = [[x - num_free for x in y] for y in dummies]
    transv_red = get_transversals(sbase_red, sgens_red)
    g1_red = _af_new(g1_red)
    g2 = double_coset_can_rep(
        dummies_red, msym, sbase_red, sgens_red, transv_red, g1_red)
    if g2 == 0:
        return 0
    # lift to the case with the free indices
    g3 = _lift_sgens(size, pos_free, free, g2)
    return g3


def canonicalize(x):
    """Canonicalize the Hadamard product ``x`` with mathematical properties.

    Examples
    ========

    >>> from sympy import MatrixSymbol, HadamardProduct
    >>> from sympy import OneMatrix, ZeroMatrix
    >>> from sympy.matrices.expressions.hadamard import canonicalize
    >>> from sympy import init_printing
    >>> init_printing(use_unicode=False)

    >>> A = MatrixSymbol('A', 2, 2)
    >>> B = MatrixSymbol('B', 2, 2)
    >>> C = MatrixSymbol('C', 2, 2)

    Hadamard product associativity:

    >>> X = HadamardProduct(A, HadamardProduct(B, C))
    >>> X
    A.*(B.*C)
    >>> canonicalize(X)
    A.*B.*C

    Hadamard product commutativity:

    >>> X = HadamardProduct(A, B)
    >>> Y = HadamardProduct(B, A)
    >>> X
    A.*B
    >>> Y
    B.*A
    >>> canonicalize(X)
    A.*B
    >>> canonicalize(Y)
    A.*B

    Hadamard product identity:

    >>> X = HadamardProduct(A, OneMatrix(2, 2))
    >>> X
    A.*1
    >>> canonicalize(X)
    A

    Absorbing element of Hadamard product:

    >>> X = HadamardProduct(A, ZeroMatrix(2, 2))
    >>> X
    A.*0
    >>> canonicalize(X)
    0

    Rewriting to Hadamard Power

    >>> X = HadamardProduct(A, A, A)
    >>> X
    A.*A.*A
    >>> canonicalize(X)
     .3
    A

    Notes
    =====

    As the Hadamard product is associative, nested products can be flattened.

    The Hadamard product is commutative so that factors can be sorted for
    canonical form.

    A matrix of only ones is an identity for Hadamard product,
    so every matrices of only ones can be removed.

    Any zero matrix will make the whole product a zero matrix.

    Duplicate elements can be collected and rewritten as HadamardPower

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Hadamard_product_(matrices)
    """
    # Associativity
    rule = condition(
            lambda x: isinstance(x, HadamardProduct),
            flatten
        )
    fun = exhaust(rule)
    x = fun(x)

    # Identity
    fun = condition(
            lambda x: isinstance(x, HadamardProduct),
            rm_id(lambda x: isinstance(x, OneMatrix))
        )
    x = fun(x)

    # Absorbing by Zero Matrix
    def absorb(x):
        if any(isinstance(c, ZeroMatrix) for c in x.args):
            return ZeroMatrix(*x.shape)
        else:
            return x
    fun = condition(
            lambda x: isinstance(x, HadamardProduct),
            absorb
        )
    x = fun(x)

    # Rewriting with HadamardPower
    if isinstance(x, HadamardProduct):
        tally = Counter(x.args)

        new_arg = []
        for base, exp in tally.items():
            if exp == 1:
                new_arg.append(base)
            else:
                new_arg.append(HadamardPower(base, exp))

        x = HadamardProduct(*new_arg)

    # Commutativity
    fun = condition(
            lambda x: isinstance(x, HadamardProduct),
            sort(default_sort_key)
        )
    x = fun(x)

    # Unpacking
    x = unpack(x)
    return x

