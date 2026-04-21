from routing.router import route_post_to_bots
from agents.bot_graph import create_graph

from bots.tech_bot import persona as tech_persona
from bots.skeptic_bot import persona as skeptic_persona
from bots.finance_bot import persona as finance_persona

from memory.rag_engine import generate_defense_reply
from memory.store_memory import store_message

# Create graph
graph = create_graph()

# Persona mapping
persona_map = {
    "tech_bot": tech_persona,
    "skeptic_bot": skeptic_persona,
    "finance_bot": finance_persona
}

print("\n🤖 Multi-Agent AI Debate System Started")
print("Type 'exit' to quit, 'clear' to reset conversation\n")

# Conversation state
conversation_active = False
selected_bots = []
comment_history = []
parent_post = ""


while True:
    user_input = input("\n👤 You: ")

    # Exit
    if user_input.lower() == "exit":
        print("👋 Exiting...")
        break

    # Clear conversation
    if user_input.lower() == "clear":
        print("🔄 Conversation reset.\n")

        conversation_active = False
        selected_bots = []
        comment_history = []
        parent_post = ""

        continue

    # First message → routing + initial responses
    if not conversation_active:
        parent_post = user_input

        # Step 1: Route to bots
        selected_bots = route_post_to_bots(parent_post)
        print("\n🤖 Selected Bots:", selected_bots)

        # Step 2: Generate responses
        for bot in selected_bots:
            result = graph.invoke({
                "persona": persona_map[bot],
                "bot_id": bot,
                "user_input": user_input   # IMPORTANT
            })

            print(f"\n🤖 {bot}:")
            print(result["output"])

            # Save in history
            comment_history.append(f"{bot}: {result['output']}")

            #  Store in vector memory
            store_message(f"{bot}: {result['output']}")

        conversation_active = True

    #  Follow-up conversation (RAG-based debate)
    else:
        for bot in selected_bots:
            persona = persona_map[bot]

            response = generate_defense_reply(
                persona,
                parent_post,
                comment_history,
                user_input
            )

            print(f"\n🤖 {bot}:")
            print(response)

            # Update history
            comment_history.append(f"{bot}: {response}")

      