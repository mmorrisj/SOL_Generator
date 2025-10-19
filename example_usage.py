"""
Example usage scripts for SOL Quiz Generator
Demonstrates various ways to use the quiz generation system
"""

from sol_quiz_generator import SOLQuizGenerator, QuestionType


def example_1_single_standard():
    """Generate questions for a single standard"""
    print("=" * 60)
    print("EXAMPLE 1: Generate questions for a single standard")
    print("=" * 60)

    generator = SOLQuizGenerator()
    data = generator.load_sol_documents("all_structured_documents.json")

    # Get first standard from first document
    first_doc = data['documents'][0]['document']
    first_standard = first_doc['strands'][0]['standards'][0]
    grade_level = first_doc['grade_level']

    print(f"\nStandard: {first_standard['id']}")
    print(f"Statement: {first_standard['statement']}\n")

    # Generate 3 questions with different types
    result = generator.generate_questions_for_standard(
        standard=first_standard,
        grade_level=grade_level,
        num_questions=3,
        question_types=[
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.FILL_IN_BLANK,
            QuestionType.TRUE_FALSE
        ]
    )

    print(f"Feasibility: {result['assessment']['feasibility']}")
    print(f"Reasoning: {result['assessment']['reasoning']}\n")

    for i, q in enumerate(result['questions'], 1):
        print(f"Question {i} ({q['question_type']}):")
        print(f"  {q['question_text']}")
        if q.get('options'):
            for opt in q['options']:
                print(f"    - {opt}")
        print(f"  Correct Answer: {q['correct_answer']}")
        print(f"  Explanation: {q['explanation']}\n")


def example_2_specific_grade():
    """Generate questions for all standards in a specific grade"""
    print("=" * 60)
    print("EXAMPLE 2: Generate questions for Grade 1 Math (first 3 standards)")
    print("=" * 60)

    generator = SOLQuizGenerator()
    data = generator.load_sol_documents("all_structured_documents.json")

    # Find Grade 1 Math document
    grade_1_math = None
    for doc_wrapper in data['documents']:
        doc = doc_wrapper['document']
        if doc.get('grade_level') == 'Grade 1' and doc.get('course_name') == 'Mathematics':
            grade_1_math = doc
            break

    if grade_1_math:
        results = generator.process_document(
            grade_1_math,
            max_standards=3,
            questions_per_standard=2
        )

        print(f"\nProcessed: {results['standards_processed']} standards")
        print(f"Generated: {results['total_questions_generated']} questions")

        # Save to file
        generator.save_results(results, "grade_1_math_sample.json")
        print("\nResults saved to 'grade_1_math_sample.json'")
    else:
        print("Grade 1 Math document not found")


def example_3_assess_only():
    """Assess text feasibility without generating questions"""
    print("=" * 60)
    print("EXAMPLE 3: Assess text feasibility for multiple standards")
    print("=" * 60)

    generator = SOLQuizGenerator()
    data = generator.load_sol_documents("all_structured_documents.json")

    first_doc = data['documents'][0]['document']
    grade_level = first_doc['grade_level']

    # Assess first 5 standards
    assessments = []
    for strand in first_doc['strands'][:2]:  # First 2 strands
        for standard in strand['standards'][:3]:  # First 3 standards each
            assessment = generator.assess_text_feasibility(standard, grade_level)
            assessments.append({
                'standard_id': assessment.standard_id,
                'feasibility': assessment.feasibility,
                'reasoning': assessment.reasoning,
                'suggested_types': assessment.suggested_question_types
            })

    print(f"\nAssessed {len(assessments)} standards:\n")
    for a in assessments:
        print(f"Standard: {a['standard_id']}")
        print(f"  Feasibility: {a['feasibility']}")
        print(f"  Suggested Types: {', '.join(a['suggested_types'])}")
        print(f"  Reasoning: {a['reasoning'][:100]}...\n")


def example_4_custom_model():
    """Use a different OpenAI model"""
    print("=" * 60)
    print("EXAMPLE 4: Using a custom OpenAI model")
    print("=" * 60)

    # Use gpt-4o for potentially better quality (more expensive)
    generator = SOLQuizGenerator(model="gpt-4o-mini")

    data = generator.load_sol_documents("all_structured_documents.json")
    first_doc = data['documents'][0]['document']

    results = generator.process_document(
        first_doc,
        max_standards=1,
        questions_per_standard=3
    )

    print(f"Generated {results['total_questions_generated']} questions using {generator.model}")


def example_5_batch_processing():
    """Process multiple documents in batch"""
    print("=" * 60)
    print("EXAMPLE 5: Batch process multiple grade levels")
    print("=" * 60)

    generator = SOLQuizGenerator()
    data = generator.load_sol_documents("all_structured_documents.json")

    # Process first 3 documents, 2 standards each
    batch_results = []

    for i, doc_wrapper in enumerate(data['documents'][:3], 1):
        doc = doc_wrapper['document']
        print(f"\nProcessing document {i}: {doc['course_name']} - {doc['grade_level']}")

        results = generator.process_document(
            doc,
            max_standards=2,
            questions_per_standard=2
        )

        batch_results.append(results)

    # Save all results
    output = {
        "total_documents_processed": len(batch_results),
        "documents": batch_results
    }

    generator.save_results(output, "batch_results.json")
    print("\nBatch processing complete. Results saved to 'batch_results.json'")


if __name__ == "__main__":
    import sys

    examples = {
        "1": example_1_single_standard,
        "2": example_2_specific_grade,
        "3": example_3_assess_only,
        "4": example_4_custom_model,
        "5": example_5_batch_processing
    }

    if len(sys.argv) > 1 and sys.argv[1] in examples:
        examples[sys.argv[1]]()
    else:
        print("SOL Quiz Generator - Example Usage")
        print("\nAvailable examples:")
        print("  1 - Generate questions for a single standard")
        print("  2 - Generate questions for specific grade (Grade 1 Math)")
        print("  3 - Assess text feasibility only")
        print("  4 - Use custom OpenAI model")
        print("  5 - Batch process multiple documents")
        print("\nUsage: python example_usage.py [1-5]")
        print("\nRunning Example 1 by default...\n")
        example_1_single_standard()
