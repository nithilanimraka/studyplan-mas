"""
Test script to verify all components are working correctly.
Run this after installation to check if everything is set up properly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    try:
        import crewai
        print(f"  ✅ CrewAI v{crewai.__version__}")
    except ImportError as e:
        print(f"  ❌ CrewAI import failed: {e}")
        return False
    
    try:
        import streamlit
        print(f"  ✅ Streamlit v{streamlit.__version__}")
    except ImportError as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print(f"  ✅ OpenAI v{openai.__version__}")
    except ImportError as e:
        print(f"  ❌ OpenAI import failed: {e}")
        return False
    
    try:
        import chromadb
        print(f"  ✅ ChromaDB v{chromadb.__version__}")
    except ImportError as e:
        print(f"  ❌ ChromaDB import failed: {e}")
        return False
    
    try:
        import langchain
        print(f"  ✅ LangChain v{langchain.__version__}")
    except ImportError as e:
        print(f"  ❌ LangChain import failed: {e}")
        return False
    
    return True


def test_config():
    """Test if configuration is properly set up."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config.settings import OPENAI_API_KEY, SERPER_API_KEY
        
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-key-here":
            print("  ⚠️  OPENAI_API_KEY not set properly in .env")
            return False
        else:
            print(f"  ✅ OPENAI_API_KEY configured (starts with: {OPENAI_API_KEY[:10]}...)")
        
        if not SERPER_API_KEY or SERPER_API_KEY == "your-key-here":
            print("  ⚠️  SERPER_API_KEY not set properly in .env")
            return False
        else:
            print(f"  ✅ SERPER_API_KEY configured (starts with: {SERPER_API_KEY[:10]}...)")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False


def test_directories():
    """Test if required directories exist."""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = [
        "data/uploads",
        "data/vectorstore",
        "data/outputs",
        "src/agents",
        "src/tools",
        "src/utils",
        "src/crews",
        "streamlit_app"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} not found")
            all_exist = False
    
    return all_exist


def test_utils():
    """Test utility modules."""
    print("\n🔍 Testing utility modules...")
    
    try:
        from src.utils.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        print("  ✅ PDF Processor initialized")
    except Exception as e:
        print(f"  ❌ PDF Processor failed: {e}")
        return False
    
    try:
        from src.utils.embeddings import EmbeddingManager
        # Don't actually initialize to avoid API calls
        print("  ✅ Embedding Manager imported")
    except Exception as e:
        print(f"  ❌ Embedding Manager failed: {e}")
        return False
    
    try:
        from src.utils.vector_store import VectorStore
        # Don't actually initialize to avoid creating db
        print("  ✅ Vector Store imported")
    except Exception as e:
        print(f"  ❌ Vector Store failed: {e}")
        return False
    
    return True


def test_agents():
    """Test agent modules."""
    print("\n🔍 Testing agent modules...")
    
    try:
        from src.agents.extraction_agent import create_extraction_agent
        from src.agents.research_agent import create_research_agent
        from src.agents.planning_agent import create_planning_agent
        from src.agents.rag_agent import create_rag_agent
        from src.agents.web_rag_agent import create_web_rag_agent
        print("  ✅ All agent modules imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Agent modules failed: {e}")
        return False


def test_tools():
    """Test tool modules."""
    print("\n🔍 Testing tool modules...")
    
    try:
        from src.tools.web_search_tool import search_tool
        print("  ✅ Web Search Tool imported")
    except Exception as e:
        print(f"  ❌ Web Search Tool failed: {e}")
        return False
    
    try:
        from src.tools.pdf_tool import pdf_tool
        print("  ✅ PDF Tool imported")
    except Exception as e:
        print(f"  ❌ PDF Tool failed: {e}")
        return False
    
    try:
        from src.tools.rag_tool import get_rag_tool
        print("  ✅ RAG Tool imported")
    except Exception as e:
        print(f"  ❌ RAG Tool failed: {e}")
        return False
    
    return True


def test_crews():
    """Test crew modules."""
    print("\n🔍 Testing crew modules...")
    
    try:
        from src.crews.study_plan_crew import StudyPlanCrew
        from src.crews.rag_crew import RAGCrew
        print("  ✅ All crew modules imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Crew modules failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Assignment Study Plan System - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Directory Structure", test_directories()))
    results.append(("Utility Modules", test_utils()))
    results.append(("Agent Modules", test_agents()))
    results.append(("Tool Modules", test_tools()))
    results.append(("Crew Modules", test_crews()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("\nTo run the application:")
        print("  ./run.sh")
        print("  or: streamlit run streamlit_app/app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("  - Missing .env file: cp .env.example .env")
        print("  - API keys not set: Edit .env and add your keys")
        print("  - Packages not installed: ./setup.sh")
        return 1


if __name__ == "__main__":
    sys.exit(main())
