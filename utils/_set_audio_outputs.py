
def _set_audio_outputs(span: "Span", response_obj, audio_attrs, span_attrs):
    audio = response_obj.get("audio", [])
    for i, audio_item in enumerate(audio):
        audio_url = audio_item.get("url")
        if audio_url is None and audio_item.get("b64_json"):
            audio_url = f"data:audio/wav;base64,{audio_item.get('b64_json')}"

        if audio_url:
            if i == 0:
                safe_set_attribute(span, span_attrs.OUTPUT_VALUE, audio_url)
            safe_set_attribute(span, f"{audio_attrs.AUDIO_URL}.{i}", audio_url)

        audio_mime = audio_item.get("mime_type")
        if audio_mime:
            safe_set_attribute(span, f"{audio_attrs.AUDIO_MIME_TYPE}.{i}", audio_mime)

        audio_transcript = audio_item.get("transcript")
        if audio_transcript:
            safe_set_attribute(
                span, f"{audio_attrs.AUDIO_TRANSCRIPT}.{i}", audio_transcript
            )

