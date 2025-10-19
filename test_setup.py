"""
Quick test script to verify the SOL Quiz Generator setup
Run this to ensure all dependencies are installed and configured correctly
"""

import sys
import os


def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    try:
        import openai
        print("  ✓ openai installed")
    except ImportError:
        print("  ✗ openai not installed. Run: pip install -r requirements.txt")
        return False

    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv installed")
    except ImportError:
        print("  ✗ python-dotenv not installed. Run: pip install -r requirements.txt")
        return False

    return True


def test_env_file():
    """Test that .env file exists and has API key"""
    print("\nTesting environment configuration...")

    if not os.path.exists(".env"):
        print("  ✗ .env file not found")
        print("    Create .env file: cp .env.example .env")
        print("    Then add your OpenAI API key")
        return False

    print("  ✓ .env file exists")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("  ✗ OPENAI_API_KEY not set in .env")
        print("    Edit .env and add your OpenAI API key")
        return False

    print("  ✓ OPENAI_API_KEY is set")
    return True


def test_data_file():
    """Test that SOL data file exists"""
    print("\nTesting data file...")

    if not os.path.exists("all_structured_documents.json"):
        print("  ✗ all_structured_documents.json not found")
        return False

    print("  ✓ all_structured_documents.json exists")

    try:
        import json
        with open("all_structured_documents.json", 'r') as f:
            data = json.load(f)
            print(f"  ✓ Data file is valid JSON with {data.get('total_documents', 0)} documents")
    except Exception as e:
        print(f"  ✗ Error reading data file: {e}")
        return False

    return True


def test_module_import():
    """Test that the main module can be imported"""
    print("\nTesting SOL Quiz Generator module...")

    try:
        from sol_quiz_generator import SOLQuizGenerator, QuestionType
        print("  ✓ Module imports successfully")

        # Try to instantiate (will fail if no API key, but that's expected)
        try:
            generator = SOLQuizGenerator()
            print("  ✓ SOLQuizGenerator can be instantiated")
            return True
        except ValueError as e:
            if "API key" in str(e):
                print("  ⚠ SOLQuizGenerator needs API key (expected if .env not configured)")
                return True
            raise

    except Exception as e:
        print(f"  ✗ Error importing module: {e}")
        return False


def run_all_tests():
    """Run all setup tests"""
    print("=" * 60)
    print("SOL Quiz Generator - Setup Test")
    print("=" * 60)

    tests = [
        ("Package Dependencies", test_imports),
        ("Environment Configuration", test_env_file),
        ("Data File", test_data_file),
        ("Module Import", test_module_import),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ All tests passed! You're ready to generate quiz questions.")
        print("\nNext steps:")
        print("  1. Run example: python example_usage.py")
        print("  2. Or use the main script: python sol_quiz_generator.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
