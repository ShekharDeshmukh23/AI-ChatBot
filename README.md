
# Secret Revelation AI App (Starter Kit)

An end-to-end starter project for a chatbot/AI assistant that **reveals a secret key only through specific interactions**.

## Highlights
- **Progressive disclosure**: user must pass 3 gates to earn 3 fragments; only then the app reveals the secret.
- **Pattern recognition**: a light-weight ML classifier scores whether a conversation *looks* eligible.
- **State machine** powered by a tiny in-house graph (works without LangGraph) with optional LangGraph integration.
- **Personality & memory**: configurable persona, short-term memory per session, and simple file-backed long-term memory.
- **Secure by default**: secret is NEVER emitted unless all conditions pass; secret is stored in `.env`.

> Suggested extensions (see `README` bottom): swap in LangChain/LangGraph, vector memory, RAG, OpenAI/Anthropic APIs.

---

## Quickstart (Local, no external LLM)
1. **Python** 3.10+ recommended.
2. Create a virtual env and install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create `.env` from example and set your secret:
   ```bash
   cp .env.example .env
   # edit SECRET_KEY and (optionally) OPENAI_API_KEY, ANTHROPIC_API_KEY
   ```
4. Run the API:
   ```bash
   uvicorn src.app:app --reload
   ```
5. Talk to the bot:
   - Open http://127.0.0.1:8000/docs and use `/chat` (POST).
   - Or use the CLI: `python -m src.cli`

---

## The Ritual (how the secret is revealed)
The bot will **only** reveal the secret if ALL gates pass in the same session:

1. **Gate A – Code of Conduct**  
   The user must explicitly say: `I accept the Code of Conduct.`

2. **Gate B – Organizer Token Format**  
   The user must provide an organizer code with pattern: `GDG-{CITY}-{YEAR}`  
   Example: `GDG-HYDERABAD-2025`. (City letters only, YEAR is 4 digits 2020–2030.)

3. **Gate C – Knowledge Check (2FA)**  
   The user must correctly answer: *"What is 2FA?"* with a definition containing words like **two**, **factor**, **authentication**.

4. **Pattern Score (ML)**  
   A tiny classifier (trained on toy data) must score the chat as **ELIGIBLE**. It uses simple text features like politeness, number of turns, and compliance cues.

If any gate fails, the bot refuses to reveal the secret and keeps guiding the user forward with **progressive hints**.

---

## Endpoints
- `POST /chat` – send a message `{ "session_id": "abc", "message": "..." }`
- `POST /reset` – clear a session
- `GET /state/{session_id}` – inspect session state for debugging

---

## Project Structure
```
secret-revelation-app/
├─ src/
│  ├─ app.py                # FastAPI app + routes
│  ├─ cli.py                # Simple CLI client
│  ├─ core/
│  │  ├─ config.py          # env + settings
│  │  ├─ memory.py          # session + file memory
│  │  ├─ persona.py         # persona + system message
│  │  ├─ policy.py          # gates + progressive disclosure
│  │  ├─ classifier.py      # toy ML classifier
│  │  ├─ statemachine.py    # minimal state graph (LangGraph optional)
│  │  └─ utils.py           # helpers
│  └─ vendors/
│     ├─ llm_openai.py      # optional OpenAI wrapper
│     └─ llm_anthropic.py   # optional Anthropic wrapper
├─ tests/
│  └─ test_policy.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Swap in Popular Stacks
- **LangGraph**: Swap `core/statemachine.py` with an actual `langgraph` graph.  
- **LangChain**: Use `vendors/llm_*` from LangChain wrappers instead.
- **Vector DB**: Replace file memory with FAISS/Chroma for contextual memory.
- **RAG**: Add a `knowledge/` folder, embed docs, provide retrieval in the policy stage.

---

## Safety Notes
- Never log the secret or full user messages in production.
- Keep the secret in `.env` and consider envelope encryption/KMS.
- Make sure any external LLM has a **strong system message** and server-side guardrails (policy gate checks happen **before** LLM responses are sent to the user).

Happy building! 🚀
