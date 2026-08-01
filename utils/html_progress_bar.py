
def html_progress_bar(value, total, prefix, label, width=300):
    # docstyle-ignore
    return f"""
    <div>
      {prefix}
      <progress value='{value}' max='{total}' style='width:{width}px; height:20px; vertical-align: middle;'></progress>
      {label}
    </div>
    """

