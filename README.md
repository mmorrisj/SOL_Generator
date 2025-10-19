# SOL Quiz Generator

AI-powered quiz question generator for Virginia Standards of Learning (SOL). This system uses OpenAI's API to analyze educational standards and generate age-appropriate quiz questions in multiple formats.

## Features

- **Automated Text Feasibility Assessment**: AI determines if standards can be assessed via text-based questions
- **Multiple Question Types**: Generates multiple choice, fill-in-the-blank, true/false, and short answer questions
- **Age-Appropriate Content**: Tailors vocabulary and complexity to specific grade levels
- **Interactive Web UI**: Streamlit-based interface for reviewing, managing, and generating questions
- **Batch Processing**: Process multiple documents and standards efficiently
- **Detailed Explanations**: Includes reasoning for correct answers
- **Flexible Configuration**: Customizable models, question types, and generation parameters

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

## Quick Start

### Option 1: Interactive Web UI (Recommended)

Launch the Streamlit web interface for an interactive experience:

```bash
streamlit run app.py
```

This opens a web interface where you can:
- Browse all SOL standards
- Generate questions with a visual interface
- Review and manage generated questions
- Delete or regenerate questions as needed
- Export questions to JSON

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed UI documentation.

### Option 2: Python API

Use the Python API directly for programmatic access:

```python
from sol_quiz_generator import SOLQuizGenerator

# Initialize the generator
generator = SOLQuizGenerator()

# Load your SOL documents
data = generator.load_sol_documents("all_structured_documents.json")

# Process first document, generating questions for 5 standards
first_doc = data['documents'][0]['document']
results = generator.process_document(
    first_doc,
    max_standards=5,
    questions_per_standard=3
)

# Save results
generator.save_results(results, "output.json")
```

### Run Examples

The project includes 5 example scripts demonstrating different use cases:

```bash
# Run all examples
python example_usage.py

# Or run a specific example (1-5)
python example_usage.py 1
```

**Available Examples**:
1. Generate questions for a single standard
2. Generate questions for specific grade (Grade 1 Math)
3. Assess text feasibility only (no question generation)
4. Use custom OpenAI model
5. Batch process multiple documents

## Project Structure

```
SOL_Generator/
├── sol_quiz_generator.py      # Main generator class
├── app.py                      # Streamlit web UI
├── ui_helpers.py               # UI helper functions
├── config.py                   # Configuration settings
├── example_usage.py            # Example scripts
├── test_setup.py               # Setup verification script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── all_structured_documents.json  # SOL standards data
├── README.md                   # This file
├── STREAMLIT_GUIDE.md         # UI documentation
└── QUICKSTART.md              # Quick start guide
```

## How It Works

### 1. Text Feasibility Assessment

The system first analyzes each standard to determine if it can be assessed via text:

```python
assessment = generator.assess_text_feasibility(standard, grade_level)
# Returns: feasible, partially_feasible, or not_feasible
```

Assessment includes:
- Feasibility rating
- Reasoning for the assessment
- Suggested question types
- Whether visual aids are needed
- Whether hands-on activities are required

### 2. Question Generation

For feasible standards, the AI generates age-appropriate questions:

```python
question = generator.generate_question(
    standard=standard,
    grade_level="Grade 1",
    question_type=QuestionType.MULTIPLE_CHOICE
)
```

Each question includes:
- Question text
- Correct answer
- Answer options (for multiple choice)
- Explanation
- Difficulty level (easy/medium/hard)

## API Reference

### SOLQuizGenerator Class

**Constructor**:
```python
SOLQuizGenerator(api_key=None, model="gpt-4o-mini")
```
- `api_key`: OpenAI API key (defaults to OPENAI_API_KEY env var)
- `model`: OpenAI model to use (default: gpt-4o-mini)

**Key Methods**:

- `load_sol_documents(filepath)`: Load SOL JSON file
- `assess_text_feasibility(standard, grade_level)`: Assess if standard is text-appropriate
- `generate_question(standard, grade_level, question_type, objective)`: Generate single question
- `generate_questions_for_standard(standard, grade_level, num_questions, question_types)`: Generate multiple questions for one standard
- `process_document(document, max_standards, questions_per_standard)`: Process entire document
- `save_results(results, output_file)`: Save to JSON file

