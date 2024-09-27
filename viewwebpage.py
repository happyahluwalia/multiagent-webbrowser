import re
import requests
from markdownify import markdownify as md
from requests.exceptions import RequestException
from transformers.agents import tool
from transformers.agents import (
    ReactCodeAgent,
    ReactJsonAgent,
    HfApiEngine,
    ManagedAgent,
)
from transformers.agents.search import DuckDuckGoSearchTool


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = md(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


model = "Qwen/Qwen2.5-72B-Instruct"

llm_engine = HfApiEngine(model)

web_agent = ReactJsonAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    llm_engine=llm_engine,
    max_iterations=10,
)
managed_web_agent = ManagedAgent(
    agent=web_agent,
    name="search",
    description="Runs web searches for you. Give it your query as an argument.",
)
manager_agent = ReactCodeAgent(
    tools=[],
    llm_engine=llm_engine,
    managed_agents=[managed_web_agent],
    additional_authorized_imports=["time", "datetime"],
)
manager_agent.run("How many years ago was Stripe founded?")