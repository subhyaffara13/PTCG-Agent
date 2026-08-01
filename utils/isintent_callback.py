
def isintent_callback(var):
    return 'callback' in var.get('intent', [])

