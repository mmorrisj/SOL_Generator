"""
Streamlit UI for SOL Quiz Generator
Interactive interface for reviewing, managing, and generating quiz questions
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from sol_quiz_generator import SOLQuizGenerator, QuestionType
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="SOL Quiz Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .standard-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .question-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
        background-color: white;
    }
    .feasibility-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.875rem;
    }
    .feasible {
        background-color: #d4edda;
        color: #155724;
    }
    .partially-feasible {
        background-color: #fff3cd;
        color: #856404;
    }
    .not-feasible {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'sol_data' not in st.session_state:
        st.session_state.sol_data = None
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = None
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'selected_document' not in st.session_state:
        st.session_state.selected_document = None
    if 'selected_standard' not in st.session_state:
        st.session_state.selected_standard = None
    if 'questions_data' not in st.session_state:
        st.session_state.questions_data = {}


def load_sol_data():
    """Load SOL documents from JSON file"""
    try:
        with open("all_structured_documents.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ all_structured_documents.json not found!")
        return None
    except Exception as e:
        st.error(f"❌ Error loading SOL data: {str(e)}")
        return None


def initialize_generator():
    """Initialize the SOL Quiz Generator"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("❌ OPENAI_API_KEY not found in environment variables!")
            st.info("💡 Create a .env file with your OpenAI API key")
            return None
        return SOLQuizGenerator(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing generator: {str(e)}")
        return None


def save_questions_to_file(data: Dict, filename: str):
    """Save questions to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"❌ Error saving file: {str(e)}")
        return False


def load_questions_from_file(filename: str) -> Optional[Dict]:
    """Load questions from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None


def render_feasibility_badge(feasibility: str):
    """Render a colored feasibility badge"""
    class_name = feasibility.replace('_', '-')
    return f'<span class="feasibility-badge {class_name}">{feasibility.replace("_", " ").title()}</span>'


def render_question_card(question: Dict, question_idx: int, standard_id: str):
    """Render a single question card with edit/delete options"""

    with st.container():
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

        with col1:
            st.markdown(f"**Question {question_idx + 1}** ({question['question_type'].replace('_', ' ').title()})")

        with col2:
            if st.button("🗑️ Delete", key=f"delete_{standard_id}_{question_idx}"):
                return "delete"

        with col3:
            difficulty_color = {
                "easy": "🟢",
                "medium": "🟡",
                "hard": "🔴"
            }
            diff = question.get('difficulty_level', 'medium')
            st.write(f"{difficulty_color.get(diff, '⚪')} {diff.title()}")

        st.markdown(f"**Q:** {question['question_text']}")

        if question.get('options'):
            st.markdown("**Options:**")
            for i, opt in enumerate(question['options'], 1):
                marker = "✓" if opt == question['correct_answer'] else "○"
                st.markdown(f"{marker} {opt}")

        st.markdown(f"**✓ Answer:** {question['correct_answer']}")

        if question.get('explanation'):
            with st.expander("📖 Explanation"):
                st.write(question['explanation'])

        st.divider()

    return None


def sidebar_navigation():
    """Render sidebar navigation"""
    st.sidebar.title("📚 SOL Quiz Generator")

    # API Status Check
    st.sidebar.subheader("🔧 Setup Status")

    if st.session_state.generator:
        st.sidebar.success("✅ OpenAI API Connected")
    else:
        st.sidebar.error("❌ OpenAI API Not Connected")
        if st.sidebar.button("🔄 Retry Connection"):
            st.session_state.generator = initialize_generator()
            st.rerun()

    if st.session_state.sol_data:
        st.sidebar.success(f"✅ {st.session_state.sol_data['total_documents']} SOL Documents Loaded")
    else:
        st.sidebar.error("❌ SOL Documents Not Loaded")

    st.sidebar.divider()

    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📖 Browse Standards", "⚡ Generate Questions", "📝 Review Questions", "💾 Manage Data"],
        label_visibility="collapsed"
    )

    return page


