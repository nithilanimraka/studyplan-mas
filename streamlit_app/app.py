"""
Multi-Agent Study Plan Generator
A CrewAI-powered application for generating personalized study plans and intelligent Q&A.
"""

import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path
import time
import io
from contextlib import redirect_stdout, redirect_stderr
import queue
import threading

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import UPLOADS_DIR, MAX_UPLOAD_SIZE_MB
from src.utils.pdf_processor import PDFProcessor
from src.utils.vector_store import VectorStore
from src.crews.study_plan_crew import StudyPlanCrew
from src.crews.rag_crew import RAGCrew
from loguru import logger

# Configure page
st.set_page_config(
    page_title="Multi Agentic Assignment Plan Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 500;
    }
    .agent-log {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        line-height: 1.5;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .agent-name {
        color: #4ec9b0;
        font-weight: bold;
    }
    .task-name {
        color: #dcdcaa;
        font-weight: bold;
    }
    .thinking {
        color: #ce9178;
    }
    .tool-use {
        color: #9cdcfe;
    }
    .status-completed {
        color: #6a9955;
    }
    .status-executing {
        color: #569cd6;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if "uploaded_docs" not in st.session_state:
        st.session_state.uploaded_docs = []
    
    if "assignment_text" not in st.session_state:
        st.session_state.assignment_text = ""
    
    if "study_plan" not in st.session_state:
        st.session_state.study_plan = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "deadline" not in st.session_state:
        st.session_state.deadline = None
    
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []


class OutputCapture:
    """Capture stdout/stderr for CrewAI verbose output."""
    
    def __init__(self):
        self.logs = []
        self.output_queue = queue.Queue()
        
    def write(self, text):
        """Capture written text."""
        if text and text.strip():
            self.logs.append(text)
            self.output_queue.put(text)
    
    def flush(self):
        """Flush (required for file-like object)."""
        pass
    
    def get_formatted_logs(self):
        """Get formatted HTML logs."""
        formatted_lines = []
        
        # Keep last 100 lines (using correct slice notation)
        recent_logs = self.logs[-100:] if len(self.logs) > 100 else self.logs
        
        for log in recent_logs:
            line = log.strip()
            if not line:
                continue
            
            # Format based on content
            if "Agent:" in line or "Working Agent:" in line:
                formatted = f'<span class="agent-name">🤖 {line}</span>'
            elif "Task:" in line:
                formatted = f'<span class="task-name">📋 {line}</span>'
            elif "Thought:" in line or "I need to" in line or "I should" in line:
                formatted = f'<span class="thinking">💭 {line}</span>'
            elif "Using Tool" in line or "Tool:" in line or "Action:" in line:
                formatted = f'<span class="tool-use">🔧 {line}</span>'
            elif "Observation:" in line or "Result:" in line:
                formatted = f'<span class="tool-use">📊 {line}</span>'
            elif "Final Answer:" in line or "Finished chain" in line:
                formatted = f'<span class="status-completed">✅ {line}</span>'
            elif "Entering new" in line or "Starting" in line:
                formatted = f'<span class="status-executing">⚙️ {line}</span>'
            else:
                formatted = f'<span style="color: #d4d4d4;">{line}</span>'
            
            formatted_lines.append(formatted)
        
        if not formatted_lines:
            return '<div class="agent-log"><span style="color: #888;">Waiting for agents to start...</span></div>'
        
        content = "<br>".join(formatted_lines)
        return f'<div class="agent-log">{content}</div>'


@st.cache_resource
def get_vector_store():
    """Get cached vector store instance."""
    return VectorStore()


@st.cache_resource
def get_study_plan_crew():
    """Get cached study plan crew instance."""
    return StudyPlanCrew()


@st.cache_resource
def get_rag_crew(_vector_store):
    """Get cached RAG crew instance."""
    return RAGCrew(_vector_store)


def process_pdf(uploaded_file):
    """Process uploaded PDF file."""
    try:
        # Save file temporarily
        file_path = UPLOADS_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text
        processor = PDFProcessor()
        result = processor.extract_text_from_pdf(str(file_path))
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise


def run_crew_with_logs(crew_func, *args, **kwargs):
    """Run crew function and capture verbose output."""
    # Create expandable section for logs
    log_expander = st.expander("🔍 View Agent Thought Process", expanded=True)
    
    with log_expander:
        log_container = st.empty()
        progress_text = st.empty()
        
        # Create output capture
        capture = OutputCapture()
        
        # Show initial message
        progress_text.info("🤖 AI agents are working... Check the thought process below!")
        
        def run_with_capture():
            """Run function with output capture."""
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            try:
                # Redirect stdout and stderr
                sys.stdout = capture
                sys.stderr = capture
                
                # Execute crew function
                return crew_func(*args, **kwargs)
                
            finally:
                # Restore stdout/stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        
        # Run in thread and update UI periodically
        result_container = {'result': None, 'error': None}
        
        def execute():
            try:
                result_container['result'] = run_with_capture()
            except Exception as e:
                result_container['error'] = e
        
        # Start execution thread
        thread = threading.Thread(target=execute)
        thread.start()
        
        # Update logs while thread is running
        while thread.is_alive():
            # Get new logs from queue
            try:
                while True:
                    capture.output_queue.get_nowait()
            except queue.Empty:
                pass
            
            # Update display
            log_container.markdown(capture.get_formatted_logs(), unsafe_allow_html=True)
            time.sleep(0.5)
        
        thread.join()
        
        # Final update
        log_container.markdown(capture.get_formatted_logs(), unsafe_allow_html=True)
        
        # Store logs
        st.session_state.agent_logs = capture.logs
        
        # Check for errors
        if result_container['error']:
            progress_text.error(f"❌ Error: {str(result_container['error'])}")
            raise result_container['error']
        
        # Show completion
        progress_text.success("✅ Process completed! Review the agent thought process above.")
        
        return result_container['result']


def main():
    """Main application function."""
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">📚 AI Study Plan Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Powered by CrewAI, GPT-4o, and SerperAPI</div>', 
        unsafe_allow_html=True
    )
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "📤 Upload Assignment", 
        "📅 Generate Study Plan", 
        "💬 Chat with Assignment"
    ])
    
    # Tab 1: Upload Assignment
    with tab1:
        st.header("Upload Assignment Materials")
        st.write("Upload your assignment document (PDF) or paste the text directly.")
        
        # File upload
        st.subheader("📄 Upload PDF")
        uploaded_files = st.file_uploader(
            "Choose PDF file(s)",
            type=['pdf'],
            accept_multiple_files=True,
            help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB}MB per file"
        )
        
        if uploaded_files:
            with st.spinner("Processing PDF files..."):
                try:
                    all_text = []
                    all_chunks = []
                    
                    for uploaded_file in uploaded_files:
                        # Process PDF
                        result = process_pdf(uploaded_file)
                        all_text.append(result['full_text'])
                        
                        # Update vector store
                        if st.session_state.vector_store is None:
                            st.session_state.vector_store = get_vector_store()
                        
                        # Chunk and add to vector store
                        from src.utils.embeddings import EmbeddingManager
                        embedding_mgr = EmbeddingManager()
                        chunks = embedding_mgr.chunk_pages(
                            result['pages'], 
                            result['metadata']
                        )
                        all_chunks.extend(chunks)
                        
                        st.session_state.uploaded_docs.append(uploaded_file.name)
                    
                    # Add all chunks to vector store
                    st.session_state.vector_store.add_documents(all_chunks)
                    
                    # Store combined text
                    st.session_state.assignment_text = "\n\n".join(all_text)
                    
                    st.success(f"✅ Successfully processed {len(uploaded_files)} PDF file(s)!")
                    st.info(f"📊 Total chunks in vector store: {st.session_state.vector_store.get_collection_count()}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")
        
        # Text input
        st.subheader("📝 Or Paste Assignment Text")
        text_input = st.text_area(
            "Paste your assignment description here",
            height=200,
            placeholder="Enter your assignment details, requirements, and instructions..."
        )
        
        if text_input:
            st.session_state.assignment_text = text_input
            
            # Add to vector store
            if st.session_state.vector_store is None:
                st.session_state.vector_store = get_vector_store()
            
            try:
                from src.utils.embeddings import EmbeddingManager
                embedding_mgr = EmbeddingManager()
                chunks = embedding_mgr.chunk_text(
                    text_input, 
                    {"source": "manual_input", "file_name": "User Input"}
                )
                st.session_state.vector_store.add_documents(chunks)
                st.success("✅ Text saved and indexed!")
            except Exception as e:
                st.error(f"❌ Error indexing text: {str(e)}")
        
        # Display current assignment
        if st.session_state.assignment_text:
            st.subheader("📋 Current Assignment")
            with st.expander("View assignment text", expanded=False):
                st.text_area(
                    "Assignment content",
                    value=st.session_state.assignment_text,
                    height=200,
                    disabled=True
                )
            
            if st.button("🗑️ Clear Assignment Data"):
                st.session_state.assignment_text = ""
                st.session_state.uploaded_docs = []
                if st.session_state.vector_store:
                    st.session_state.vector_store.clear_collection()
                st.success("✅ Assignment data cleared!")
                st.rerun()
    
    # Tab 2: Generate Study Plan
    with tab2:
        st.header("Generate Personalized Study Plan")
        
        if not st.session_state.assignment_text:
            st.warning("⚠️ Please upload or enter assignment details in the 'Upload Assignment' tab first.")
        else:
            # Deadline input
            col1, col2 = st.columns(2)
            
            with col1:
                deadline_date = st.date_input(
                    "📅 Assignment Deadline (Date)",
                    value=datetime.now() + timedelta(days=14),
                    min_value=datetime.now().date(),
                    help="Select the due date for your assignment"
                )
            
            with col2:
                deadline_time = st.time_input(
                    "⏰ Deadline Time",
                    value=datetime.now().replace(hour=23, minute=59).time(),
                    help="Select the due time"
                )
            
            # Combine date and time
            deadline_datetime = datetime.combine(deadline_date, deadline_time)
            days_remaining = (deadline_datetime - datetime.now()).days
            
            st.info(f"⏳ Days remaining: **{days_remaining}** days")
            
            # Generate button
            if st.button("🚀 Generate Study Plan", type="primary", use_container_width=True):
                try:
                    # Get crew and generate plan with log capture
                    crew = get_study_plan_crew()
                    
                    result = run_crew_with_logs(
                        crew.generate_study_plan,
                        assignment_text=st.session_state.assignment_text,
                        deadline=deadline_datetime
                    )
                    
                    if result["success"]:
                        st.session_state.study_plan = result["study_plan"]
                        st.session_state.deadline = result["deadline"]
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {result['error']}")
                
                except Exception as e:
                    st.error(f"❌ Error generating study plan: {str(e)}")
                    logger.error(f"Study plan generation error: {str(e)}")
            
            # Display study plan
            if st.session_state.study_plan:
                st.subheader("📅 Your Personalized Study Plan")
                st.markdown("---")
                st.markdown(str(st.session_state.study_plan))
                
                # Download button
                st.download_button(
                    label="📥 Download Study Plan",
                    data=str(st.session_state.study_plan),
                    file_name=f"study_plan_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    
    # Tab 3: Chat with Assignment
    with tab3:
        st.header("Chat with Your Assignment")
        st.write("Ask questions about your assignment materials. Answers are enhanced with web research.")
        
        if not st.session_state.assignment_text and not st.session_state.vector_store:
            st.warning("⚠️ Please upload assignment materials in the 'Upload Assignment' tab first.")
        else:
            # Display chat history
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask a question about your assignment..."):
                # Add user message to chat
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get AI response
                with st.chat_message("assistant"):
                    try:
                        # Get RAG crew and answer with log capture
                        rag_crew = get_rag_crew(st.session_state.vector_store)
                        
                        result = run_crew_with_logs(
                            rag_crew.answer_question,
                            prompt
                        )
                        
                        if result["success"]:
                            answer = str(result["answer"])
                            st.markdown(answer)
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": answer
                            })
                        else:
                            error_msg = f"❌ Error: {result['error']}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": error_msg
                            })
                    
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        logger.error(f"Chat error: {str(e)}")
            
            # Clear chat button
            if st.session_state.chat_history and st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This application uses **CrewAI** with multiple AI agents to:
        
        1. 🔍 **Extract** assignment details using GPT-4o
        2. 🌐 **Research** study resources via SerperAPI
        3. 📋 **Plan** personalized study schedules
        4. 💬 **Answer** questions using RAG + web search
        
        **Agents:**
        - Assignment Analyzer
        - Web Research Specialist  
        - Study Plan Architect
        - Enhanced Q&A Assistant
        """)
        
        st.markdown("---")
        
        st.header("📊 Status")
        st.metric("Documents Uploaded", len(st.session_state.uploaded_docs))
        if st.session_state.vector_store:
            st.metric("Chunks Indexed", st.session_state.vector_store.get_collection_count())
        st.metric("Chat Messages", len(st.session_state.chat_history))
        
        st.markdown("---")
        st.caption("Powered by CrewAI, OpenAI GPT-4o, and SerperAPI")


if __name__ == "__main__":
    main()
