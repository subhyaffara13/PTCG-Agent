
def get_class_similarity(class_distance_type, cls_feature, class_proj):
    logit_scale = torch.tensor(1 / 0.07).log()
    if class_distance_type == "cosine":
        class_logits = _cosine_similarity_scaled(cls_feature, class_proj, logit_scale)
    elif class_distance_type == "dot":
        class_logits = torch.bmm(cls_feature, class_proj)
    else:
        raise Exception(f"Unknown class_distance_type {class_distance_type}")
    return class_logits

