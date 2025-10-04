# ShambhaviSharma-langsmith-MAT496
Intro to langsmith for course MAT496, Roll Number- 2410110313

## MODULE 1 
## LESSON 1: Tracing Concepts in LangSmith

- **Projects**: Containers that group multiple traces.  
  - Example: Our project is a RAG application.

- **Runs**: A single unit of work (e.g., model call, retriever, tool, or sub-chain).

- **Traces**: A collection of runs representing the full end-to-end execution of a request.  
  - In short:  
    - Trace = full program execution  
    - Run = each unit of work  
  - Example in RAG:  
    - Run 1: Retrieve documents  
    - Run 2: Generate response  

- **@traceable Decorator**:  
  - Automatically traces functions.  
  - Logs inputs, outputs, errors, and metadata.  
  - Enables detailed observability and debugging.

- **Debugging with Tracing**:  
  - Replay exact sequence of operations.  
  - Identify issues like unexpected outputs or failures.

### Changes Made
1. Replaced OpenAI calls with Claude.  
2. Modified `utils` to use HuggingFace embeddings instead of OpenAI.  
3. Updated last cell in `tracing_basics.ipynb` for better RAG testing.  

### LangSmith Interface
- Provides visual view of traced runs and execution flow.

## Lesson 2: Types of Runs  

This lesson explains the different **types of runs** in an LLM application and how they appear in a trace.  

- **Chain Runs** → represent the overall workflow  
- **Tool Runs** → represent external calls/tools within the chain  
- **LLM Runs** → represent direct calls to the language model  

### Why It Matters  
- Helps distinguish workflow steps for **debugging** and **optimization**  
- Run hierarchy pinpoints **errors or bottlenecks**  
- Traces can be **filtered by run type** for focused inspection

## LESSON 3 ALTERNATIVE WAYS TO TRACE
## Summary: Alternative Methods for Tracing

- **Tracing Options**:  
  - Built-in LangChain tracing  
  - **OpenTelemetry** (open-source tracing framework)  
  - **Phoenix** (visual interface for exploring traces and chains)  

- **Changes Made**:  
  - Replaced `wrap_openai()` with `wrap_anthropic()` for compatibility with Anthropic instead of OpenAI.  
  - Updated multiple code sections to avoid OpenAI dependencies.  

### Key Approaches
1. **Context Manager (`with trace()`)**  
   - Provides custom control over logged data.  
   - Allows manual setting of inputs/outputs.  
   - Useful for non-standard code flows.  

2. **Wrapper (`wrap_anthropic`)**  
   - Enables automatic tracing by wrapping the client.  
   - Example: `wrap_anthropic(Anthropic())`.  
   - Works alongside `@traceable` for function-level tracing.  

3. **RunTree API**  
   - Offers maximum flexibility by manually creating parent/child runs.  
   - Suitable for custom frameworks or highly specific tracing needs.  


## Lesson 4: COVERSATIONAL THREADS


- **Focus**: Tracing in conversational applications where maintaining context across multiple turns is essential.  
- **Threads**: Group runs into threads to visualize conversation flow.  
- **Benefits**:  
  - Show how context is preserved across user inputs and model responses.  
  - Help debug issues unique to multi-turn conversations.  
  - Enable tracing of the entire dialogue, not just individual messages, for better UX understanding.  

- **Example**: Metadata (like thread ID) links all runs within a conversation for easier inspection in LangSmith.  

