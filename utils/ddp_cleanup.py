
def ddp_cleanup():
    dist.destroy_process_group()

