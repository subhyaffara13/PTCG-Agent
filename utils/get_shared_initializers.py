
def get_shared_initializers(encoder_model: ModelProto, decoder_model: ModelProto):
    encoder = OnnxModel(encoder_model)
    decoder = OnnxModel(decoder_model)
    encoder.add_prefix_to_names("e_")
    decoder.add_prefix_to_names("d_")
    signature_cache1, signature_cache2 = {}, {}
    encoder.remove_duplicated_initializer(signature_cache1)
    decoder.remove_duplicated_initializer(signature_cache2)
    initializers = remove_shared_initializers(
        decoder.model.graph,
        encoder.model.graph,
        shared_prefix="s_",
        signature_cache1=signature_cache1,
        signature_cache2=signature_cache2,
    )
    return initializers

