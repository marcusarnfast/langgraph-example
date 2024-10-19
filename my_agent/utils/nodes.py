from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from my_agent.utils.investment import evaluate_investment  # Import the function
from langgraph.prebuilt import ToolNode


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    elif model_name == "anthropic":
        model =  ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


system_prompt = """You are a financial advisor assistant. Your role is to provide insightful and practical advice on financial matters, including investments, savings, and personal finance management. Always consider the user's financial situation and risk tolerance when providing recommendations. 


The answer should be concise and to the point.
"""

# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "anthropic")
    model = _get_model(model_name)
    
    # Gather user financial information
    financial_info = gather_user_financial_info()
    
    # Prepare the evaluation input
    evaluation_result = evaluate_investment(
        investment_risk=financial_info["investment_risk"],
        user_savings=financial_info["user_savings"],
        user_income=financial_info["user_income"]
    )
    
    # Instead of adding the evaluation result to messages, just return it
    response = model.invoke(messages)
    
    # Return the evaluation result along with the model's response
    return {
        "messages": [response],
        "evaluation": evaluation_result  # Include the evaluation result separately
    }

# Define the function to execute tools
tool_node = ToolNode(tools)

def gather_user_financial_info() -> dict:
    """
    Prompts the user for their financial information.

    Returns:
        dict: A dictionary containing user income, savings, and investment risk.
    """
    try:
        user_income = float(input("Please enter your annual income: "))
        user_savings = float(input("Please enter your current savings: "))
        investment_risk = float(input("On a scale of 0 to 1, how would you rate the investment risk (0 being no risk and 1 being high risk)? "))
    except EOFError:
        print("Input was not provided. Using default values.")
        user_income = 80000  # Default value
        user_savings = 50000  # Default value
        investment_risk = 0.3  # Default value

    return {
        "user_income": user_income,
        "user_savings": user_savings,
        "investment_risk": investment_risk
    }