def home_page():
    """Render home page"""
    st.title("📚 SOL Quiz Generator")
    st.markdown("### AI-Powered Quiz Question Generator for Virginia Standards of Learning")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("SOL Documents", st.session_state.sol_data['total_documents'] if st.session_state.sol_data else 0)

    with col2:
        total_questions = 0
        if st.session_state.questions_data:
            for doc_questions in st.session_state.questions_data.values():
                for std_data in doc_questions.get('standards', []):
                    total_questions += len(std_data.get('questions', []))
        st.metric("Generated Questions", total_questions)

    with col3:
        total_standards = 0
        if st.session_state.sol_data:
            for doc_wrapper in st.session_state.sol_data['documents']:
                doc = doc_wrapper['document']
                for strand in doc.get('strands', []):
                    total_standards += len(strand.get('standards', []))
        st.metric("Total Standards", total_standards)

    st.divider()

    st.markdown("""
    ## 🚀 Quick Start Guide

    1. **Browse Standards** - Explore available SOL standards by grade and subject
    2. **Generate Questions** - Use AI to create age-appropriate quiz questions
    3. **Review Questions** - View, edit, and manage generated questions
    4. **Export Data** - Save your questions to JSON files

    ## ✨ Features

    - 🤖 **AI-Powered Generation** - Uses OpenAI to create contextual questions
    - 📊 **Multiple Question Types** - Multiple choice, fill-in-blank, true/false, short answer
    - 🎯 **Text Feasibility Assessment** - Automatically determines if standards are text-testable
    - 📝 **Age-Appropriate** - Tailors vocabulary and complexity to grade level
    - 💾 **Data Management** - Save, load, and export question sets

    ## 📋 Getting Started

    Use the sidebar to navigate between different sections!
    """)


def browse_standards_page():
    """Render browse standards page"""
    st.title("📖 Browse Standards")

    if not st.session_state.sol_data:
        st.error("❌ No SOL data loaded!")
        return

    # Document selection
    documents = st.session_state.sol_data['documents']
    doc_options = [
        f"{doc['document']['course_name']} - {doc['document']['grade_level']} ({doc['document']['year']})"
        for doc in documents
    ]

    selected_doc_idx = st.selectbox(
        "Select Document",
        range(len(doc_options)),
        format_func=lambda i: doc_options[i]
    )

    doc = documents[selected_doc_idx]['document']
    st.session_state.selected_document = doc

    # Document info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Grade Level", doc['grade_level'])
    with col2:
        st.metric("Course", doc['course_name'])
    with col3:
        st.metric("Year", doc['year'])

    st.divider()

    # Browse strands and standards
    st.subheader("📑 Standards by Strand")

    for strand in doc['strands']:
        with st.expander(f"**{strand['code']}** - {strand['name']} ({len(strand['standards'])} standards)"):
            for standard in strand['standards']:
                st.markdown(f"**{standard['id']}**: {standard['statement']}")

                if standard.get('knowledge_and_skills', {}).get('objectives'):
                    with st.expander(f"View Objectives ({len(standard['knowledge_and_skills']['objectives'])} items)"):
                        for obj in standard['knowledge_and_skills']['objectives']:
                            st.markdown(f"- {obj['text']}")

                st.divider()


