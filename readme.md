## 🧠 LangGraph Node Structure

The system uses LangGraph to manage agent execution as a flow:

1. **Input Node**

   * Receives user input.

2. **Routing Node**

   * Uses embeddings to select relevant bots dynamically.

3. **Tool Node (Search)**

   * Provides contextual information if needed.

4. **Generation Node**

   * Each bot generates a response based on its persona.

This modular structure allows flexible multi-agent execution.

---

## 🛡️ Prompt Injection Defense (Phase 3)

To defend against prompt injection attacks:

* The system enforces **strict system-level instructions** that override user manipulation attempts.
* Instructions like *"ignore previous context"* are explicitly rejected in prompts.
* The model is constrained to:

  * Stay on topic
  * Maintain logical reasoning
  * Ignore irrelevant or malicious instructions

Additionally, conversation context is preserved using RAG, ensuring responses remain grounded and consistent.
