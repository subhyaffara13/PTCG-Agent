
def vt_getitem(
    tx: "InstructionTranslator",
    obj: VariableTracker,
    key: VariableTracker,
) -> VariableTracker:
    """CPython's PyObject_GetItem — dispatch to the type's mp_subscript/sq_item.

    PyObject_GetItem: https://github.com/python/cpython/blob/62a6e898e01/Objects/abstract.c#L155-L206

    CPython checks three branches in order:
      1. tp_as_mapping->mp_subscript  (L161-166)
      2. tp_as_sequence->sq_item      (L168-181) — only if key passes _PyIndex_Check
      3. PyType_Check(o)              (L183-203) — type[int] → GenericAlias/__class_getitem__

    Branch 1 is the common path (list, tuple, dict, range all have mp_subscript).
    TODO(follow-up): use has_slot(map_slots, PyMappingSlots.MP_SUBSCRIPT) to gate
    Branch 1 and has_slot(seq_slots, PySequenceSlots.SQ_ITEM) to gate Branch 2,
    matching CPython's dispatch order.
    TODO(follow-up): Branch 2 (sq_item) for C extension types that only have
    tp_as_sequence (e.g. deque — Modules/_collectionsmodule.c:1888).
    Branch 3 is handled by TypingVariable.mp_subscript_impl for typing module types
    and by BuiltinVariable for builtin types like list[int].

    Types that work via constant fold fallback (no dedicated mp_subscript_impl):
    TODO(follow-up): str (unicode_subscript, Objects/unicodeobject.c:13809)
    TODO(follow-up): bytes (bytes_subscript, Objects/bytesobject.c)
    """
    return obj.mp_subscript_impl(tx, key)

