"""
Configuration settings for SOL Quiz Generator
"""

# OpenAI Settings
OPENAI_MODEL = "gpt-4o-mini"  # Cost-effective model, can upgrade to "gpt-4o" for better results
OPENAI_TEMPERATURE_ASSESSMENT = 0.3  # Lower temperature for more consistent feasibility assessments
OPENAI_TEMPERATURE_GENERATION = 0.7  # Higher temperature for more creative question generation

# Question Generation Settings
DEFAULT_QUESTIONS_PER_STANDARD = 3
MAX_RETRIES = 3  # Number of retries for failed API calls

# Question Type Distribution (when auto-selecting)
# These weights determine the probability of each question type
QUESTION_TYPE_WEIGHTS = {
    "multiple_choice": 0.4,
    "fill_in_blank": 0.3,
    "true_false": 0.2,
    "short_answer": 0.1
}

# Grade Level Configuration
# Adjust vocabulary complexity and sentence structure
GRADE_LEVEL_CONFIG = {
    "K": {"max_sentence_length": 8, "complexity": "very_simple"},
    "Grade 1": {"max_sentence_length": 10, "complexity": "simple"},
    "Grade 2": {"max_sentence_length": 12, "complexity": "simple"},
    "Grade 3": {"max_sentence_length": 15, "complexity": "moderate"},
    "Grade 4": {"max_sentence_length": 18, "complexity": "moderate"},
    "Grade 5": {"max_sentence_length": 20, "complexity": "moderate"},
    "Grade 6": {"max_sentence_length": 22, "complexity": "moderate"},
    "Grade 7": {"max_sentence_length": 25, "complexity": "advanced"},
    "Grade 8": {"max_sentence_length": 25, "complexity": "advanced"},
    "High School": {"max_sentence_length": 30, "complexity": "advanced"}
}

# Output Settings
DEFAULT_OUTPUT_FILE = "generated_questions.json"
SAVE_ASSESSMENTS = True  # Whether to save feasibility assessments
INCLUDE_EXPLANATIONS = True  # Whether to include answer explanations
