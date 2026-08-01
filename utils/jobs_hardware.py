
def jobs_hardware() -> None:
    """List available hardware options for Jobs"""
    api = get_hf_api()
    hardware_list = api.list_jobs_hardware()
    items = []
    for hw in hardware_list:
        accelerator_info = ""
        if hw.accelerator:
            accelerator_info = f"{hw.accelerator.quantity}x {hw.accelerator.model} ({hw.accelerator.vram})"
        cost_min = f"${hw.unit_cost_usd:.4f}" if hw.unit_cost_usd else "free"
        cost_hour = f"${hw.unit_cost_usd * 60:.2f}" if hw.unit_cost_usd else "free"
        items.append(
            {
                "name": hw.name,
                "pretty name": hw.pretty_name,
                "cpu": hw.cpu,
                "ram": hw.ram,
                "storage": hw.ephemeral_storage,
                "accelerator": accelerator_info,
                "cost/min": cost_min,
                "cost/hour": cost_hour,
            }
        )
    out.table(items)
    out.hint("Use `hf jobs run --flavor <name> ...` to request a specific hardware flavor.")

