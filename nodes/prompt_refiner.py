"""
PromptRefiner node for LangGraph.
Converts raw user input into structured JSON brief.
"""
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import StoryState
from utils.prompts import PROMPT_REFINER_SYSTEM
from utils.json_parser import parse_strict_json
from utils.llm_factory import get_llm
from typing import Dict


def prompt_refiner_node(state: StoryState) -> Dict:
    """
    Refines user input into structured JSON brief.
    
    Args:
        state: Current StoryState
        
    Returns:
        Dictionary with refined_brief update
    """
    # Extract user input from state
    user_input = state.user_input
    age = state.age
    tone = state.tone
    
    # Build user prompt
    user_prompt = f"Raw topic: \"{user_input}\"\nAge (5–10): {age}"
    if tone:
        user_prompt += f"\nPreferred tone (optional): \"{tone}\""
    
    # Initialize LLM (flexible: Gemini or OpenAI)
    llm = get_llm(temperature=0.3)
    
    # Call LLM
    messages = [
        SystemMessage(content=PROMPT_REFINER_SYSTEM),
        HumanMessage(content=user_prompt)
    ]
    response = llm.invoke(messages)
    
    # Parse JSON response
    try:
        refined_brief = parse_strict_json(response.content)
        print(f"jjjjjjDEBUG: Refined brief: {refined_brief}")
    except (ValueError, Exception) as e:
        # If parsing fails, retry once with stricter prompt
        retry_prompt = user_prompt + "\n\nReturn STRICT JSON only."
        retry_response = llm.invoke([
            SystemMessage(content=PROMPT_REFINER_SYSTEM),
            HumanMessage(content=retry_prompt)
        ])
        refined_brief = parse_strict_json(retry_response.content)
    
    return {"refined_brief": refined_brief}

