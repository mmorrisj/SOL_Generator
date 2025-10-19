# Quick Start Guide

Get started with SOL Quiz Generator in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `streamlit` - Interactive web UI
- `pandas` - Data analysis and statistics

## Step 2: Configure API Key

1. Get your OpenAI API key from: https://platform.openai.com/api-keys

2. Create a `.env` file (copy from template):
   ```bash
   # On Windows
   copy .env.example .env

   # On Mac/Linux
   cp .env.example .env
   ```

3. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Step 3: Test Your Setup

```bash
python test_setup.py
```

This verifies:
- All packages are installed
- API key is configured
- Data file is accessible
- Module imports correctly

## Your First Quiz Generation

### Option A: Use the Web UI (Recommended!)

```bash
streamlit run app.py
```

This launches an **interactive web interface** where you can:
- 📖 **Browse** all SOL standards by grade and subject
- ⚡ **Generate** questions with visual controls
- 📝 **Review** generated questions in an organized view
- 🗑️ **Delete** unwanted questions with one click
- ➕ **Generate more** questions for any standard
- 💾 **Export** your complete question bank

**Perfect for:** Visual review, managing questions, non-programmers

👉 See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for complete UI documentation

### Option B: Run an Example Script

```bash
# Generate questions for a single standard
python example_usage.py 1

# Generate questions for Grade 1 Math
python example_usage.py 2

# See all examples
python example_usage.py
```

**Perfect for:** Quick testing, understanding the API

### Option C: Use the API Directly

```python
from sol_quiz_generator import SOLQuizGenerator

# Initialize
generator = SOLQuizGenerator()

# Load data
data = generator.load_sol_documents("all_structured_documents.json")

# Generate questions for first document, first 3 standards
first_doc = data['documents'][0]['document']
results = generator.process_document(
    first_doc,
    max_standards=3,
    questions_per_standard=2
)

# Save results
generator.save_results(results, "my_questions.json")

print(f"Generated {results['total_questions_generated']} questions!")
```

## What Gets Generated?

For each standard, the system:

1. **Assesses Text Feasibility**: Determines if the standard can be tested via text
2. **Generates Multiple Questions**: Creates 2-3 questions in various formats:
   - Multiple choice (4 options)
   - Fill in the blank
   - True/false
   - Short answer
3. **Provides Explanations**: Includes why each answer is correct
4. **Rates Difficulty**: Easy, medium, or hard

## Output Example

```json
{
  "standard_id": "1.NS.1",
  "question_type": "multiple_choice",
  "question_text": "If you count forward by ones starting at 45, what number comes next?",
  "correct_answer": "46",
  "options": ["44", "45", "46", "47"],
  "explanation": "When counting forward by ones, each number increases by 1.",
  "difficulty_level": "easy"
}
```

## Cost Estimate

Using the default `gpt-4o-mini` model:
- **1 standard**: ~$0.001 (about 1/10 of a cent)
- **100 standards**: ~$0.15-0.50
- **1000 standards**: ~$1.50-5.00

## Next Steps

- 🌐 **Launch the Web UI**: `streamlit run app.py` for interactive experience
- 📖 **Read [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)** for UI features and workflows
- 📚 **Read [README.md](README.md)** for detailed API documentation
- 🔧 **Customize [config.py](config.py)** to adjust generation settings
- 💻 **Explore [example_usage.py](example_usage.py)** for programmatic usage

## Troubleshooting

**Import errors?**
→ Run: `pip install -r requirements.txt`

**API key error?**
→ Make sure `.env` file exists with valid `OPENAI_API_KEY`

**Rate limits?**
→ Reduce `max_standards` or add delays between calls

**Need help?**
→ Check the examples or review the full README

---

**Ready to generate thousands of quiz questions? Let's go!**
