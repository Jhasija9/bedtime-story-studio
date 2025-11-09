"""
Safety Check node for LangGraph.
Local checks only (no LLM): word count and banned terms.
"""
from graph.state import StoryState
from utils.config import MIN_WORDS, MAX_WORDS, BANNED_TERMS
from typing import Dict, List


def safety_check_node(state: StoryState) -> Dict:
    """
    Performs local safety checks on the story.
    
    Checks:
    1. Word count: ~250-400 words (200-480 with tolerance)
    2. Banned terms: gun, knife, kill, die, alcohol, drugs, blood, adult themes
    
    Args:
        state: Current StoryState
        
    Returns:
        Dictionary with safety_notes update (None if passes, string if fails)
    """
    if not state.story:
        return {"safety_notes": "No story to check"}
    
    violations: List[str] = []
    
    # Check word count
    word_count = len(state.story.split())
    if word_count < MIN_WORDS:
        violations.append(f"Story too short: {word_count} words (minimum {MIN_WORDS})")
    elif word_count > MAX_WORDS:
        violations.append(f"Story too long: {word_count} words (maximum {MAX_WORDS})")
    
    # Check banned terms (case-insensitive)
    story_lower = state.story.lower()
    found_terms = []
    for term in BANNED_TERMS:
        if term.lower() in story_lower:
            found_terms.append(term)
    
    if found_terms:
        violations.append(f"Banned terms found: {', '.join(found_terms)}")
    
    # Set safety_notes
    if violations:
        safety_notes = "; ".join(violations)
    else:
        safety_notes = None
    print(f"hhhhhsafety_check DEBUG: Safety notes: {safety_notes}")
    
    return {"safety_notes": safety_notes}

