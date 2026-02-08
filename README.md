# Agentic QA
Tool Routing Strategies

## Overview
| Patth | Focus | Typical Use Case |
|---|---|---|

## Path A 
** Very common for internal projects, MVPs, and side projects.**
### How it works
- Use a **small embedding model**:
    - `sentence-transformers`
    - `bge-small-en-v1.5`
    - `gte-small`
- Embed:
    - Tool descriptions
    - 5-15 examples questions per tool
- At runtime:
    - 1. Embed the user query
    - 2. Compute cosine similarity
    - 3. Select top-1 or top-k tools
    - 4. Apply a similarity threshold

## Path B
**The most popular pattern for serious indie projects and small teams today.**
### How it works
- Use a capable LLM with **tool / funtion calling**
- Models commonly used:
    - `llama-3.1-70b` (Groq)
    - `gemma-2-27b
- Prompt includes:
    - Tool descriptions
    - 0-4 examples
- Model is instructed to output:
    - Exactly **one tool call**
    - Or `no_tool_needed`

## Path C
### How it works
- Introduce a **dedicated router / dispateched LLM**
- The router decides whether to:
    - Use no tool, call one tool, call multiple tools in parallel, ask a clarification question, escalte to a larger model or human

### Architecture
1. **Router model** (often small or distilled)
2. **Executor model** for tool calls
3. **Final response model**

user question  --> router LLM call (small / fast model or quantized 7-13B) --> produce structured decision among
~5-9 coarse categories --> match / switch on the chosen strategy
- direct answer (no tools)
- single tool call -> execute -> final answer synthesis
- parallel tool calls (2-4 tools at once) -> gather -> synthesize
- needs clarification -> return questions to user
- multi-step / loop (ReAct style, max 4-6 cycles)
- escalate / refuse / fallback message

LangChain
- Multi-tool agents, parallel calls
- Multi-provider support needed later
- Memory / conversation history