def generate_questions_page():
    """Render generate questions page"""
    st.title("⚡ Generate Questions")

    if not st.session_state.generator:
        st.error("❌ Generator not initialized. Check your OpenAI API key!")
        return

    if not st.session_state.sol_data:
        st.error("❌ No SOL data loaded!")
        return

    # Document and Standard Selection
    col1, col2 = st.columns(2)

    with col1:
        documents = st.session_state.sol_data['documents']
        doc_options = [
            f"{doc['document']['course_name']} - {doc['document']['grade_level']}"
            for doc in documents
        ]

        selected_doc_idx = st.selectbox(
            "Select Document",
            range(len(doc_options)),
            format_func=lambda i: doc_options[i]
        )

        doc = documents[selected_doc_idx]['document']

    with col2:
        # Get all standards from document
        all_standards = []
        for strand in doc['strands']:
            for standard in strand['standards']:
                all_standards.append({
                    'id': standard['id'],
                    'statement': standard['statement'],
                    'data': standard
                })

        standard_options = [f"{s['id']}: {s['statement'][:80]}..." for s in all_standards]
        selected_std_idx = st.selectbox(
            "Select Standard",
            range(len(standard_options)),
            format_func=lambda i: standard_options[i]
        )

        selected_standard = all_standards[selected_std_idx]['data']

    st.divider()

    # Display selected standard
    st.subheader(f"📌 {selected_standard['id']}")
    st.write(selected_standard['statement'])

    # Generation options
    st.subheader("⚙️ Generation Settings")

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.slider("Number of Questions", 1, 10, 3)

    with col2:
        question_types = st.multiselect(
            "Question Types",
            ["multiple_choice", "fill_in_blank", "true_false", "short_answer"],
            default=["multiple_choice", "fill_in_blank"]
        )

    # Generate button
    if st.button("🚀 Generate Questions", type="primary", use_container_width=True):
        with st.spinner("🤖 AI is generating questions..."):
            try:
                # First assess feasibility
                assessment = st.session_state.generator.assess_text_feasibility(
                    selected_standard,
                    doc['grade_level']
                )

                st.info(f"**Feasibility:** {assessment.feasibility}")
                st.write(f"**Reasoning:** {assessment.reasoning}")

                if assessment.feasibility == "not_feasible":
                    st.warning("⚠️ This standard may not be suitable for text-based questions.")
                    proceed = st.checkbox("Generate anyway?")
                    if not proceed:
                        st.stop()

                # Generate questions
                q_types = [QuestionType(qt) for qt in question_types[:num_questions]]

                result = st.session_state.generator.generate_questions_for_standard(
                    selected_standard,
                    doc['grade_level'],
                    num_questions=num_questions,
                    question_types=q_types if question_types else None
                )

                # Store in session state
                doc_key = f"{doc['course_name']}_{doc['grade_level']}"
                if doc_key not in st.session_state.questions_data:
                    st.session_state.questions_data[doc_key] = {
                        'document_info': {
                            'title': doc['title'],
                            'grade_level': doc['grade_level'],
                            'course_name': doc['course_name'],
                            'year': doc['year']
                        },
                        'standards': []
                    }

                # Check if standard already exists
                existing_idx = None
                for idx, std_data in enumerate(st.session_state.questions_data[doc_key]['standards']):
                    if std_data['standard_id'] == selected_standard['id']:
                        existing_idx = idx
                        break

                if existing_idx is not None:
                    # Append to existing questions
                    st.session_state.questions_data[doc_key]['standards'][existing_idx]['questions'].extend(result['questions'])
                else:
                    # Add new standard
                    st.session_state.questions_data[doc_key]['standards'].append(result)

                st.success(f"✅ Generated {len(result['questions'])} questions!")

                # Display generated questions
                st.subheader("📝 Generated Questions")
                for i, q in enumerate(result['questions']):
                    render_question_card(q, i, selected_standard['id'])

            except Exception as e:
                st.error(f"❌ Error generating questions: {str(e)}")


def review_questions_page():
    """Render review questions page"""
    st.title("📝 Review Questions")

    if not st.session_state.questions_data:
        st.info("ℹ️ No questions generated yet. Go to 'Generate Questions' to create some!")
        return

    # Document selection
    doc_keys = list(st.session_state.questions_data.keys())

    if not doc_keys:
        st.info("ℹ️ No questions available.")
        return

    selected_doc_key = st.selectbox(
        "Select Document",
        doc_keys,
        format_func=lambda k: k.replace('_', ' ')
    )

    doc_data = st.session_state.questions_data[selected_doc_key]

    # Display document info
    st.subheader(f"📚 {doc_data['document_info']['course_name']} - {doc_data['document_info']['grade_level']}")

    total_questions = sum(len(std['questions']) for std in doc_data['standards'])
    st.metric("Total Questions", total_questions)

    st.divider()

    # Standards and questions
    for std_idx, std_data in enumerate(doc_data['standards']):
        with st.expander(f"**{std_data['standard_id']}** ({len(std_data['questions'])} questions)", expanded=True):

            # Assessment info
            assessment = std_data.get('assessment', {})
            if assessment:
                col1, col2 = st.columns([0.3, 0.7])
                with col1:
                    st.markdown(render_feasibility_badge(assessment.get('feasibility', 'unknown')), unsafe_allow_html=True)
                with col2:
                    st.write(assessment.get('reasoning', ''))

            st.divider()

            # Questions
            questions_to_remove = []
            for q_idx, question in enumerate(std_data['questions']):
                action = render_question_card(question, q_idx, std_data['standard_id'])
                if action == "delete":
                    questions_to_remove.append(q_idx)

            # Remove deleted questions
            for q_idx in reversed(questions_to_remove):
                del std_data['questions'][q_idx]
                st.success(f"✅ Question {q_idx + 1} deleted!")
                st.rerun()

            # Generate more questions for this standard
            if st.button(f"➕ Generate More Questions", key=f"gen_more_{std_data['standard_id']}"):
                st.info("💡 Go to 'Generate Questions' page and select this standard!")


