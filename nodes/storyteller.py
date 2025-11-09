"""
Storyteller node for LangGraph.
Generates stories in two modes: Initial (from brief) and Revision (from edit instructions).
"""
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import StoryState
from utils.prompts import STORYTELLER_SYSTEM
from utils.llm_factory import get_llm
from typing import Dict
import json


def storyteller_node(state: StoryState) -> Dict:
    """
    Generates or revises story based on state.
    
    Two modes:
    1. Initial: Uses refined_brief to generate story
    2. Revision: Uses story + edit_instructions to revise (lower temperature)
    
    Args:
        state: Current StoryState
        
    Returns:
        Dictionary with story update
    """
    revision_instructions = None
    if state.feedback_request and state.story:
        revision_instructions = state.feedback_request
    elif state.judge_result and state.story:
        revision_instructions = state.judge_result.get("edit_instructions", "")

    # Check if this is a revision
    if revision_instructions:
        # Revision mode: apply edit instructions
        edit_instructions = revision_instructions or ""
        temperature = 0.3  # Lower temperature for revisions
        
        llm = get_llm(temperature=temperature)
        
        source_label = "Reader feedback" if state.feedback_request else "Edit instructions"
        user_prompt = f"""Revise the following story according to these {source_label.lower()}. Keep it safe, age-fit, and 250–400 words.

{source_label}:

{edit_instructions}

Original story:

{state.story}

Output only the revised story text."""
    else:
        # Initial mode: use refined_brief
        if not state.refined_brief:
            raise ValueError("refined_brief is required for initial story generation")
        
        llm = get_llm(temperature=0.7)  # Default temperature for initial
        
        brief_json = json.dumps(state.refined_brief, indent=2)
        user_prompt = f"""Create a children's story using this brief:

Brief (JSON):

{brief_json}

Guidance:

Follow must strictly.

Aim to satisfy should.

Use can if it helps engagement without breaking safety/length.

Output only the story text."""
    
    # Call LLM
    messages = [
        SystemMessage(content=STORYTELLER_SYSTEM),
        HumanMessage(content=user_prompt)
    ]
    response = llm.invoke(messages)
    
    story_text = response.content.strip()
    
    return {"story": story_text}
