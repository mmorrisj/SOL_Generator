"""
SOL Quiz Generator
Generates age-appropriate quiz questions from Virginia Standards of Learning (SOL) documents.
Uses OpenAI API to determine if standards are text-appropriate and create various question types.
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class QuestionType(Enum):
    """Types of quiz questions that can be generated"""
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


class TextFeasibility(Enum):
    """Whether a standard can be assessed via text-based questions"""
    FEASIBLE = "feasible"
    PARTIALLY_FEASIBLE = "partially_feasible"
    NOT_FEASIBLE = "not_feasible"


@dataclass
class QuizQuestion:
    """Represents a generated quiz question"""
    standard_id: str
    question_type: str
    question_text: str
    correct_answer: str
    options: Optional[List[str]] = None  # For multiple choice
    explanation: Optional[str] = None
    difficulty_level: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class StandardAssessment:
    """Assessment of whether a standard can be tested via text"""
    standard_id: str
    feasibility: str
    reasoning: str
    suggested_question_types: List[str]
    requires_visual_aids: bool
    requires_hands_on: bool


class SOLQuizGenerator:
    """Main class for generating quiz questions from SOL standards"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the quiz generator.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")

        openai.api_key = self.api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)

    def load_sol_documents(self, filepath: str) -> Dict:
        """
        Load SOL documents from JSON file.

        Args:
            filepath: Path to the all_structured_documents.json file

        Returns:
            Dictionary containing all SOL documents
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def assess_text_feasibility(self, standard: Dict, grade_level: str) -> StandardAssessment:
        """
        Determine if a standard can be assessed via text-based questions.

        Args:
            standard: The standard object from SOL document
            grade_level: Grade level (e.g., "Grade 1", "Grade 5")

        Returns:
            StandardAssessment object with feasibility analysis
        """
        prompt = f"""Analyze the following educational standard and determine if it can be assessed using text-based quiz questions.

Grade Level: {grade_level}
Standard ID: {standard.get('id', 'N/A')}
Standard Statement: {standard.get('statement', 'N/A')}

Objectives:
{json.dumps(standard.get('knowledge_and_skills', {}).get('objectives', []), indent=2)}

Please analyze:
1. Can this standard be assessed via text-based questions? (feasible/partially_feasible/not_feasible)
2. Why or why not?
3. What types of questions would work best? (multiple_choice, fill_in_blank, true_false, short_answer)
4. Does this require visual aids or diagrams?
5. Does this require hands-on physical activities?

