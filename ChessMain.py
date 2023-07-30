"""
Main driver file. User input handling + GameState
"""

import pygame
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {

}


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("light blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def move_piece(clicks, board):
    start = clicks[0]
    newPos = clicks[1]

    if board[start[0]][start[1]] != "--":
        end = board[start[0]][start[1]]
        board[start[0]][start[1]] = "--"
        board[newPos[0]][newPos[1]] = end


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.get_valid_moves()
    moveMade = False
    load_images()
    running = True
    squareSelected = (-1, -1)
    playerClicks = []

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # (x, y) position of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if squareSelected != (row, col):
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                else:
                    squareSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in validMoves:
                        gs.make_move(move)
                        moveMade = True
                        squareSelected = ()
                        playerClicks = []
                    else:
                        if gs.board[squareSelected[0]][squareSelected[1]] != "--":
                            playerClicks = [squareSelected]
                        else:
                            squareSelected = ()
                            playerClicks = []
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undo_move()
                    moveMade = True
        if moveMade:
            validMoves = gs.get_valid_moves()
            moveMade = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
