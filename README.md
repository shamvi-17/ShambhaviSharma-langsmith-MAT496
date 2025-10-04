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


## MODULE 2

## Lesson 1: Datasets 

- **Purpose**: Used for systematic testing and benchmarking of LLM applications.  
- **Definition**: Collections of input-output pairs for evaluating model performance.  
- **Benefits**:  
  - Simplify experiment management and progress tracking.  
  - Allow consistent and repeatable evaluation of LLM behavior.  
- **Creation Methods**:  
  - Import from CSV files.  
  - Create programmatically or generate examples (requires an OpenAI API key).  
- **Example**: A custom dataset was created with a custom example to demonstrate usage. 

## Lesson 2: Evaluators 

- **Purpose**: Automatically assess the quality and accuracy of LLM outputs.  
- **Types**:  
  - Exact Match  
  - Semantic Similarity  
  - Custom Evaluators  
- **Usage**:  
  - Automate output evaluation for efficiency and consistency.  
  - Combine multiple evaluators for a more comprehensive performance analysis.  
  - Create custom evaluators to meet specific project needs.  
- **Example**: A custom evaluator was created using the new LangSmith UI.  

## Lesson 3: Experiments  

This section demonstrates how to **run, evaluate, and optimize a RAG application** using LangSmith. It covers setting up experiments, defining evaluators, and testing different models and datasets.  

### Setup  
- Set API keys and enable tracing using environment variables or a `.env` file.  
- Define the **RAG application** with functions for:  
  - `retrieve_documents` → fetch relevant documents from a vector store  
  - `generate_response` → generate answers using retrieved context  
  - `call_openai` → interface with the language model  
  - `langsmith_rag` → orchestrates retrieval and response generation  
- Apply the `@traceable` decorator to track runs and chains.  

### Running Experiments  
- Define **evaluators** to automatically assess model output (e.g., check if responses are concise).  
- Use a **target function** to map dataset examples to the RAG application input.  
- Run experiments with `evaluate()` on:  
  - Entire datasets  
  - Specific dataset versions (`as_of`)  
  - Dataset splits (`splits`)  
  - Individual examples (`example_ids`)  
- Configure additional parameters:  
  - **Repetitions** → run multiple times for consistency  
  - **Concurrency** → parallel execution for speed  
  - **Metadata** → attach info like model name for easy tracking in the UI  

### Model Experiments  
- Swap models easily (e.g., `gpt-4o` → `gpt-3.5-turbo`) and compare performance.  
- Run experiments on different data subsets to analyze performance variations.  

### Evaluator Example  

```python
def is_concise_enough(reference_outputs: dict, outputs: dict) -> dict:
    score = len(outputs["output"]) < 1.5 * len(reference_outputs["output"])
    return {"key": "is_concise", "score": int(score)}




