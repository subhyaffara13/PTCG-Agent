
def autoname_modules(model):
    for name, module in model.named_modules():
        module.name = name

