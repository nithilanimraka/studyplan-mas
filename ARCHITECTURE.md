# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT USER INTERFACE                             │
│                                                                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐   │
│  │   TAB 1: UPLOAD │  │ TAB 2: GENERATE  │  │   TAB 3: CHAT WITH      │   │
│  │   ASSIGNMENT    │  │  STUDY PLAN      │  │   ASSIGNMENT            │   │
│  │                 │  │                  │  │                         │   │
│  │ • PDF Upload    │  │ • Date Picker    │  │ • Chat Interface        │   │
│  │ • Text Input    │  │ • Generate Button│  │ • Message History       │   │
│  │ • View Docs     │  │ • View Plan      │  │ • Clear History         │   │
│  └────────┬────────┘  └────────┬─────────┘  └───────────┬─────────────┘   │
└───────────┼────────────────────┼────────────────────────┼──────────────────┘
            │                    │                        │
            ▼                    ▼                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                         SESSION STATE MANAGEMENT                           │
│                                                                             │
│  • uploaded_docs: List[str]          • assignment_text: str               │
│  • vector_store: VectorStore         • study_plan: str                    │
│  • chat_history: List[Dict]          • deadline: datetime                 │
└───────────────────────┬───────────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                         PROCESSING LAYER                                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    PDF PROCESSING (PyPDF)                            │ │
│  │  • Extract text from PDFs                                            │ │
│  │  • Track page numbers                                                │ │
│  │  • Preserve metadata                                                 │ │
│  └─────────────────────────┬───────────────────────────────────────────┘ │
│                              │                                             │
│  ┌─────────────────────────▼───────────────────────────────────────────┐ │
│  │              TEXT CHUNKING & EMBEDDINGS                              │ │
│  │  • RecursiveCharacterTextSplitter (1000 tokens, 200 overlap)       │ │
│  │  • OpenAI text-embedding-3-small                                     │ │
│  │  • Generate embeddings for each chunk                                │ │
│  └─────────────────────────┬───────────────────────────────────────────┘ │
│                              │                                             │
│  ┌─────────────────────────▼───────────────────────────────────────────┐ │
│  │                VECTOR STORE (ChromaDB)                               │ │
│  │  • Persistent storage to disk                                        │ │
│  │  • Cosine similarity search                                          │ │
│  │  • Metadata filtering                                                │ │
│  │  • Top-k retrieval                                                   │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         CREWAI MULTI-AGENT SYSTEM                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                    STUDY PLAN GENERATION CREW                         │ │
│  │                                                                        │ │
│  │  Agent 1: EXTRACTION AGENT                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Role: Assignment Details Analyzer                              │ │ │
│  │  │ LLM: GPT-4o (temp=0.1)                                         │ │ │
│  │  │ Task: Extract topic, requirements, objectives                  │ │ │
│  │  │ Output: Structured assignment details                          │ │ │
│  │  └────────────────────┬───────────────────────────────────────────┘ │ │
│  │                       │ (passes context to)                         │ │
│  │                       ▼                                             │ │
│  │  Agent 2: RESEARCH AGENT                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Role: Web Research Specialist                                  │ │ │
│  │  │ LLM: GPT-4o (temp=0.7)                                         │ │ │
│  │  │ Tools: SerperAPI (10 results)                                  │ │ │
│  │  │ Task: Find tutorials, courses, documentation                   │ │ │
│  │  │ Output: Categorized learning resources with URLs              │ │ │
│  │  └────────────────────┬───────────────────────────────────────────┘ │ │
│  │                       │ (passes context to)                         │ │
│  │                       ▼                                             │ │
│  │  Agent 3: PLANNING AGENT                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Role: Study Plan Architect                                     │ │ │
│  │  │ LLM: GPT-4o (temp=0.5)                                         │ │ │
│  │  │ Task: Create week-by-week study schedule                       │ │ │
│  │  │ Output: Detailed markdown-formatted study plan                 │ │ │
│  │  └────────────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                    Q&A GENERATION CREW                                │ │
│  │                                                                        │ │
│  │  Agent 4: WEB-ENHANCED RAG AGENT                                     │ │
│  │  ┌────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Role: Enhanced Research Assistant                              │ │ │
│  │  │ LLM: GPT-4o (temp=0.4)                                         │ │ │
│  │  │ Tools: RAG Tool + SerperAPI                                    │ │ │
│  │  │                                                                 │ │ │
│  │  │ Step 1: Search uploaded documents (ChromaDB)                  │ │ │
│  │  │         └─> Retrieve top 5 relevant chunks                    │ │ │
│  │  │                                                                 │ │ │
│  │  │ Step 2: Perform web search (SerperAPI)                        │ │ │
│  │  │         └─> Get current online information                     │ │ │
│  │  │                                                                 │ │ │
│  │  │ Step 3: Synthesize answer                                      │ │ │
│  │  │         └─> Combine document + web sources                     │ │ │
│  │  │         └─> Cite page numbers and URLs                        │ │ │
│  │  │                                                                 │ │ │
│  │  │ Output: Comprehensive answer with citations                    │ │ │
│  │  └────────────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                                  │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │
│  │   OPENAI API     │  │   SERPER API     │  │   FILE SYSTEM        │   │
│  │                  │  │                  │  │                      │   │
│  │ • GPT-4o        │  │ • Web Search     │  │ • PDF Storage        │   │
│  │ • Embeddings    │  │ • 10 results     │  │ • Vector DB          │   │
│  │ • Rate limits   │  │ • Free tier      │  │ • Outputs            │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                          │
│                                                                             │
│  UPLOAD FLOW:                                                              │
│  PDF/Text → PyPDF → Chunking → Embeddings → ChromaDB                     │
│                                                                             │
│  STUDY PLAN FLOW:                                                          │
│  Assignment Text → Extraction Agent → Research Agent → Planning Agent     │
│      ↓               ↓                    ↓                 ↓             │
│  Deadline        Topic/Reqs          Resources          Study Plan        │
│                                                                             │
│  Q&A FLOW:                                                                 │
│  Question → RAG Agent → [ChromaDB Search + Web Search] → GPT-4o → Answer │
│                            ↓              ↓                                │
│                      Documents        Web Results                          │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         CONFIGURATION & SETTINGS                           │
│                                                                             │
│  Environment Variables (.env):                                             │
│  • OPENAI_API_KEY          • SERPER_API_KEY                              │
│  • OPENAI_MODEL=gpt-4o     • EMBEDDING_MODEL=text-embedding-3-small     │
│  • CHUNK_SIZE=1000         • CHUNK_OVERLAP=200                           │
│  • MAX_UPLOAD_SIZE_MB=10   • CHROMA_PERSIST_DIR=./data/vectorstore      │
│                                                                             │
│  Directory Structure:                                                      │
│  • data/uploads/          → Temporary PDF storage                         │
│  • data/vectorstore/      → ChromaDB persistence                          │
│  • data/outputs/          → Generated study plans                         │
│  • src/agents/            → Agent definitions                             │
│  • src/crews/             → Crew orchestration                            │
│  • src/tools/             → Custom tools                                  │
│  • src/utils/             → Utility functions                             │
│  • streamlit_app/         → UI application                                │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                         ERROR HANDLING & LOGGING                           │
│                                                                             │
│  • Loguru: Structured logging throughout                                  │
│  • Try-catch blocks in all critical sections                              │
│  • User-friendly error messages in Streamlit                              │
│  • API error handling (rate limits, timeouts)                             │
│  • Validation: file types, sizes, date ranges                             │
└───────────────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### Frontend Layer (Streamlit)
- **3-Tab Interface**: Clear separation of concerns
- **Session State**: Persistent data across interactions
- **Caching**: Vector store and crews cached with `@st.cache_resource`
- **Progress Indicators**: Spinners and status messages

