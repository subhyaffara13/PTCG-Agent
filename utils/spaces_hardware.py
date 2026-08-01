
def spaces_hardware(token: TokenOpt = None) -> None:
    """List available hardware options for Spaces."""
    api = get_hf_api(token=token)
    hardware_list = api.list_spaces_hardware()
    items = []
    for hw in hardware_list:
        accelerator = (
            f"{hw.accelerator.quantity}x {hw.accelerator.model} ({hw.accelerator.vram})" if hw.accelerator else None
        )
        cost_min = f"${hw.unit_cost_usd:.4f}" if hw.unit_cost_usd else "free"
        cost_hour = f"${hw.unit_cost_usd * 60:.2f}" if hw.unit_cost_usd else "free"
        items.append(
            {
                "name": hw.name,
                "pretty name": hw.pretty_name,
                "cpu": hw.cpu,
                "ram": hw.ram,
                "accelerator": accelerator,
                "cost/min": cost_min,
                "cost/hour": cost_hour,
            }
        )
    out.table(items)
    out.hint("Use `hf spaces settings <space_id> --hardware <name>` to request hardware for a Space.")

