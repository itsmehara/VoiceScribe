import ollama


def generate_summary(transcript_text: str) -> str:
    prompt = f"""
    Analyze the meeting transcript and generate a structured summary.

    Rules:
    - Use only information present in the transcript.
    - Do not invent facts, decisions, actions, or participants.
    - Use concise bullet points.
    - Prioritize Key Points over all other sections.
    - Generate up to 50 total bullet points across all sections.
    - Purpose: maximum 5 points.
    - Key Points: maximum 20 points.
    - Decisions: maximum 20 points.
    - Action Items: maximum 20 points.
    - Next Steps: maximum 20 points.
    - If a section has insufficient information, redistribute the remaining points to other sections, giving highest priority to Key Points.
    - Omit empty sections.
    - Focus on technical discussions, important observations, decisions, commitments, blockers, risks, and follow-up activities.
    
    Return in the following format:
    
    ## Purpose

    ## Key Points
    
    ## Decisions
    
    ## Action Items
    
    ## Next Steps
    
    Transcript:
    
    {transcript_text}
    """

    response = ollama.chat(
        model="qwen3:4b",
        options={"temperature": 0},
        messages=[{"role": "user", "content": prompt}]
    )
 
    return response["message"]["content"]
