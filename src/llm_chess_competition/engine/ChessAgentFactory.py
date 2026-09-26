from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

class ChessAgentFactory:
  def __init__(self) -> None:
    pass

  
  def make_agent(self, model_code) -> CompiledStateGraph:
    agent = create_agent(
      model="openrouter:" + model_code,
      tools=[],
      system_prompt="You are a helpful assistant"
      
    )

    return agent