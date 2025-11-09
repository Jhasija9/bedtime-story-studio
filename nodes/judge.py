"""
Judge node for LangGraph.
Evaluates story on 6 dimensions and returns STRICT JSON only (no Chain-of-Thought).
"""
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import StoryState
from utils.prompts import JUDGE_SYSTEM
from utils.json_parser import parse_strict_json
from utils.llm_factory import get_llm
from typing import Dict


def judge_node(state: StoryState) -> Dict:
    """
    Judges story quality on 6 dimensions.
    
    Args:
        state: Current StoryState
        
    Returns:
        Dictionary with judge_result and updated iteration_count
    """
    if not state.story:
        raise ValueError("story is required for judging")
    
    # Get age from refined_brief or default
    age = 7
    if state.refined_brief:
        age = state.refined_brief.get("age", 7)
    
    # Initialize LLM (flexible: Gemini or OpenAI)
    llm = get_llm(temperature=0.1)  # Lower temperature for evaluation
    
    # Build user prompt
    user_prompt = f"""Please evaluate the following story for ages {age} and return JSON per the schema.

{state.story}"""
    
    # Call LLM
    messages = [
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=user_prompt)
    ]
    response = llm.invoke(messages)
    print(f"judge DEBUG: Judge response: {response.content}")
    
    # Parse JSON response
    try:
        judge_result = parse_strict_json(response.content)
        print(f"judge DEBUG: Judge result: {judge_result}")
    except (ValueError, Exception) as e:
        # If parsing fails, retry once with stricter prompt
        retry_prompt = user_prompt + "\n\nReturn STRICT JSON only."
        retry_response = llm.invoke([
            SystemMessage(content=JUDGE_SYSTEM),
            HumanMessage(content=retry_prompt)
        ])
        judge_result = parse_strict_json(retry_response.content)
    
    # Update iteration count
    iteration_count = state.iteration_count + 1
    
    return {
        "judge_result": judge_result,
        "iteration_count": iteration_count
    }