Respond in JSON format:
{{
    "feasibility": "feasible|partially_feasible|not_feasible",
    "reasoning": "explanation of your assessment",
    "suggested_question_types": ["type1", "type2"],
    "requires_visual_aids": true/false,
    "requires_hands_on": true/false
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an educational assessment expert specializing in creating age-appropriate quiz questions."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        result = json.loads(response.choices[0].message.content)

        return StandardAssessment(
            standard_id=standard.get('id', 'N/A'),
            feasibility=result['feasibility'],
            reasoning=result['reasoning'],
            suggested_question_types=result['suggested_question_types'],
            requires_visual_aids=result['requires_visual_aids'],
            requires_hands_on=result['requires_hands_on']
        )

    def generate_question(
        self,
        standard: Dict,
        grade_level: str,
        question_type: QuestionType,
        objective: Optional[Dict] = None
    ) -> QuizQuestion:
        """
        Generate a single quiz question for a standard.

        Args:
            standard: The standard object from SOL document
            grade_level: Grade level for age-appropriate language
            question_type: Type of question to generate
            objective: Specific objective to focus on (optional)

        Returns:
            QuizQuestion object
        """
        objective_text = ""
        if objective:
            objective_text = f"\nSpecific Objective: {objective.get('text', '')}"

        prompt = f"""Create an age-appropriate quiz question for the following educational standard.

Grade Level: {grade_level}
Standard ID: {standard.get('id', 'N/A')}
Standard Statement: {standard.get('statement', 'N/A')}{objective_text}

Question Type: {question_type.value}

Requirements:
1. Use age-appropriate vocabulary and sentence structure for {grade_level}
2. Question should directly assess understanding of the standard
3. For multiple choice: provide 4 options with one correct answer
4. For fill in blank: indicate the blank with _____
5. Include a brief explanation of why the answer is correct
6. Rate difficulty as: easy, medium, or hard

Respond in JSON format:
{{
    "question_text": "the question",
    "correct_answer": "the correct answer",
    "options": ["option1", "option2", "option3", "option4"],  // only for multiple choice
    "explanation": "why this answer is correct",
    "difficulty_level": "easy|medium|hard"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert elementary and secondary education teacher who creates engaging, age-appropriate quiz questions."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        result = json.loads(response.choices[0].message.content)

        return QuizQuestion(
            standard_id=standard.get('id', 'N/A'),
            question_type=question_type.value,
            question_text=result['question_text'],
            correct_answer=result['correct_answer'],
            options=result.get('options'),
            explanation=result.get('explanation'),
            difficulty_level=result.get('difficulty_level')
        )

    def generate_questions_for_standard(
        self,
        standard: Dict,
        grade_level: str,
        num_questions: int = 3,
        question_types: Optional[List[QuestionType]] = None
    ) -> Dict[str, Any]:
        """
        Generate multiple questions for a single standard.

        Args:
            standard: The standard object
            grade_level: Grade level
            num_questions: Number of questions to generate
            question_types: List of question types to use (if None, will assess automatically)

        Returns:
            Dictionary with assessment and generated questions
        """
        # First, assess text feasibility
        assessment = self.assess_text_feasibility(standard, grade_level)

        if assessment.feasibility == TextFeasibility.NOT_FEASIBLE.value:
            return {
                "standard_id": standard.get('id'),
                "assessment": asdict(assessment),
                "questions": [],
                "message": "Standard not suitable for text-based assessment"
            }

        # Determine question types to use
        if question_types is None:
            question_types = [QuestionType(qt) for qt in assessment.suggested_question_types[:num_questions]]

        # Generate questions
        questions = []
        objectives = standard.get('knowledge_and_skills', {}).get('objectives', [])

        for i in range(min(num_questions, len(question_types))):
            q_type = question_types[i]
            objective = objectives[i] if i < len(objectives) else None

            try:
                question = self.generate_question(standard, grade_level, q_type, objective)
                questions.append(question.to_dict())
            except Exception as e:
                print(f"Error generating question {i+1}: {str(e)}")

        return {
            "standard_id": standard.get('id'),
            "assessment": asdict(assessment),
            "questions": questions
        }

    def process_document(
        self,
        document: Dict,
        max_standards: Optional[int] = None,
        questions_per_standard: int = 3
    ) -> Dict[str, Any]:
        """
        Process an entire SOL document and generate questions for all standards.

        Args:
            document: The document object from SOL JSON
            max_standards: Maximum number of standards to process (None for all)
            questions_per_standard: Number of questions per standard

        Returns:
            Dictionary with all generated content
        """
        grade_level = document.get('grade_level', 'Unknown')
        course_name = document.get('course_name', 'Unknown')

        results = {
            "document_info": {
                "title": document.get('title'),
                "grade_level": grade_level,
                "course_name": course_name,
                "year": document.get('year')
            },
            "standards_processed": 0,
            "total_questions_generated": 0,
            "standards": []
        }

        count = 0
        for strand in document.get('strands', []):
            for standard in strand.get('standards', []):
                if max_standards and count >= max_standards:
                    break

                print(f"Processing {standard.get('id')}...")

                result = self.generate_questions_for_standard(
                    standard,
                    grade_level,
                    questions_per_standard
                )

                results['standards'].append(result)
                results['standards_processed'] += 1
                results['total_questions_generated'] += len(result.get('questions', []))

                count += 1

            if max_standards and count >= max_standards:
                break

        return results

    def save_results(self, results: Dict, output_file: str):
        """Save generated questions to a JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")


def main():
    """Example usage"""
    # Initialize generator
    generator = SOLQuizGenerator()

    # Load SOL documents
    print("Loading SOL documents...")
    data = generator.load_sol_documents("all_structured_documents.json")

    # Process first document (as an example)
    print(f"\nProcessing document 1 of {data['total_documents']}...")
    first_doc = data['documents'][0]['document']

    # Generate questions for first 2 standards
    results = generator.process_document(
        first_doc,
        max_standards=2,
        questions_per_standard=3
    )

    # Save results
    generator.save_results(results, "generated_questions.json")

    print(f"\nCompleted!")
    print(f"Standards processed: {results['standards_processed']}")
    print(f"Questions generated: {results['total_questions_generated']}")


if __name__ == "__main__":
    main()
