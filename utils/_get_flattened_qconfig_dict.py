
def _get_flattened_qconfig_dict(
    qconfig_mapping: QConfigMapping,
) -> dict[Callable | str, QConfigAny]:
    """flatten the global, object_type and module_name qconfig
    to the same qconfig_dict so that it can be used by
    propagate_qconfig_ function.
    "module_name_regex" is ignored for now since it's not supported
    in propagate_qconfig_, but it can be fixed later.

    For example:
    Input: {
      "": qconfig,
      "object_type": [
        (torch.add, qconfig)
      ],
      "module_name": [
        ("conv", qconfig)
      ]
    }

    Output: {
      "": qconfig,
      torch.add: qconfig,
      "conv": qconfig
    }
    """
    flattened: dict[Callable | str, QConfigAny] = {"": qconfig_mapping.global_qconfig}
    flattened.update(qconfig_mapping.object_type_qconfigs)
    flattened.update(qconfig_mapping.module_name_qconfigs)  # type: ignore[arg-type]
    return flattened

