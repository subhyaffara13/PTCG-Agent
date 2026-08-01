
def easy_class_getitem_inference(node, context: InferenceContext | None = None):
    # Here __class_getitem__ exists but is quite a mess to infer thus
    # put an easy inference tip
    func_to_add = extract_node(CLASS_GET_ITEM_TEMPLATE)
    node.locals["__class_getitem__"] = [func_to_add]

