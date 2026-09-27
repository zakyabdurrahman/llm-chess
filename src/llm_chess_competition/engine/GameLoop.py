from .ChessEngine import ChessEngine
from .ChessAgentFactory import ChessAgentFactory
from langgraph.graph.state import CompiledStateGraph


class GameLoop:
    def __init__(self) -> None:
        self.game = ChessEngine()
        self.white_agent = None
        self.black_agent = None

    def initAgents(self):
        factory = ChessAgentFactory()

        agents : list[CompiledStateGraph]  = []
        for color in ("white", "black"):
            while True:
                model_code = input(f"Enter model tag/code for {color}: ").strip()
                if model_code:
                    break
                print("Model tag/code cannot be empty.")
            agents.append(factory.make_agent(model_code))

        self.white_agent, self.black_agent = agents
        self.game.renderBoard()

      