def manage_data_page():
    """Render manage data page"""
    st.title("💾 Manage Data")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Export Questions")

        if st.session_state.questions_data:
            # Prepare export data
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_documents': len(st.session_state.questions_data),
                'documents': list(st.session_state.questions_data.values())
            }

            filename = st.text_input("Filename", "exported_questions.json")

            if st.button("💾 Save to File", type="primary"):
                if save_questions_to_file(export_data, filename):
                    st.success(f"✅ Saved to {filename}")

            # Download button
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name=filename,
                mime="application/json"
            )
        else:
            st.info("ℹ️ No questions to export")

    with col2:
        st.subheader("📥 Import Questions")

        uploaded_file = st.file_uploader("Upload JSON file", type=['json'])

        if uploaded_file:
            try:
                data = json.load(uploaded_file)

                if st.button("📥 Load Questions"):
                    # Merge with existing data
                    for doc in data.get('documents', []):
                        doc_key = f"{doc['document_info']['course_name']}_{doc['document_info']['grade_level']}"
                        st.session_state.questions_data[doc_key] = doc

                    st.success("✅ Questions imported successfully!")
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")

    st.divider()

    # Statistics
    st.subheader("📊 Statistics")

    if st.session_state.questions_data:
        stats_data = []
        for doc_key, doc_data in st.session_state.questions_data.items():
            for std_data in doc_data['standards']:
                question_types = {}
                for q in std_data['questions']:
                    q_type = q['question_type']
                    question_types[q_type] = question_types.get(q_type, 0) + 1

                stats_data.append({
                    'Document': doc_key,
                    'Standard': std_data['standard_id'],
                    'Total Questions': len(std_data['questions']),
                    'Multiple Choice': question_types.get('multiple_choice', 0),
                    'Fill in Blank': question_types.get('fill_in_blank', 0),
                    'True/False': question_types.get('true_false', 0),
                    'Short Answer': question_types.get('short_answer', 0)
                })

        df = pd.DataFrame(stats_data)
        st.dataframe(df, use_container_width=True)

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Standards", len(stats_data))
        with col2:
            st.metric("Total Questions", df['Total Questions'].sum())
        with col3:
            st.metric("Avg Questions/Standard", f"{df['Total Questions'].mean():.1f}")
        with col4:
            most_common_type = df[['Multiple Choice', 'Fill in Blank', 'True/False', 'Short Answer']].sum().idxmax()
            st.metric("Most Common Type", most_common_type)
    else:
        st.info("ℹ️ No data available")

    st.divider()

    # Clear data
    st.subheader("🗑️ Clear Data")
    st.warning("⚠️ This will remove all generated questions from memory (files will not be affected)")

    if st.button("🗑️ Clear All Questions", type="secondary"):
        st.session_state.questions_data = {}
        st.success("✅ All questions cleared!")
        st.rerun()


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()

    # Load SOL data on first run
    if st.session_state.sol_data is None:
        st.session_state.sol_data = load_sol_data()

    # Initialize generator on first run
    if st.session_state.generator is None:
        st.session_state.generator = initialize_generator()

    # Sidebar navigation
    page = sidebar_navigation()

    # Render selected page
    if page == "🏠 Home":
        home_page()
    elif page == "📖 Browse Standards":
        browse_standards_page()
    elif page == "⚡ Generate Questions":
        generate_questions_page()
    elif page == "📝 Review Questions":
        review_questions_page()
    elif page == "💾 Manage Data":
        manage_data_page()


if __name__ == "__main__":
    main()
