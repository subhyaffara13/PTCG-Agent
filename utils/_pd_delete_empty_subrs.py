
def _pd_delete_empty_subrs(private_dict):
    if hasattr(private_dict, "Subrs") and not private_dict.Subrs:
        if "Subrs" in private_dict.rawDict:
            del private_dict.rawDict["Subrs"]
        del private_dict.Subrs

