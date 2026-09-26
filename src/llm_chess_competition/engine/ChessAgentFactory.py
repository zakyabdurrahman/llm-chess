from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

SYSTEM_PROMPT = "You are a helpful assistant"

class ChessAgentFactory:
  def __init__(self) -> None:
    pass

  
  def make_agent(self, model_code) -> CompiledStateGraph:
    agent = create_agent(
      model="openrouter:" + model_code,
      tools=[],
      system_prompt=SYSTEM_PROMPT
      
    )

    return agent