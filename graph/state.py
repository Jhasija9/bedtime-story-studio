"""
State definition for LangGraph StoryState using Pydantic.
Reference: https://docs.langchain.com/oss/python/langgraph/overview
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class StoryState(BaseModel):
    """State schema for the bedtime story generator workflow."""
    user_input: str = ""  # Raw user input
    age: int = 7  # Target age (5-10)
    tone: Optional[str] = None  # Optional tone preference
    refined_brief: Optional[Dict[str, Any]] = None  # JSON from PromptRefiner
    story: Optional[str] = None  # Generated story text
    judge_result: Optional[Dict[str, Any]] = None  # JSON from Judge
    safety_notes: Optional[str] = None  # Safety warnings (None if passes)
    iteration_count: int = 0  # Current iteration number
    max_iterations: int = 3  # Maximum iterations (default 3, configurable 2-3)
    final_story: Optional[str] = None  # Final story output
    feedback_request: Optional[str] = None  # User-provided revision instructions
    
    class Config:
        arbitrary_types_allowed = True
