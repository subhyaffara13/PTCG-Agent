
def force_serialization_as_bin_files():
    """Since we don't support saving with torch `.bin` files anymore, but still support loading them, we use this context
    to easily create the bin files and try to load them back"""
    try:
        # Monkey patch the method to save as bin files
        original_save = PreTrainedModel.save_pretrained

        def new_save(self, save_directory, *args, **kwargs):
            original_save(self, save_directory, *args, **kwargs)
            convert_all_safetensors_to_bins(save_directory)

        PreTrainedModel.save_pretrained = new_save

        yield
    finally:
        PreTrainedModel.save_pretrained = original_save

