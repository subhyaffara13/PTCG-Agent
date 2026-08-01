
def process_function(info: DifferentiabilityInfo, template: CodeTemplate) -> str:
    saved_variables: list[str] = []
    release_variables: list[str] = []
    saved_list_sizes: list[str] = []
    unpack: list[str] = []
    asserts: list[str] = []
    compute_index_ranges: list[str] = []
    getter_definitions: list[str] = []
    py_getsetdef_structs: list[str] = []
    compiled_args: list[str] = []
    apply_with_saved_before: list[str] = []
    apply_with_saved_after: list[str] = []
    apply_functional_args: list[str] = []
    apply_functional_args_ref_types: list[str] = []
    # Maps the name of an input (to the original forward operator;
    # examples are "self", "other") to the order in which they appear in the
    # operator.
    # For example; if the operator is foo(Tensor self, int64_t k, Tensor other),
    # the mapping is: {"self": 0, "other": 1}.
    # We use this mapping to populate needs_input_grad in some order and then grab
    # values from it.
    input_name_to_idx: dict[str, int] = {}

    for idx, arg in enumerate(info.args_with_derivatives):
        if arg.type in TENSOR_LIST_LIKE_CTYPES:
            size = f"{arg.name}_size_"
            saved_list_sizes.append(f"size_t {arg.name}_size_;")
            apply_functional_args.append(f"{arg.name}_size_")
            apply_functional_args_ref_types.append("size_t")
        else:
            size = "1"
        compute_index_ranges.append(f"auto {arg.name}_ix = gen.range({size});")
        input_name_to_idx[arg.name] = idx

    def save_var(var: SavedAttribute, is_output: bool) -> None:
        name = var.nctype.name
        type = var.nctype.type
        should_append_getsetdef = True
        should_append_raw_getsetdef = False
        visit_name = name
        uses_cpp_saved_variable_cls = False
        unpacked_ref_type = None

        if (
            type == BaseCType(tensorT)
            or type == OptionalCType(BaseCType(tensorT))
            or type == MutRefCType(OptionalCType(BaseCType(tensorT)))
            or (type == BaseCType(scalarT) and is_output)
        ):
            uses_cpp_saved_variable_cls = True
            saved_variables.append(f"SavedVariable {name}_;")
            release_variables.append(f"{name}_.reset_data();")
            ptr = "shared_from_this()" if is_output else ""
            unpack.append(f"auto {name} = {name}_.unpack({ptr});")
            getter_definitions.append(
                GETTER_DEFINITION_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_SAVEDVAR
                )
            )
            getter_definitions.append(
                GETTER_DEFINITION_RAW_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_RAW_SAVEDVAR
                )
            )
            should_append_raw_getsetdef = True
            visit_name = f"{name}_"
            unpacked_ref_type = "Tensor&"
        elif (
            type == BaseCType(tensorListT)
            or type == BaseCType(iTensorListRefT)
            or type == VectorCType(BaseCType(tensorT))
        ):
            # note(crcrpar): [nuanced return type of out-of-place foreach functions]
            # When an out-of-place foreach function whose return signature is `Tensor[]`
            # spells out its backward definitions in `derivatives.yaml`, and some of them depend on
            # `result`, `result`'s type is interpreted and treated as `std::vector<Tensor>`.
            # An out-of-place foreach whose backwards rely on their output doesn't suffer from this
            # difference if the definitions are codegen'ed.
            # This special case is needed for `_foreach_pow.List` and `_foreach_pow.ScalarAndTensor`
            # as of https://github.com/pytorch/pytorch/pull/105504.
            if type == VectorCType(BaseCType(tensorT)):
                if not (
                    info.func.func.name.name.base.startswith("_foreach") and is_output
                ):
                    raise AssertionError(
                        "VectorCType(BaseCType(tensorT)) requires foreach function and is_output"
                    )
            uses_cpp_saved_variable_cls = True
            saved_variables.append(f"std::vector<SavedVariable> {name}_;")
            saved_variables.append(f"bool {name}_released_ = false;")
            # Just clear() is sufficient, we don't need to loop and clear each variable.
            # Because the SavedVariable owns a tensor and a grad_fn, removing the SavedVariable makes them go away as well.
            release_variables.append(f"{name}_.clear();")
            release_variables.append(f"{name}_released_ = true;")
            ptr = "shared_from_this()" if is_output else "nullptr"
            unpack.append(f"auto {name} = unpack_list({name}_, {ptr});")
            asserts.append(f"TORCH_CHECK(!{name}_released_, ERR_BACKWARD_TWICE);")
            getter_definitions.append(
                GETTER_DEFINITION_VEC_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_VEC_SAVEDVAR
                )
            )
            getter_definitions.append(
                GETTER_DEFINITION_RAW_VEC_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_RAW_VEC_SAVEDVAR
                )
            )
            should_append_raw_getsetdef = True
            visit_name = f"{name}_"
            unpacked_ref_type = "std::vector<Tensor>&"
        elif type == ListCType(OptionalCType(BaseCType(tensorT))):
            uses_cpp_saved_variable_cls = True
            saved_variables.append(f"std::vector<SavedVariable> {name}_;")
            saved_variables.append(f"bool {name}_released_ = false;")
            # Just clear() is sufficient, we don't need to loop and clear each variable.
            # Because the SavedVariable owns a tensor and a grad_fn, removing the SavedVariable makes them go away as well.
            release_variables.append(f"{name}_.clear();")
            release_variables.append(f"{name}_released_ = true;")
            unpack.append(f"auto {name} = unpack_opt_list({name}_);")
            asserts.append(f"TORCH_CHECK(!{name}_released_, ERR_BACKWARD_TWICE);")
            getter_definitions.append(
                GETTER_DEFINITION_VEC_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_VEC_SAVEDVAR
                )
            )
            getter_definitions.append(
                GETTER_DEFINITION_RAW_VEC_SAVEDVAR.substitute(
                    op=info.op, name=name, body=GETTER_BODY_RAW_VEC_SAVEDVAR
                )
            )
            should_append_raw_getsetdef = True
            visit_name = f"{name}_"
            unpacked_ref_type = "torch::List<std::optional<Tensor>>&"
        elif type == BaseCType(intArrayRefT):
            saved_variables.append(f"std::vector<int64_t> {name};")
            getter_definitions.append(
                GETTER_DEFINITION.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_LONG
                )
            )
        elif type == BaseCType(symIntArrayRefT):
            saved_variables.append(f"std::vector<c10::SymInt> {name};")
            getter_definitions.append(
                GETTER_DEFINITION.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_SYMINT
                )
            )
        elif type == BaseCType(optionalIntArrayRefT):
            saved_variables.append(f"c10::OptionalArray<int64_t> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_LONG
                )
            )
        elif type == BaseCType(optionalSymIntArrayRefT):
            saved_variables.append(f"c10::OptionalArray<c10::SymInt> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_SYMINT
                )
            )
        elif type == OptionalCType(BaseCType(intArrayRefT)):
            saved_variables.append(f"c10::OptionalArray<int64_t> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_LONG
                )
            )
        elif type == OptionalCType(BaseCType(symIntArrayRefT)):
            saved_variables.append(f"c10::OptionalArray<c10::SymInt> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_SYMINT
                )
            )
        elif type == OptionalCType(ArrayRefCType(BaseCType(doubleT))):
            saved_variables.append(f"c10::OptionalArray<double> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                    op=info.op, name=name, body=GETTER_BODY_ARRAYREF_DOUBLE
                )
            )
        elif type == BaseCType(longT):
            saved_variables.append(f"{type.cpp_type()} {name} = 0;")
            getter_definitions.append(
                GETTER_DEFINITION.substitute(
                    op=info.op, name=name, body=GETTER_BODY_INT64_T
                )
            )
        elif type == BaseCType(SymIntT):
            saved_variables.append(f"c10::SymInt {name};")
            getter_definitions.append(
                GETTER_DEFINITION.substitute(
                    op=info.op, name=name, body=GETTER_BODY_SYMINT
                )
            )
        elif type == BaseCType(stringT):
            saved_variables.append(f"std::string {name};")
            getter_definitions.append(
                GETTER_DEFINITION.substitute(
                    op=info.op, name=name, body=GETTER_BODY_STRING
                )
            )
        elif type == OptionalCType(BaseCType(stringT)):
            saved_variables.append(f"std::optional<std::string> {name};")
            getter_definitions.append(
                GETTER_DEFINITION_OPT.substitute(
                    op=info.op, name=name, body=GETTER_BODY_STRING
                )
            )
        elif type == ArrayRefCType(
            elem=BaseCType(type=BaseCppType(ns="at", name="Scalar"))
        ):
            saved_variables.append(f"std::vector<at::Scalar> {name};")
            unpacked_ref_type = "std::vector<at::Scalar>&"
            saved_variables.append(f"bool {name}_released_ = false;")
            # Just clear() is sufficient, we don't need to loop and clear each variable.
            # Because the SavedVariable owns a tensor and a grad_fn, removing the SavedVariable makes them go away as well.
            release_variables.append(f"{name}.clear();")
            # release_variables.append(f"{name}_released_ = true;")
            # unpack.append(f"auto {name} = unpack_list({name}_);")
            # asserts.append(f"TORCH_CHECK(!{name}_released_, ERR_BACKWARD_TWICE);")
            getter_definitions.append(
                CodeTemplate(
                    """\
static PyObject* THP${op}_${name}_getter(THPCppFunction *self, void *_unused) {
  HANDLE_TH_ERRORS
  const auto *node = static_cast<${op}*>(self->cdata.get());
  const auto& prop = node->${name};
  if (node->${name}_released_) {
    PyErr_SetString(PyExc_RuntimeError, ERR_BACKWARD_TWICE);
    return nullptr;
  }
  ${body}
  END_HANDLE_TH_ERRORS
}
                            """
                ).substitute(
                    op=info.op,
                    name=name,
                    body=GETTER_BODY_VEC_SCALAR,
                )
            )
        else:
            # Check for indicators that you're putting a non-owning reference
            # into the saved variable field.  If this is spuriously firing,
            # edit this field.  Otherwise, you probably need to add a case
            # above.
            if not (
                "ref" not in type.cpp_type().lower()
                and "view" not in type.cpp_type().lower()
                and "*" not in type.cpp_type()
                and "&" not in type.cpp_type()
            ):
                raise AssertionError(
                    f"{type.cpp_type()} looks like it contains a non-owning reference"
                )
            saved_variables.append(f"{type.cpp_type()} {name};")

            if type in MISC_GETTER_DEFS:
                # pyrefly: ignore [bad-index, index-error]
                getter_def, body = MISC_GETTER_DEFS[type]
                getter_definitions.append(
                    getter_def.substitute(op=info.op, name=name, body=body)
                )
            else:
                # Types we don't expose python bindings to yet:
                #   TypeAndSize, at::ScalarType, TensorOptions, TensorGeometry,
                #   std::vector<std::vector<int64_t>>, std::vector<at::ScalarType>
                should_append_getsetdef = False

        if should_append_getsetdef:
            py_getsetdef_structs.append(
                PY_GETSETDEF_STRUCT.substitute(op=info.op, name=name)
            )
        if should_append_raw_getsetdef:
            py_getsetdef_structs.append(
                PY_RAW_GETSETDEF_STRUCT.substitute(op=info.op, name=name)
            )

        if uses_cpp_saved_variable_cls:
            compiled_args.append(
                f"args.collect({visit_name}, {'true' if is_output else 'false'});"
            )
        else:
            compiled_args.append(f"args.collect({visit_name});")
        apply_with_saved_before.append(f"saved.before({visit_name});")
        apply_with_saved_after.append(f"saved.after({visit_name});")

        if unpacked_ref_type is None:
            unpacked_ref_type = f"{saved_variables[-1].split(' ')[0]}&"
        apply_functional_args.append(str(name))
        apply_functional_args_ref_types.append(unpacked_ref_type)

    for var in sorted(info.all_saved_inputs, key=lambda sa: str(sa.nctype.name)):
        save_var(var, is_output=False)
    for var in sorted(info.all_saved_outputs, key=lambda sa: str(sa.nctype.name)):
        save_var(var, is_output=True)

    # lock the mutex when we release variables and in Node::apply to protect thread safety
    # see Note [Thread Safety on Autograd Node]
    if len(release_variables) > 0:
        thread_lock = "std::lock_guard<std::mutex> lock(mutex_);"
    else:
        thread_lock = ""

    if uses_retain_variables(info):
        apply_functional_args.append("retain_variables")
        apply_functional_args_ref_types.append("bool")
        will_release_variables = WILL_RELEASE_VARIABLES.substitute()
    else:
        will_release_variables = ""

    body: list[str] = []

    if uses_single_grad(info):
        body.append("const auto& grad = grads[0];")
    else:
        # Generate aliases for gradients named for returned values.
        body.extend(
            f"const auto& {name} = grads[{info.available_named_gradients.index(name)}];"
            for name in sorted(info.used_named_gradients)
        )

    def emit_derivative(
        derivative: Derivative,
        args_with_derivatives: Sequence[Binding],
    ) -> tuple[bool, str]:
        formula = derivative.formula
        var_names = derivative.var_names

        if len(var_names) == 1:
            checks_any_grad_defined = False
            if "not_implemented" not in formula:
                matching_args = [
                    arg for arg in args_with_derivatives if arg.name == var_names[0]
                ]
                if len(matching_args) == 1:
                    # We can add undefined grad support if the input variable is a Tensor
                    arg = matching_args[0]
                    if isinstance(arg.argument, Argument) and str(
                        arg.argument.type
                    ) in ("Tensor", "Tensor?"):
                        formula = "any_grad_defined ? (" + formula + ") : Tensor()"
                        checks_any_grad_defined = True
            if info.name.startswith("_foreach_"):
                derivative_template = DERIVATIVE_SINGLE_FOREACH
            else:
                derivative_template = DERIVATIVE_SINGLE
            return (
                checks_any_grad_defined,
                derivative_template.substitute(
                    name=var_names[0],
                    derivative=formula,
                    idx=input_name_to_idx[var_names[0]],
                ),
            )

        else:
            if "grad_input_mask" in formula:
                masks = [
                    f"needs_input_grad[{input_name_to_idx[name]}],"
                    for name in var_names
                ]
                grad_input_mask = GRAD_INPUT_MASK.substitute(
                    n=len(var_names), masks=masks
                )
            else:
                grad_input_mask = ""
            needs_input_grad = [
                f"needs_input_grad[{input_name_to_idx[name]}]" for name in var_names
            ]
            needs_input_grad = " || ".join(needs_input_grad)
            copy_ranges: list[str] = []
            for i, n in enumerate(var_names):
                copy_ranges.append(
                    DERIVATIVE_MULTI_COPY_RANGE.substitute(
                        name=n, i=i, idx=input_name_to_idx[n]
                    )
                )
            return False, DERIVATIVE_MULTI.substitute(
                needs_input_grad=needs_input_grad,
                copy_ranges=copy_ranges,
                derivative=formula,
                grad_input_mask=grad_input_mask,
            )

    masks = []

    need_any_grad_defined_var = False
    for derivative in info.derivatives:
        checks_any_grad_defined, derivative_text = emit_derivative(
            derivative, info.args_with_derivatives
        )
        body.append(derivative_text)
        need_any_grad_defined_var |= checks_any_grad_defined

    for name in input_name_to_idx:
        masks.append(f"task_should_compute_output({{ {name}_ix }}),")

    # Since single-output derivative formulas need to check if grads are
    # defined, only perform the check once, before all the formulas
    if need_any_grad_defined_var:
        body.insert(
            -len(info.derivatives),
            "bool any_grad_defined = any_variable_defined(grads);",
        )

    if info.name in UNTRACEABLE_FUNCTIONS:
        superclass = "Node"
    else:
        superclass = "TraceableFunction"

    all_getsetdef_structs = (
        ",\n".join(py_getsetdef_structs) + "," if len(py_getsetdef_structs) != 0 else ""
    )
    all_getter_definitions = "\n".join(getter_definitions)

    compute_needs_input_grad = COMPUTE_NEEDS_INPUT_GRAD.substitute(
        n=len(masks), compute_index_ranges=compute_index_ranges, masks=masks
    )
    apply_functional_args_signature = [
        f"{T} {x}"
        for T, x in zip(apply_functional_args_ref_types, apply_functional_args)
    ]
    get_packed_args = "\n".join(
        f"packed_args.pack({name});" for name in apply_functional_args
    )
    unpack_ivalues = []
    for typ, name in zip(apply_functional_args_ref_types, apply_functional_args):
        typ = typ.removesuffix("&")
        # pyrefly: ignore [bad-argument-type]
        unpack_ivalues.append(f"auto {name} = packed_args.unpack<{typ}>();")

    schema_args = [f"std::array<bool, {len(input_name_to_idx)}>"]
    for typ in apply_functional_args_ref_types:
        typ = typ.removesuffix("&")
        typ = typ.removeprefix("const")
        schema_args.append(typ.strip())
    compute_schema = ["std::vector<at::TypePtr> schema = {"]
    for schema_arg in schema_args:
        compute_schema.append(
            f"  torch::dynamo::autograd::IValuePacker<{schema_arg}>::packed_type(),"
        )
    compute_schema.append("};")

    return template.substitute(
        unpacks="\n".join(unpack),
        op=info.op,
        compute_schema="\n".join(compute_schema),
        apply_functional_args=apply_functional_args,
        apply_functional_args_signature=apply_functional_args_signature,
        compute_needs_input_grad=compute_needs_input_grad,
        num_inputs=len(input_name_to_idx),
        unpack_ivalues="\n".join(unpack_ivalues),
        compute_index_ranges=compute_index_ranges,
        saved_variables=saved_variables,
        release_variables=release_variables,
        saved_list_sizes=saved_list_sizes,
        asserts=asserts,
        thread_lock=thread_lock,
        will_release_variables=will_release_variables,
        body=body,
        superclass=superclass,
        all_getter_definitions=all_getter_definitions,
        all_getsetdef_structs=all_getsetdef_structs,
        compiled_args=compiled_args,
        apply_with_saved_before=apply_with_saved_before,
        apply_with_saved_after=apply_with_saved_after,
        get_packed_args=get_packed_args,
    )