### Question Types

Available via `QuestionType` enum:
- `QuestionType.MULTIPLE_CHOICE`: 4-option multiple choice
- `QuestionType.FILL_IN_BLANK`: Fill-in-the-blank format
- `QuestionType.TRUE_FALSE`: True/false questions
- `QuestionType.SHORT_ANSWER`: Short answer questions

## Configuration

Edit [config.py](config.py) to customize:

- **OpenAI Model**: Switch between models (gpt-4o-mini, gpt-4o, etc.)
- **Temperature Settings**: Control creativity vs consistency
- **Question Distribution**: Adjust probability of each question type
- **Grade Level Settings**: Configure vocabulary complexity
- **Output Options**: Toggle explanations, assessments, etc.

## Output Format

Generated questions are saved in JSON format:

```json
{
  "document_info": {
    "title": "Mathematics Standards of Learning...",
    "grade_level": "Grade 1",
    "course_name": "Mathematics",
    "year": 2023
  },
  "standards_processed": 5,
  "total_questions_generated": 15,
  "standards": [
    {
      "standard_id": "1.NS.1",
      "assessment": {
        "feasibility": "feasible",
        "reasoning": "...",
        "suggested_question_types": ["multiple_choice", "fill_in_blank"]
      },
      "questions": [
        {
          "standard_id": "1.NS.1",
          "question_type": "multiple_choice",
          "question_text": "Which number comes after 45?",
          "correct_answer": "46",
          "options": ["44", "46", "47", "50"],
          "explanation": "When counting forward by ones...",
          "difficulty_level": "easy"
        }
      ]
    }
  ]
}
```

## Cost Considerations

The system uses OpenAI's API, which charges per token:

- **gpt-4o-mini** (default): Most cost-effective (~$0.15/1M input tokens)
- **gpt-4o**: Higher quality, more expensive (~$2.50/1M input tokens)

Estimated costs:
- Assessing 1 standard: ~500-1000 tokens
- Generating 1 question: ~300-500 tokens
- Processing 100 standards with 3 questions each: ~$0.15-0.50 (using gpt-4o-mini)

## Advanced Usage

### Custom Question Types for Each Standard

```python
from sol_quiz_generator import QuestionType

result = generator.generate_questions_for_standard(
    standard=my_standard,
    grade_level="Grade 3",
    num_questions=4,
    question_types=[
        QuestionType.MULTIPLE_CHOICE,
        QuestionType.MULTIPLE_CHOICE,
        QuestionType.FILL_IN_BLANK,
        QuestionType.TRUE_FALSE
    ]
)
```

### Focus on Specific Objectives

```python
objectives = standard['knowledge_and_skills']['objectives']
for obj in objectives:
    question = generator.generate_question(
        standard=standard,
        grade_level="Grade 2",
        question_type=QuestionType.MULTIPLE_CHOICE,
        objective=obj
    )
```

### Batch Process Specific Grades

```python
data = generator.load_sol_documents("all_structured_documents.json")

# Filter for specific grade and subject
for doc_wrapper in data['documents']:
    doc = doc_wrapper['document']
    if doc['grade_level'] == 'Grade 3' and doc['course_name'] == 'Science':
        results = generator.process_document(doc, max_standards=None)
        generator.save_results(results, "grade3_science_questions.json")
```

## Troubleshooting

**"OpenAI API key must be provided"**
- Ensure you've created a `.env` file with your API key
- Or pass the key directly: `SOLQuizGenerator(api_key="your-key")`

**Rate limit errors**
- Add delays between API calls
- Reduce `max_standards` parameter
- Upgrade your OpenAI plan

**Poor question quality**
- Try using `gpt-4o` instead of `gpt-4o-mini`
- Adjust temperature in [config.py](config.py)
- Modify prompts in [sol_quiz_generator.py](sol_quiz_generator.py)

## Contributing

Contributions welcome! Areas for improvement:
- Additional question types (matching, ordering, etc.)
- Integration with learning management systems
- Question difficulty calibration
- Multi-language support
- Question validation and testing

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the example scripts in [example_usage.py](example_usage.py)
2. Review configuration options in [config.py](config.py)
3. Consult OpenAI API documentation: https://platform.openai.com/docs