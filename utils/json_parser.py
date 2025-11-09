"""
JSON parser for strict JSON extraction from LLM responses.
Slices first {...} block and parses with json.loads.
Retries once if parsing fails.
"""
import json
import re
from typing import Dict, Any, Optional


def parse_strict_json(text: str, retry_prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse strict JSON from text by extracting first {...} block.
    
    Args:
        text: Text containing JSON
        retry_prompt: Optional prompt to add if first attempt fails
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON cannot be parsed after retry
    """
    # Find first JSON object block {...}
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    
    if not match:
        # If no match found, try to find any {...} pattern more broadly
        match = re.search(r'\{.*\}', text, re.DOTALL)
    
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If parsing fails and we have a retry prompt, try adding it
            if retry_prompt:
                # This would be used if we need to retry with LLM
                raise ValueError(f"JSON parsing failed. Retry with: {retry_prompt}")
            raise ValueError("JSON parsing failed")
    
    raise ValueError("No JSON object found in text")