def process_function(f: NativeFunction) -> str | None:
    name = cpp.name(f.func)
    has_tensor_options = python.has_tensor_options(f)
    is_factory = has_tensor_options or name.endswith("_like")

    if Variant.function not in f.variants or not is_factory:
        return None

    cpp_sigs = CppSignatureGroup.from_native_function(f, method=False)
    sigs = [cpp_sigs.signature]
    if cpp_sigs.symint_signature is not None:
        sigs.append(cpp_sigs.symint_signature)
    r = ""
    for sig in sigs:
        formals: list[str] = []
        exprs: list[str] = []
        requires_grad = "false"
        for arg in sig.arguments():
            qualified_type = fully_qualified_type(arg.type)
            if arg.default:
                formals.append(f"{qualified_type} {arg.name} = {arg.default}")
            else:
                formals.append(f"{qualified_type} {arg.name}")

            if isinstance(arg.argument, TensorOptionsArguments):
                # note: we remove the requires_grad setting from the TensorOptions because
                # it is ignored anyways (and we actually have an assertion that it isn't set
                # which would fail otherwise). We handle requires_grad explicitly here
                # instead of passing it through to the kernel.
                exprs.append(
                    f"at::TensorOptions({arg.name}).requires_grad(::std::nullopt)"
                )
                # Manually set the requires_grad bit on the result tensor.
                requires_grad = f"{arg.name}.requires_grad()"
            else:
                exprs.append(arg.name)

        r += f"""\
inline at::Tensor {sig.name()}({", ".join(formals)}) {{
  at::AutoDispatchBelowADInplaceOrView guard;
  return autograd::make_variable(at::{sig.name()}({", ".join(exprs)}), /*requires_grad=*/{requires_grad});
}}
"""
    return r


