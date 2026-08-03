import random
import time
from typing import Optional

def summarize_with_gemini(transcript: str, model_id: str = "gemini-3-pro-preview", max_retries: int = 10) -> Optional[GameAnalysis]:
    project = get_gcloud_project()
    client = None

    if project:
        print(f"Using Vertex AI with project: {project} (global)")
        client = genai.Client(vertexai=True, project=project, location="global")
    else:
        print("Error: GOOGLE_CLOUD_PROJECT not found. This script requires Vertex AI.")
        return None

    prompt = f"""
You are an expert commentator and analyst for the game of Werewolf (also known as Mafia).
I will provide you with a structured log of a game session.
Your task is to analyze the game and provide a detailed summary, highlighting the key moments, player performances, and strategy.

Here is the game transcript:
{transcript}

Please provide the analysis in the requested structured JSON format.
For 'excitement_score', consider the following rubric:
- Strategic Depth: Were there complex plays or counter-plays?
- Unpredictability: Were there twists or unexpected outcomes?
- Narrative Quality: Did a compelling story emerge?
- Humor: Was the dialogue funny, witty, or entertaining?
- Player Competence: Did players demonstrate high-level understanding?
- Pacing: Was the game tense throughout?
- Subjective Impression: Your personal enjoyment as a spectator (the "X-factor").
- Synergy: Did players demonstrate amazing teamwork or coordination (e.g. Wolf bussing, Village consolidation, Doctor/Seer sync)?

For 'dramatic_moments', identify specific key turns where the game shifted or excitement peaked.
For 'player_stats', assess them relative to high-level play.
"""

    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GameAnalysis,
                    temperature=0.5,
                )
            )
            
            # Check if response is valid
            if not response.parsed:
                 print("Error: Gemini response could not be parsed.")
                 # print(response.text) # Debugging
                 return None
            
            analysis = response.parsed
            
            # Recalculate excitement_score to be the strict average of rubric components
            # This ensures the score reflects all criteria including Humor
            r = analysis.entertainment_metrics.rubric
            rubric_values = [
                r.strategic_depth,
                r.unpredictability,
                r.narrative_quality,
                r.humor,
                r.player_competence,
                r.pacing,
                r.subjective_impression,
                r.synergy
            ]
            avg_score = sum(rubric_values) / len(rubric_values)
            analysis.entertainment_metrics.excitement_score = round(avg_score, 1)
            
            return analysis
                 
            return response.parsed

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "Resource has been exhausted" in error_str or "404" in error_str:
                # 404 might be transient model loading or actual missing model, but let's treat it as fatal or transient?
                # User had 404 earlier for invalid model, but 429 is the main target here.
                # Actually, 404 for model not found shouldn't be retried if it's static config error. 
                # Focusing on 429/Resource Exhausted.
                is_resource_exhausted = "429" in error_str or "Resource has been exhausted" in error_str
                
                if is_resource_exhausted and attempt < max_retries - 1:
                    sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                    print(f"Quota exceeded (429). Retrying in {sleep_time:.2f}s... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue
            
            print(f"Error calling Gemini API: {e}")
            return None
            
    return None

