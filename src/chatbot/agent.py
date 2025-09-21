from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from .tools import get_product_price, get_product_features
from config.settings import settings

def create_product_agent():
    print("DEBUG: Creating LLM...")
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=settings.openai_api_key,
    )
    print("DEBUG: LLM created successfully.")

    print("DEBUG: Creating tools...")
    tools = [get_product_price, get_product_features]
    print("DEBUG: Tools created successfully.")
    try:
        print("DEBUG: Pulling ReAct prompt template...")
        prompt = hub.pull("hwchase17/react") # ReAct prompt template
        print("DEBUG: ReAct prompt template pulled successfully.")
    except Exception:
        print("DEBUG: Failed to pull ReAct prompt template. Using default prompt.")
        prompt = """
        Plese answer questions about Macbook laptops with access to the following tools:

        {tools}

        Question: {input}

        Thought: {agent_scratchpad}
        """

        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent = agent,
            tools = tools,
            verbose = True,
            handle_parsing_errors=True,
            max_iterations=3,
        )

        return agent_executor

def ask_product_question(query: str):
    pass

if __name__ == "__main__":
    print("=== Vector pricer agent demo ===")
    print("Ask a question about Macbook laptops or type 'quit' to exit")

    agent = create_product_agent()

    while True:
        query = input("\nYou: ")
        if query.lower() in ["quit", "exit", "q"]:
            break

        if query.strip():
            print("\nAgent is thinking...")
            try:
                result = agent.invoke({"input": query})
                print("\nAgent:", result["output"])
            except Exception as e:
                print("\nError:", str(e))
        else:
            print("Please enter a question. ")