# 🎓 Assignment Study Plan Generator - Complete Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Usage Guide](#usage-guide)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)
7. [API Costs](#api-costs)

---

## 🚀 Quick Start

### Installation (3 Steps)

1. **Run setup script:**
```bash
./setup.sh
```

2. **Configure API keys:**
```bash
cp .env.example .env
# Edit .env file and add your keys:
# OPENAI_API_KEY=sk-...
# SERPER_API_KEY=...
```

3. **Launch application:**
```bash
./run.sh
```

The app will open in your browser at `http://localhost:8501`

---

## ✨ Features

### 1. 📤 Upload Assignment Materials
- **PDF Upload**: Support for single or multiple PDF files
- **Text Input**: Paste assignment text directly
- **Automatic Indexing**: Content is automatically vectorized and stored
- **Multi-document Support**: Upload multiple PDFs for comprehensive coverage

### 2. 📅 Generate Personalized Study Plans
- **Deadline Tracking**: Set exact deadline (date + time)
- **Automatic Analysis**: GPT-4o extracts key assignment details
- **Web Research**: Finds best learning resources via SerperAPI
- **Smart Planning**: Creates week-by-week study schedule with:
  - Learning objectives
  - Daily tasks
  - Resource recommendations
  - Time estimates
  - Milestones
- **Export**: Download plan as Markdown file

### 3. 💬 Chat with Your Assignment
- **RAG-Powered**: Ask questions about uploaded materials
- **Web-Enhanced**: Every answer includes fresh web research
- **Source Citations**: See exact page numbers and URLs
- **Chat History**: Full conversation history maintained
- **Context-Aware**: Understands follow-up questions

---

## 🔧 How It Works

### Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Study Plan Workflow                  │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. Extraction Agent (GPT-4o)                       │
│     └─> Analyzes assignment text                    │
│         └─> Extracts: topic, requirements, details  │
│                                                       │
│  2. Research Agent (GPT-4o + SerperAPI)            │
│     └─> Searches web for learning resources         │
│         └─> Finds: tutorials, courses, articles     │
│                                                       │
│  3. Planning Agent (GPT-4o)                         │
│     └─> Creates personalized study plan             │
│         └─> Uses: extracted details + research      │
│                                                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  Q&A Workflow                        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. Document Search (ChromaDB)                       │
│     └─> Semantic search in uploaded PDFs            │
│         └─> Returns: top 5 relevant chunks           │
│                                                       │
│  2. Web Search (SerperAPI)                          │
│     └─> Finds additional context online             │
│         └─> Returns: current information            │
│                                                       │
│  3. Answer Synthesis (GPT-4o)                       │
│     └─> Combines both sources                        │
│         └─> Provides: comprehensive answer + sources │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

- **LLM**: OpenAI GPT-4o (reasoning & generation)
- **Embeddings**: text-embedding-3-small (vector search)
- **Vector DB**: ChromaDB (document storage & retrieval)
- **Web Search**: SerperAPI (real-time information)
- **Framework**: CrewAI (multi-agent orchestration)
- **UI**: Streamlit (user interface)
- **PDF**: PyPDF (text extraction)

---

## 📖 Usage Guide

### Tab 1: Upload Assignment 📤

#### Option A: Upload PDF
1. Click "Choose PDF file(s)"
2. Select one or more PDF files
3. Wait for processing (shows progress)
4. See confirmation: "✅ Successfully processed X PDF file(s)!"

#### Option B: Paste Text
1. Scroll to "Or Paste Assignment Text"
2. Paste your assignment description
3. Text is automatically indexed

#### View Uploaded Content
- Click "View assignment text" expander to review
- See document count and chunk statistics in sidebar
- Click "Clear Assignment Data" to start over

### Tab 2: Generate Study Plan 📅

#### Step 1: Set Deadline
1. **Date**: Use calendar picker (must be future date)
2. **Time**: Set specific deadline time
3. View "Days remaining" indicator

#### Step 2: Generate Plan
1. Click "🚀 Generate Study Plan" button
2. Wait 1-3 minutes while agents work:
   - Extracting assignment details...
   - Researching learning resources...
   - Creating personalized plan...
3. View generated plan (formatted with emojis and sections)

#### Step 3: Download Plan
- Click "📥 Download Study Plan"
- Saves as `study_plan_YYYYMMDD.md`

### Tab 3: Chat with Assignment 💬

#### Ask Questions
1. Type question in chat input
2. Press Enter or click send
3. Wait for response (15-30 seconds)
4. View answer with sources

#### Example Questions
- "What are the main requirements of this assignment?"
- "Explain the concept of [topic] mentioned in the materials"
- "What resources can help me learn [topic]?"
- "How should I approach this problem?"
- "What are the evaluation criteria?"

#### Tips for Best Results
- Be specific in your questions
- Reference specific topics from your materials
- Ask follow-up questions for clarification
- Check cited sources for more details

---

## 💡 Examples

### Example 1: Computer Science Assignment

**Assignment**: "Create a web application using React and Node.js that implements user authentication and a REST API."

**Generated Study Plan** (excerpt):
```markdown
## Week 1: React Fundamentals
- Learn React basics (components, state, props)
- Build simple React app
- **Resources**: 
  - React Official Tutorial
  - FreeCodeCamp React Course
- **Time**: 10 hours

## Week 2: Node.js & Express
- Set up Node.js environment
- Create REST API with Express
- Implement routing and middleware
- **Resources**:
  - Node.js Documentation
  - Express.js Guide
- **Time**: 12 hours
```

**Chat Example**:
> **User**: "How do I implement JWT authentication?"
> 
> **Assistant**: Based on your course materials (Page 15), JWT authentication involves:
> 1. User sends credentials to server
> 2. Server validates and generates JWT token
> 3. Token is sent back to client
> 4. Client includes token in subsequent requests
> 
> Additionally, from web research:
> - Use libraries like `jsonwebtoken` (Node.js)
> - Store tokens securely in httpOnly cookies
> - Implement token refresh mechanism
> - [Tutorial: JWT Authentication in Node.js](https://jwt.io)

### Example 2: Business Assignment

**Assignment**: "Analyze the impact of digital transformation on retail businesses"

**Generated Study Plan** (excerpt):
```markdown
## Research Phase (Days 1-3)
- Define digital transformation in retail context
- Identify key technologies (AI, IoT, AR/VR)
- Research case studies: Amazon, Walmart, Alibaba
- **Resources**:
  - Harvard Business Review articles
  - McKinsey Digital Reports
  - Academic papers on retail innovation

## Analysis Phase (Days 4-7)
- Framework: SWOT analysis of digital transformation
- Impact areas: customer experience, supply chain, operations
- Create comparison matrices
- **Resources**:
  - Business analysis frameworks
  - Industry reports
```

---

## 🔍 Troubleshooting

### Issue: "OPENAI_API_KEY is not set"

**Solution**:
```bash
# Check if .env exists
ls -la .env

# If not, create it
cp .env.example .env

# Edit and add your key
nano .env
```

### Issue: "No module named 'crewai'"

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Study plan generation takes too long

**Reasons**:
- Web research can take 30-60 seconds
- GPT-4o processing takes time
- This is normal for complex assignments

**Tips**:
- Be patient, watch progress indicators
- Don't refresh the page
- Simpler assignments = faster generation

### Issue: Chat responses are slow

**Reasons**:
- Vector search + web search + GPT-4o
- Each step takes 5-10 seconds

**Normal timing**:
- Simple questions: 15-20 seconds
- Complex questions: 30-45 seconds

### Issue: "Rate limit exceeded"

**Solution**:
- Wait 60 seconds and try again
- Check your OpenAI API rate limits
- Consider upgrading API tier

### Issue: Vector store errors

**Solution**:
```bash
# Clear vector store
rm -rf data/vectorstore/*

# Restart app and re-upload documents
```

---

## 💰 API Costs

### OpenAI GPT-4o Pricing
- **Input**: $2.50 per 1M tokens
- **Output**: $10.00 per 1M tokens

### SerperAPI Pricing
- **Free Tier**: 2,500 searches/month
- **Paid**: $0.003 per search after free tier

### Estimated Costs Per Use

#### Study Plan Generation
| Component | Tokens | Cost |
|-----------|--------|------|
| Assignment extraction | 500-1000 | $0.001-0.002 |
| Web research | 1000-2000 | $0.002-0.005 |
| Plan generation | 2000-4000 | $0.02-0.04 |
| **Total** | **3500-7000** | **$0.03-$0.05** |

#### Chat Query
| Component | Tokens | Cost |
|-----------|--------|------|
| Document retrieval | 500-1000 | $0.001-0.002 |
| Web search | 500-1000 | $0.001-0.002 |
| Answer generation | 500-1500 | $0.005-0.015 |
| **Total** | **1500-3500** | $0.007-$0.02 |

### Monthly Budget Estimate
- **10 study plans**: $0.30-0.50
- **50 chat queries**: $0.35-1.00
- **Web searches**: Free (within 2,500/month)
- **Total**: **~$1-2/month** for typical student use

---

## 🎯 Best Practices

### For Study Plans
1. **Upload comprehensive materials**: More context = better plans
2. **Set realistic deadlines**: Give yourself adequate time
3. **Review and adjust**: Plans are starting points, customize as needed
4. **Download and save**: Keep plans for reference

### For Chat
1. **Upload relevant documents first**: Better context = better answers
2. **Ask specific questions**: Avoid vague queries
3. **Check sources**: Verify information from citations
4. **Build on previous questions**: Use chat history for context

### For Performance
1. **Don't upload huge PDFs**: Keep under 10MB per file
2. **Clear old documents**: Remove when done with assignment
3. **Use descriptive filenames**: Helps with source citations
4. **One assignment at a time**: Clear data between assignments

---

## 📞 Support

### Common Questions

**Q: Can I use this for multiple assignments?**  
A: Yes! Clear data between assignments using the "Clear Assignment Data" button.

**Q: Are my documents stored permanently?**  
A: Documents are stored locally in `data/vectorstore/`. Clear them when done.

**Q: Can I export chat history?**  
A: Not currently, but you can copy/paste from the chat interface.

**Q: Does it work offline?**  
A: No, requires internet for OpenAI and SerperAPI.

**Q: What file formats are supported?**  
A: PDF and text input. For other formats, convert to PDF first.

---

## 🎉 Tips for Success

1. **Start early**: Generate study plan as soon as you get assignment
2. **Upload all materials**: Lecture notes, textbooks, assignment brief
3. **Use chat frequently**: Ask questions as you study
4. **Review sources**: Click through to recommended resources
5. **Customize plans**: Adjust based on your learning pace
6. **Track progress**: Mark off completed tasks
7. **Ask follow-ups**: Get clarification on unclear points

---

## 📚 Additional Resources

- **CrewAI Documentation**: https://docs.crewai.com
- **OpenAI API Reference**: https://platform.openai.com/docs
- **SerperAPI Guide**: https://serper.dev/docs
- **Streamlit Docs**: https://docs.streamlit.io

---

**Made with ❤️ using CrewAI, OpenAI GPT-4o, and SerperAPI**

*Last updated: November 2025*
