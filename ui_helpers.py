"""
Helper functions for the Streamlit UI
Utilities for data formatting, validation, and processing
"""

from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime


def format_standard_id(standard_id: str) -> str:
    """Format standard ID for display"""
    return standard_id.upper()


def get_feasibility_color(feasibility: str) -> str:
    """Get color code for feasibility status"""
    colors = {
        "feasible": "#28a745",
        "partially_feasible": "#ffc107",
        "not_feasible": "#dc3545"
    }
    return colors.get(feasibility, "#6c757d")


def get_difficulty_emoji(difficulty: str) -> str:
    """Get emoji for difficulty level"""
    emojis = {
        "easy": "🟢",
        "medium": "🟡",
        "hard": "🔴"
    }
    return emojis.get(difficulty.lower(), "⚪")


def validate_question(question: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate a question structure

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['question_text', 'correct_answer', 'question_type']

    for field in required_fields:
        if field not in question:
            return False, f"Missing required field: {field}"

    # Validate multiple choice questions have options
    if question['question_type'] == 'multiple_choice':
        if 'options' not in question or not question['options']:
            return False, "Multiple choice questions must have options"
        if len(question['options']) < 2:
            return False, "Multiple choice must have at least 2 options"
        if question['correct_answer'] not in question['options']:
            return False, "Correct answer must be in options list"

    return True, None


def calculate_statistics(questions_data: Dict) -> Dict:
    """
    Calculate statistics from questions data

    Returns:
        Dictionary with various statistics
    """
    stats = {
        'total_documents': 0,
        'total_standards': 0,
        'total_questions': 0,
        'by_type': {},
        'by_difficulty': {},
        'by_feasibility': {},
        'avg_questions_per_standard': 0
    }

    if not questions_data:
        return stats

    stats['total_documents'] = len(questions_data)

    for doc_data in questions_data.values():
        standards = doc_data.get('standards', [])
        stats['total_standards'] += len(standards)

        for std_data in standards:
            questions = std_data.get('questions', [])
            stats['total_questions'] += len(questions)

            # Count by type
            for q in questions:
                q_type = q.get('question_type', 'unknown')
                stats['by_type'][q_type] = stats['by_type'].get(q_type, 0) + 1

                # Count by difficulty
                difficulty = q.get('difficulty_level', 'unknown')
                stats['by_difficulty'][difficulty] = stats['by_difficulty'].get(difficulty, 0) + 1

            # Count by feasibility
            assessment = std_data.get('assessment', {})
            feasibility = assessment.get('feasibility', 'unknown')
            stats['by_feasibility'][feasibility] = stats['by_feasibility'].get(feasibility, 0) + 1

    if stats['total_standards'] > 0:
        stats['avg_questions_per_standard'] = stats['total_questions'] / stats['total_standards']

    return stats


def filter_questions(
    questions_data: Dict,
    question_types: Optional[List[str]] = None,
    difficulty_levels: Optional[List[str]] = None,
    feasibility: Optional[List[str]] = None
) -> Dict:
    """
    Filter questions based on criteria

    Args:
        questions_data: The questions data to filter
        question_types: List of question types to include
        difficulty_levels: List of difficulty levels to include
        feasibility: List of feasibility statuses to include

    Returns:
        Filtered questions data
    """
    filtered_data = {}

    for doc_key, doc_data in questions_data.items():
        filtered_standards = []

        for std_data in doc_data.get('standards', []):
            # Check feasibility filter
            if feasibility:
                assessment = std_data.get('assessment', {})
                if assessment.get('feasibility') not in feasibility:
                    continue

            # Filter questions
            filtered_questions = []
            for q in std_data.get('questions', []):
                # Check question type filter
                if question_types and q.get('question_type') not in question_types:
                    continue

                # Check difficulty filter
                if difficulty_levels and q.get('difficulty_level') not in difficulty_levels:
                    continue

                filtered_questions.append(q)

            # Only include standard if it has questions after filtering
            if filtered_questions:
                filtered_std = std_data.copy()
                filtered_std['questions'] = filtered_questions
                filtered_standards.append(filtered_std)

        # Only include document if it has standards after filtering
        if filtered_standards:
            filtered_doc = doc_data.copy()
            filtered_doc['standards'] = filtered_standards
            filtered_data[doc_key] = filtered_doc

    return filtered_data


def export_to_quiz_format(questions_data: Dict, format_type: str = "generic") -> str:
    """
    Export questions to different quiz formats

    Args:
        questions_data: Questions data to export
        format_type: Format type (generic, moodle, canvas, etc.)

    Returns:
        Formatted string
    """
    if format_type == "generic":
        return json.dumps(questions_data, indent=2)

    # Add more formats as needed
    return json.dumps(questions_data, indent=2)


def merge_question_data(data1: Dict, data2: Dict) -> Dict:
    """
    Merge two question data dictionaries

    Args:
        data1: First questions data
        data2: Second questions data

    Returns:
        Merged questions data
    """
    merged = data1.copy()

    for doc_key, doc_data in data2.items():
        if doc_key in merged:
            # Merge standards
            existing_standards = {s['standard_id']: s for s in merged[doc_key]['standards']}

            for std_data in doc_data['standards']:
                std_id = std_data['standard_id']
                if std_id in existing_standards:
                    # Append questions to existing standard
                    existing_standards[std_id]['questions'].extend(std_data['questions'])
                else:
                    # Add new standard
                    merged[doc_key]['standards'].append(std_data)
        else:
            # Add new document
            merged[doc_key] = doc_data

    return merged


def generate_report(questions_data: Dict) -> str:
    """
    Generate a text report of the questions data

    Args:
        questions_data: Questions data to report on

    Returns:
        Formatted report string
    """
    stats = calculate_statistics(questions_data)

    report = f"""
SOL QUIZ GENERATOR REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
-------
Total Documents: {stats['total_documents']}
Total Standards: {stats['total_standards']}
Total Questions: {stats['total_questions']}
Avg Questions per Standard: {stats['avg_questions_per_standard']:.2f}

QUESTIONS BY TYPE
-----------------
"""

    for q_type, count in stats['by_type'].items():
        percentage = (count / stats['total_questions'] * 100) if stats['total_questions'] > 0 else 0
        report += f"{q_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"

    report += """
QUESTIONS BY DIFFICULTY
-----------------------
"""

    for difficulty, count in stats['by_difficulty'].items():
        percentage = (count / stats['total_questions'] * 100) if stats['total_questions'] > 0 else 0
        report += f"{difficulty.title()}: {count} ({percentage:.1f}%)\n"

    report += """
STANDARDS BY FEASIBILITY
------------------------
"""

    for feasibility, count in stats['by_feasibility'].items():
        percentage = (count / stats['total_standards'] * 100) if stats['total_standards'] > 0 else 0
        report += f"{feasibility.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"

    return report


def get_question_type_icon(question_type: str) -> str:
    """Get icon for question type"""
    icons = {
        "multiple_choice": "🔘",
        "fill_in_blank": "📝",
        "true_false": "✓✗",
        "short_answer": "💭"
    }
    return icons.get(question_type, "❓")


def search_questions(questions_data: Dict, search_term: str) -> Dict:
    """
    Search questions by text

    Args:
        questions_data: Questions data to search
        search_term: Text to search for

    Returns:
        Filtered questions data containing search term
    """
    search_term = search_term.lower()
    filtered_data = {}

    for doc_key, doc_data in questions_data.items():
        filtered_standards = []

        for std_data in doc_data.get('standards', []):
            # Check if standard ID or statement matches
            if search_term in std_data.get('standard_id', '').lower():
                filtered_standards.append(std_data)
                continue

            # Search in questions
            filtered_questions = []
            for q in std_data.get('questions', []):
                if (search_term in q.get('question_text', '').lower() or
                    search_term in q.get('correct_answer', '').lower() or
                    any(search_term in opt.lower() for opt in q.get('options', []))):
                    filtered_questions.append(q)

            if filtered_questions:
                filtered_std = std_data.copy()
                filtered_std['questions'] = filtered_questions
                filtered_standards.append(filtered_std)

        if filtered_standards:
            filtered_doc = doc_data.copy()
            filtered_doc['standards'] = filtered_standards
            filtered_data[doc_key] = filtered_doc

    return filtered_data