### Processing Layer
- **PDF Processor**: Extracts text with page tracking
- **Embedding Manager**: Chunks text and generates embeddings
- **Vector Store**: ChromaDB for semantic search

### Agent Layer (CrewAI)
- **4 Specialized Agents**: Each with specific role and tools
- **Sequential Execution**: Tasks run in order with context passing
- **Memory**: Crew memory enabled for context retention

### External Services
- **OpenAI**: GPT-4o for reasoning, text-embedding-3-small for vectors
- **SerperAPI**: Web search with 10 results per query
- **File System**: Local storage for PDFs and vector DB

## Data Flow Patterns

### 1. Document Upload
```
User uploads PDF → Save to disk → Extract text → 
Chunk into 1000-token segments → Generate embeddings → 
Store in ChromaDB with metadata
```

### 2. Study Plan Generation
```
User provides assignment + deadline → 
Extraction Agent analyzes text → 
Research Agent searches web → 
Planning Agent creates schedule → 
Display formatted plan
```

### 3. Question Answering
```
User asks question → 
Search ChromaDB (top 5 chunks) + 
Search web (SerperAPI) → 
GPT-4o synthesizes answer → 
Display with citations
```

## Performance Characteristics

- **PDF Processing**: ~1-2 seconds per page
- **Embedding Generation**: ~2-3 seconds per document
- **Study Plan**: 60-120 seconds total
- **Chat Response**: 15-30 seconds per query
- **Vector Search**: <1 second
- **Web Search**: 3-5 seconds

## Security Features

- ✅ API keys stored in .env (not in code)
- ✅ .gitignore prevents committing secrets
- ✅ Input validation on file uploads
- ✅ No external data transmission (except APIs)
- ✅ Local vector store (data stays on machine)
