import chess
import chess.engine
import pygame
import chessboard.pieces
import chessboard.board

def score_move(board, move):
    line = board.copy()
    line.push_uci(move.uci())
    result = fish.analyse(line, chess.engine.Limit(depth=30))
    return result["score"]

def get_worst_best_moves(board):
    moves = list(board.legal_moves)
    scores = [score_move(board, move) for move in moves]
    scored_moves = list(zip(moves, scores))

    for scored_move in scored_moves.copy():
        if not scored_move[1].relative.mate():
            # print("removing: " + str(scored_move[1]))
            scored_moves.remove(scored_move)

    return scored_moves

pygame.init()
fish = chess.engine.SimpleEngine.popen_uci("fish/fish.exe")
board = chess.Board(fen="8/1pp5/p3pkp1/8/1P3PK1/8/r5P1/8 b - - 0 31")
display_surf = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("WORST BEST")
display_board = chessboard.board.Board({
    "Ash" : (50, 50, 50),
    "Black" : (0, 0, 0),
    "White" : (255, 255, 255)
}, (0, 10, 30), display_surf)
display_font = pygame.font.SysFont(None, 24)
display_board.updatePieces(board.fen())
display_board.displayBoard()
display_surf.blit(display_font.render("FINDING FIRST WORST BEST MOVE...", True, (200, 220, 240)), (10, 10))
pygame.display.flip()

def update_board():
    display_surf.fill((0, 10, 30))
    display_board.displayBoard()
    display_board.updatePieces(board.fen())
    display_surf.blit(display_font.render("Updating board...", True, (200, 220, 240)), (10, 10))
    display_surf.blit(display_font.render(str(fish.analyse(board, limit=chess.engine.Limit(depth=20))["score"]), True, (200, 220, 240)), (10, 30))
    pygame.display.flip()

while True:
    print("Playing worst best move...")
    board.push_uci(get_worst_best_moves(board)[0][0].uci())
    update_board()

    print("Playing best move...")
    board.push_uci(fish.play(board, chess.engine.Limit(depth=20)).move.uci())
    update_board()

fish.quit()