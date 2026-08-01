
def max_batch(args):
    if args.max_batch_size:
        max_batch_size = args.max_batch_size
    else:
        do_classifier_free_guidance = args.guidance > 1.0
        batch_multiplier = 2 if do_classifier_free_guidance else 1
        max_batch_size = 32 // batch_multiplier
        if args.engine != "ORT_CUDA" and (args.build_dynamic_shape or args.height > 512 or args.width > 512):
            max_batch_size = 8 // batch_multiplier
    return max_batch_size

