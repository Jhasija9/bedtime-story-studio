"""
Shared helpers for running the LangGraph story workflow from both CLI and Streamlit front-ends.
"""
from functools import lru_cache
from typing import Optional, Tuple

from dotenv import load_dotenv

from graph.graph import build_graph
from graph.state import StoryState

# Ensure environment variables are loaded once for any entry point.
load_dotenv()


@lru_cache(maxsize=1)
def _get_graph():
    """Build and cache the compiled LangGraph instance."""
    return build_graph()


def generate_story(
    user_input: str,
    age: int,
    tone: Optional[str] = None,
    max_iterations: int = 3,
    previous_state: Optional[StoryState] = None,
    feedback_request: Optional[str] = None,
) -> Tuple[StoryState, Optional[str]]:
    """
    Run the LangGraph workflow and return the final state and best-available story text.
    """
    initial_state = StoryState(
        user_input=user_input,
        age=age,
        tone=tone,
        max_iterations=max_iterations,
    )

    if previous_state:
        initial_state.refined_brief = previous_state.refined_brief
        initial_state.story = previous_state.final_story or previous_state.story

    if feedback_request:
        initial_state.feedback_request = feedback_request

    graph = _get_graph()
    result = graph.invoke(initial_state)

    # LangGraph returns dicts by default; coerce back into StoryState for consistent access.
    final_state = result if isinstance(result, StoryState) else StoryState(**result)
    final_story = final_state.final_story or final_state.story
    return final_state, final_story