def process_function(fn: NativeFunction, template: CodeTemplate) -> str:
    bindings = extract_bindings(fn)
    non_self_bindings = [b for b in bindings if b.name != "self"]

    non_self_args = fn.func.arguments.flat_all[1:]
    non_self_value_bindings = [
        dispatcher.argument(a, remove_non_owning_ref_types=True) for a in non_self_args
    ]

    # Generate constructor / clone args for the generated struct.
    constructor_args = [b.defn() for b in non_self_bindings]
    clone_args = [b.name for b in non_self_bindings]

    # Generate state variable declarations for the generated struct.
    state_variables = [
        f"{remove_const_ref(b).defn()};" for b in non_self_value_bindings
    ]

    # Generate initializer list expressions for the generated struct.
    # allow_expensive_conversions=True because we need to store e.g. SymIntArrayRefs as
    # vector<SymInt>s.
    init_exprs = translate(
        non_self_bindings, non_self_value_bindings, allow_expensive_conversions=True
    )
    initializers = []
    for b, init_expr in zip(non_self_bindings, init_exprs):
        name = b.nctype.name
        if not isinstance(name, str):
            raise AssertionError(f"Expected name to be str, got {type(name)}")
        initializers.append(f"{name}({init_expr.expr})")

    # Generate call to underlying view op
    call_input_name = "input_base"
    op_call_args = [call_input_name, *(b.name for b in non_self_bindings)]
    op_call = CALL_DISPATCH.substitute(
        unambiguous_name=fn.func.name.unambiguous_name(),
        unpacked_args=op_call_args,
    )

    # Multi-output views additionally require a view_idx for disambiguation.
    if returns_multi_tensor(fn):
        view_idx_name = "view_idx"
        view_idx_typename = "int64_t"
        view_idx_decl = f"{view_idx_typename} {view_idx_name}"
        constructor_args.append(view_idx_decl)
        clone_args.append(view_idx_name)
        state_variables.append(f"{view_idx_decl};")
        initializers.append(f"{view_idx_name}({view_idx_name})")
        op_call += f"[{view_idx_name}]"

    # Generate initializer list for the generated struct.
    initializer_list = f": {', '.join(initializers)}" if len(initializers) > 0 else ""

    # Generate getter / setter logic for any symints.
    symint_bindings = [
        b
        for b in non_self_bindings
        if isinstance(b.argument, Argument) and b.argument.type.is_symint_like()
    ]
    symints_vec_type = NamedCType("symints", VectorCType(BaseCType(SymIntT)))
    get_symints, set_symints, num_symints = generate_state_getter_setter(
        symint_bindings, symints_vec_type
    )

    # Generate getter / setter logic for any tensors.
    tensor_bindings = [
        b
        for b in non_self_bindings
        if isinstance(b.argument, Argument) and b.argument.type.is_tensor_like()
    ]
    tensors_vec_type = NamedCType("tensors", VectorCType(BaseCType(tensorT)))
    get_tensors, set_tensors, num_tensors = generate_state_getter_setter(
        tensor_bindings, tensors_vec_type
    )

    return template.substitute(
        op=view_func_name(fn),
        uppercase_op=view_func_name(fn, camel_case=False).upper(),
        superclass="torch::autograd::ViewFunc",
        initializer_list=initializer_list,
        state=state_variables,
        constructor_args=constructor_args,
        clone_args=clone_args,
        symints_vec=symints_vec_type.name,
        get_symints=get_symints,
        set_symints=set_symints,
        num_symints=num_symints,
        tensors_vec=tensors_vec_type.name,
        get_tensors=get_tensors,
        set_tensors=set_tensors,
        num_tensors=num_tensors,
        call_input_name=call_input_name,
        op_call=op_call,
    )

