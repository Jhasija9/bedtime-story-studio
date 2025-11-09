"""
Configuration constants for the bedtime story generator.
Supports both OpenAI and Google Gemini models.
"""
import os

# Model configuration
# OpenAI model (used if OPENAI_API_KEY is set and GOOGLE_API_KEY is not)
MODEL_NAME = "gpt-3.5-turbo"

# Gemini model (used if GOOGLE_API_KEY is set)
# Allow override via GEMINI_MODEL env so users can pick a model their project has access to.
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)

# Provider selection
# STORY_LLM_PROVIDER can be: "openai", "gemini", or "auto" (defaults to "auto").
# We default to OpenAI because the assignment requires gpt-3.5 unless the user
# explicitly opts into Gemini.
LLM_PROVIDER = os.getenv("STORY_LLM_PROVIDER", "auto").strip().lower()

# Thresholds for quality control
OVERALL_THRESHOLD = 8.0  # Overall score must be >= 8.0 to pass
DIMENSION_THRESHOLD = 7.0  # Each dimension must be >= 7.0 to pass

# Iteration limits
MAX_ITERATIONS = 3  # Configurable (2-3)

# Story constraints
MIN_WORDS = 200  # 250 - 20% tolerance
MAX_WORDS = 480  # 400 + 20% tolerance
TARGET_WORDS_MIN = 250
TARGET_WORDS_MAX = 400

# Banned terms for safety check
BANNED_TERMS = ["gun", "knife", "kill", "die", "alcohol", "drugs", "blood", "adult themes", "violence","Porn","Sexual content"]
