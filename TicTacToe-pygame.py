import pygame
import sys
import random

# --- הגדרות קבועות ---
WIDTH, HEIGHT = 450, 600
LINE_WIDTH = 7
BOARD_SIZE = 450
SQUARE_SIZE = BOARD_SIZE // 3
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 12
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# --- צבעים ---
BG_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
SCORE_BG = (30, 30, 30)  # רקע כהה ללוח הניקוד

# משתני ניקוד
scores = {"X": 0, "O": 0, "Ties": 0}


def create_board():
    return [None] * 9


def draw_lines(screen):
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (BOARD_SIZE, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, BOARD_SIZE), LINE_WIDTH)


def draw_figures(screen, board):
    for idx, sym in enumerate(board):
        if sym is None: continue
        row, col = idx // 3, idx % 3
        center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
        center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)

        if sym == "O":
            pygame.draw.circle(screen, PLAYER_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
        elif sym == "X":
            pygame.draw.line(screen, PLAYER_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            pygame.draw.line(screen, PLAYER_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             CROSS_WIDTH)


def draw_scoreboard(screen, current_player, game_mode):
    # ציור מלבן רקע ללוח הניקוד
    pygame.draw.rect(screen, SCORE_BG, (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))
    pygame.draw.line(screen, LINE_COLOR, (0, BOARD_SIZE), (WIDTH, BOARD_SIZE), 3)

    font = pygame.font.SysFont("Arial", 22, bold=True)

    # יצירת טקסטים בצבעים שונים
    x_score = font.render(f"X Wins: {scores['X']}", True, PLAYER_COLOR)
    o_score = font.render(f"O Wins: {scores['O']}", True, PLAYER_COLOR)
    ties_score = font.render(f"Ties: {scores['Ties']}", True, (200, 200, 200))  # אפור/לבן לתיקו

    mode_str = "VS Computer" if game_mode == "AI" else "Player vs Player"
    turn_render = font.render(f"Turn: {current_player} ({mode_str})", True, (255, 255, 0))  # צהוב לתור הנוכחי

    # מיקום הטקסטים
    screen.blit(x_score, (20, BOARD_SIZE + 15))
    screen.blit(o_score, (160, BOARD_SIZE + 15))
    screen.blit(ties_score, (310, BOARD_SIZE + 15))
    screen.blit(turn_render, (20, BOARD_SIZE + 50))

    reset_font = pygame.font.SysFont("Arial", 14)
    reset_render = reset_font.render("R: Restart | M: Menu", True, (150, 150, 150))
    screen.blit(reset_render, (WIDTH - 150, HEIGHT - 25))


def check_winner(board, symbol):
    win_options = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    return any(all(board[i] == symbol for i in combo) for combo in win_options)


def is_tie(board):
    return all(spot is not None for spot in board)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe - Colorful Scoreboard')

    board = create_board()
    current_turn = "X"
    game_over = False
    game_mode = None

    while True:
        if game_mode is None:
            screen.fill(BG_COLOR)
            menu_font = pygame.font.SysFont("Arial", 30, bold=True)
            t1 = menu_font.render("Press 1: vs Computer", True, PLAYER_COLOR)
            t2 = menu_font.render("Press 2: vs Player", True, TEXT_COLOR)
            screen.blit(t1, (WIDTH // 2 - 130, HEIGHT // 2 - 50))
            screen.blit(t2, (WIDTH // 2 - 130, HEIGHT // 2 + 20))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: game_mode = "AI"
                    if event.key == pygame.K_2: game_mode = "PVP"
            continue

        draw_lines(screen)
        draw_figures(screen, board)
        draw_scoreboard(screen, current_turn, game_mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                if mouseY < BOARD_SIZE:
                    idx = (mouseY // SQUARE_SIZE) * 3 + (mouseX // SQUARE_SIZE)

                    if board[idx] is None:
                        board[idx] = current_turn

                        if check_winner(board, current_turn):
                            scores[current_turn] += 1
                            game_over = True
                        elif is_tie(board):
                            scores["Ties"] += 1
                            game_over = True
                        else:
                            current_turn = "O" if current_turn == "X" else "X"

                            if game_mode == "AI" and current_turn == "O" and not game_over:
                                draw_figures(screen, board)
                                pygame.display.update()
                                pygame.time.delay(400)
                                available = [i for i, s in enumerate(board) if s is None]
                                if available:
                                    move = random.choice(available)
                                    board[move] = "O"
                                    if check_winner(board, "O"):
                                        scores["O"] += 1
                                        game_over = True
                                    elif is_tie(board):
                                        scores["Ties"] += 1
                                        game_over = True
                                    current_turn = "X"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = create_board()
                    game_over = False
                    current_turn = "X"
                if event.key == pygame.K_m:
                    game_mode = None
                    board = create_board()
                    game_over = False
                    current_turn = "X"

        pygame.display.update()


if __name__ == "__main__":
    main()