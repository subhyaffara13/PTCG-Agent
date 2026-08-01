
def _remove_duplicates_and_none(qconfig_list: list[QConfigAny]) -> None:
    to_remove = []
    for index, cur_qconfig in enumerate(qconfig_list):
        if cur_qconfig is None:
            to_remove.append(index)
            break
        for checked_qconfig in qconfig_list[:index]:
            if torch.ao.quantization.qconfig_equals(cur_qconfig, checked_qconfig):
                to_remove.append(index)
                break
    for index in to_remove[::-1]:
        qconfig_list.pop(index)

