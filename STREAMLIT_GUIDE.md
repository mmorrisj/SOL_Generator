# Streamlit UI Guide

Interactive web interface for the SOL Quiz Generator - review, manage, and generate quiz questions through an intuitive UI.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- streamlit
- pandas
- openai
- python-dotenv

### 2. Set Up API Key

Make sure your `.env` file exists with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 3. Launch the UI

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Features Overview

### 🏠 Home Page

The landing page shows:
- Quick stats (documents, questions, standards)
- Feature overview
- Getting started guide

### 📖 Browse Standards

**Browse all SOL standards by document:**
- Select course and grade level
- View all strands and standards
- Explore objectives for each standard
- Review standard statements

**Use this to:**
- Familiarize yourself with available standards
- Find specific standards to generate questions for
- Understand the structure of SOL documents

### ⚡ Generate Questions

**AI-powered question generation:**

1. **Select Document & Standard**
   - Choose from all available documents
   - Select specific standard to work with

2. **Configure Generation**
   - Set number of questions (1-10)
   - Choose question types:
     - Multiple Choice
     - Fill in the Blank
     - True/False
     - Short Answer

3. **AI Assessment**
   - System first assesses if standard is text-feasible
   - Shows reasoning for assessment
   - Warns if standard may not be suitable

4. **Generate & Review**
   - AI creates questions based on your settings
   - Questions are age-appropriate for the grade level
   - Each question includes explanation and difficulty rating

5. **Automatic Storage**
   - Generated questions are stored in session
   - Can generate more questions for the same standard
   - All questions accumulate until you clear or export

### 📝 Review Questions

**Manage your generated questions:**

- **View by Document**: Browse questions organized by course and grade
- **Standard Details**: See feasibility assessment for each standard
- **Question Cards**: Each question displayed with:
  - Question type and difficulty
  - Question text
  - Answer options (for multiple choice)
  - Correct answer highlighted
  - Explanation (expandable)

- **Actions Available**:
  - 🗑️ **Delete**: Remove individual questions
  - ➕ **Generate More**: Add questions to existing standards

**Question Display:**
- Visual difficulty indicators (🟢 Easy, 🟡 Medium, 🔴 Hard)
- Correct answers marked with ✓
- Expandable explanations

### 💾 Manage Data

**Import, export, and analyze your questions:**

#### Export Questions
- Save all questions to JSON file
- Download questions directly to your computer
- Custom filename support

#### Import Questions
- Upload previously exported JSON files
- Merge with existing questions
- Resume work from previous sessions

#### Statistics Dashboard
- **Table View**: All standards with question counts by type
- **Summary Metrics**:
  - Total standards processed
  - Total questions generated
  - Average questions per standard
  - Most common question type

#### Clear Data
- Remove all questions from memory
- Start fresh (files are not affected)

## Workflow Examples

### Example 1: Generate Questions for Specific Grade

1. Go to **📖 Browse Standards**
2. Select "Mathematics - Grade 1"
3. Note interesting standards
4. Go to **⚡ Generate Questions**
5. Select the document and standard
6. Set to 3 questions, multiple choice + fill in blank
7. Click **Generate**
8. Review questions in the same page
9. Go to **📝 Review Questions** to manage them
10. Export from **💾 Manage Data**

### Example 2: Build Question Bank for Multiple Standards

1. **⚡ Generate Questions**
   - Select first standard
   - Generate 3 questions

2. Repeat for more standards
   - Questions accumulate automatically
   - Switch between different documents

3. **📝 Review Questions**
   - Review all generated questions
   - Delete any that don't fit
   - Generate more for weak areas

4. **💾 Manage Data**
   - Check statistics
   - Export complete question bank
   - Save for later use

### Example 3: Review and Refine Question Set

1. **💾 Manage Data**
   - Import previously saved questions

2. **📝 Review Questions**
   - Browse through all questions
   - Delete low-quality questions
   - Note standards needing more questions

3. **⚡ Generate Questions**
   - Add more questions to sparse standards
   - Try different question types

4. **💾 Manage Data**
   - Review updated statistics
   - Export refined question set

## Tips & Best Practices

### For Best Results

1. **Start Small**: Generate 2-3 questions per standard first
2. **Review Quality**: Check AI-generated questions before accumulating many
3. **Mix Types**: Use different question types for comprehensive assessment
4. **Check Feasibility**: Pay attention to feasibility warnings
5. **Regular Exports**: Save your work frequently

