import chess
import chess.svg
import cairosvg
from PIL import Image
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parents[2] / "cache"

class ChessEngine:
  def __init__(self) -> None:
    self.board : chess.Board = chess.Board()

  def renderBoard(self):
    board_svg = chess.svg.board(self.board)
    png_board = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
    # Save temporarily to render as text pixels
    with open(CACHE_PATH / "temp.png", "wb") as f:
      f.write(png_board) # type: ignore

    

    img = Image.open(CACHE_PATH / "temp.png")
    img.show()

  # now make tools (check game state (ASCII), make move, check move legal)