import json
import sys
from typing import Any, Dict, List, Optional

def _stream_response(
    console: Console,
    client: ChatClient,
    model: str,
    messages: List[Dict[str, Any]],
    temperature: float,
    max_tokens: Optional[int],
) -> Optional[str]:
    """Stream the model response and return the complete content"""
    try:
        assistant_content = ""
        for chunk in client.completions_stream(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    assistant_content += content
                    console.print(content, end="")
                    sys.stdout.flush()

        console.print()  # Add newline after streaming
        return assistant_content if assistant_content else None

    except requests.exceptions.HTTPError as e:
        console.print(f"\n[red]Error: HTTP {e.response.status_code}[/red]")
        try:
            error_body = e.response.json()
            console.print(
                f"[red]{error_body.get('error', {}).get('message', 'Unknown error')}[/red]"
            )
        except json.JSONDecodeError:
            console.print(f"[red]{e.response.text}[/red]")
        return None
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        return None

