import chess
import chess.svg
import cairosvg
from PIL import Image
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parents[3] / "cache"

class ChessEngine:
  def __init__(self) -> None:
    self.board : chess.Board = chess.Board()
    self.render_index = 0

  def renderBoard(self):
    self.render_index += 1
    board_svg = chess.svg.board(self.board)
    png_board = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
    # Save sequentially so we keep every board state
    path = CACHE_PATH / f"board_{self.render_index:04d}.png"
    with open(path, "wb") as f:
      f.write(png_board) # type: ignore

    img = Image.open(path)
    img.show()

  # now make tools (check game state (ASCII), make move, check move legal)