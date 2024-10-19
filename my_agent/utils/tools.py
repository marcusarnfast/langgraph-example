from langchain_community.tools.tavily_search import TavilySearchResults
from my_agent.utils.investment import evaluate_investment

tools = [
    TavilySearchResults(max_results=1),
    evaluate_investment  # Add the new evaluation tool
]