### Understanding Feasibility

- **Feasible**: Standard works well for text-based questions
- **Partially Feasible**: Some aspects can be tested via text
- **Not Feasible**: Requires hands-on or visual assessment

You can still generate questions for "not feasible" standards, but quality may vary.

### Question Quality

The AI generates questions based on:
- Grade-appropriate vocabulary
- Standard objectives
- Question type requirements

**If questions need improvement:**
- Delete and regenerate
- Try different question types
- Manually edit exported JSON

### Managing Large Question Sets

- Use **Statistics** to track coverage
- Export regularly to avoid losing work
- Clear session data when starting new project
- Keep organized exports by subject/grade

## Keyboard Shortcuts

Streamlit provides these shortcuts:
- `R` - Rerun the app
- `C` - Clear cache
- `S` - Settings

## Troubleshooting

### UI Won't Start

**Error: "No module named 'streamlit'"**
```bash
pip install streamlit
```

**Error: "No module named 'sol_quiz_generator'"**
- Make sure you're in the correct directory
- Check that `sol_quiz_generator.py` exists

### API Connection Issues

**Red status in sidebar: "OpenAI API Not Connected"**
1. Check `.env` file exists
2. Verify API key is correct
3. Test with: `python test_setup.py`
4. Click "🔄 Retry Connection" in sidebar

### Data Not Loading

**"No SOL data loaded"**
- Verify `all_structured_documents.json` exists
- Check file isn't corrupted
- Try restarting the app

### Questions Not Saving

Questions are stored in **session state** (memory):
- They persist while app is running
- Cleared when you close the browser or restart app
- Use **Export** to save permanently

### Performance Issues

If app is slow:
1. Clear generated questions (Manage Data page)
2. Restart Streamlit
3. Generate fewer questions at once
4. Check internet connection (API calls)

## Advanced Features

### Custom Styling

The UI includes custom CSS for:
- Colored feasibility badges
- Formatted question cards
- Responsive layout

Modify in `app.py` under the `st.markdown("""<style>...)` section.

### Session State

Data is stored in `st.session_state`:
- `sol_data` - Loaded SOL documents
- `generator` - OpenAI generator instance
- `questions_data` - All generated questions
- `selected_document` - Currently selected document
- `selected_standard` - Currently selected standard

### Helper Functions

Additional utilities in [ui_helpers.py](ui_helpers.py):
- `calculate_statistics()` - Compute question stats
- `filter_questions()` - Filter by criteria
- `validate_question()` - Validate question structure
- `search_questions()` - Search functionality
- `generate_report()` - Create text reports

## Data Format

### Exported JSON Structure

```json
{
  "export_date": "2024-01-15T10:30:00",
  "total_documents": 1,
  "documents": [
    {
      "document_info": {
        "title": "Mathematics Standards...",
        "grade_level": "Grade 1",
        "course_name": "Mathematics",
        "year": 2023
      },
      "standards": [
        {
          "standard_id": "1.NS.1",
          "assessment": {
            "feasibility": "feasible",
            "reasoning": "...",
            "suggested_question_types": ["multiple_choice"]
          },
          "questions": [
            {
              "standard_id": "1.NS.1",
              "question_type": "multiple_choice",
              "question_text": "...",
              "correct_answer": "...",
              "options": ["...", "..."],
              "explanation": "...",
              "difficulty_level": "easy"
            }
          ]
        }
      ]
    }
  ]
}
```

## Future Enhancements

Potential features for future versions:
- Search functionality for questions
- Filter questions by type/difficulty
- Edit questions inline
- Batch generation for multiple standards
- Export to LMS formats (Moodle, Canvas)
- Question difficulty calibration
- Duplicate question detection
- AI-powered question improvement suggestions

## Support

For issues:
1. Check this guide
2. Review [README.md](README.md)
3. Test setup with `python test_setup.py`
4. Check console for error messages

## Running in Production

To deploy the UI:

```bash
# Run on custom port
streamlit run app.py --server.port 8080

# Run on network
streamlit run app.py --server.address 0.0.0.0

# Configure settings in .streamlit/config.toml
```

See [Streamlit documentation](https://docs.streamlit.io/) for deployment options.
