"""
Finalize node to set final_story in state when workflow ends.
"""
from graph.state import StoryState
from typing import Dict


def finalize_node(state: StoryState) -> Dict:
    """
    Sets final_story when workflow completes.
    
    Args:
        state: Current StoryState
        
    Returns:
        Dictionary with final_story update
    """
    return {"final_story": state.story}

