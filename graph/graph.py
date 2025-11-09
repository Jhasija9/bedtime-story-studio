"""
LangGraph StateGraph definition for bedtime story generator.
Reference: https://docs.langchain.com/oss/python/langgraph/overview
"""
from langgraph.graph import StateGraph, START, END
from graph.state import StoryState
from nodes.prompt_refiner import prompt_refiner_node
from nodes.storyteller import storyteller_node
from nodes.judge import judge_node
from nodes.safety_check import safety_check_node
from nodes.finalize import finalize_node
from utils.config import OVERALL_THRESHOLD, DIMENSION_THRESHOLD, MAX_ITERATIONS


def check_scores(state: StoryState) -> str:
    """
    Conditional function for LangGraph routing.
    
    Stop condition: overall >= 8.0 AND all dimensions >= 7.0 AND safety_notes is None
    Continue condition: (overall < 8.0 OR any dim < 7.0 OR safety_notes not None) AND iteration_count < max_iterations
    
    Args:
        state: Current StoryState
        
    Returns:
        "revise" or "end" string for LangGraph routing
    """
    # Check iteration limit
    if state.iteration_count >= state.max_iterations:
        return "end"
    
    # Check if judge_result exists
    if not state.judge_result:
        return "end"  # No judge result, end
    
    # Check overall score
    overall = state.judge_result.get("overall", 0.0)
    if overall < OVERALL_THRESHOLD:
        return "revise"
    
    # Check all dimensions
    dimensions = state.judge_result.get("dimensions", [])
    for dim in dimensions:
        score = dim.get("score", 0.0)
        if score < DIMENSION_THRESHOLD:
            return "revise"
    
    # Check safety notes
    if state.safety_notes is not None and state.safety_notes != "":
        return "revise"
    
    # All conditions met, end
    return "end"


def build_graph():
    """
    Builds and compiles the LangGraph StateGraph.
    
    Returns:
        Compiled LangGraph
    """
    # Create StateGraph following LangGraph documentation
    # Reference: https://docs.langchain.com/oss/python/langgraph/overview
    graph = StateGraph(StoryState)
    
    # Add nodes
    graph.add_node("prompt_refiner", prompt_refiner_node)
    graph.add_node("storyteller", storyteller_node)
    graph.add_node("judge", judge_node)
    graph.add_node("safety_check", safety_check_node)
    graph.add_node("finalize", finalize_node)
    
    # Add edges
    graph.add_edge(START, "prompt_refiner")
    graph.add_edge("prompt_refiner", "storyteller")
    graph.add_edge("storyteller", "judge")
    graph.add_edge("judge", "safety_check")
    
    # Conditional edge (LangGraph feature)
    graph.add_conditional_edges(
        "safety_check",
        check_scores,  # Function that returns "revise" or "end"
        {
            "revise": "storyteller",
            "end": "finalize"
        }
    )
    
    # Finalize to END
    graph.add_edge("finalize", END)
    
    # Compile graph
    return graph.compile()

