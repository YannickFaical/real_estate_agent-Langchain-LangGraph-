from langchain_core.messages import HumanMessage
from agent_graph import graph

def run_agent():
    print("Assistant immobilier prêt. Tape 'quit' pour sortir.\n")
    
    messages = []
    
    while True:
        user_input = input("Vous: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Fin.")
            break

        messages.append(HumanMessage(content=user_input))
        result = graph.invoke({"messages": messages})
        messages = result["messages"]

        # on affiche le dernier message IA lisible
        for msg in reversed(messages):
            if getattr(msg, "type", "") == "ai" and msg.content:
                print(f"\nAgent: {msg.content}\n")
                break


if __name__ == "__main__":
    run_agent()