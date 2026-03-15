import pygame
import sys
import random

# --- הגדרות קבועות ---
WIDTH, HEIGHT = 450, 600
LINE_WIDTH = 7
BOARD_SIZE = 450
SQUARE_SIZE = BOARD_SIZE // 3

# גודל הצורות
CIRCLE_RADIUS = SQUARE_SIZE // 3.5
CIRCLE_WIDTH = 12
CROSS_WIDTH = 18
SPACE = SQUARE_SIZE // 3

# --- צבעים ---
BG_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
SCORE_BG = (30, 30, 30)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WIN_MSG_COLOR = (255, 215, 0)
TIE_MSG_COLOR = (0, 191, 255)

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
            pygame.draw.circle(screen, PLAYER_COLOR, (center_x, center_y), int(CIRCLE_RADIUS), CIRCLE_WIDTH)
        elif sym == "X":
            pygame.draw.line(screen, PLAYER_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            pygame.draw.line(screen, PLAYER_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             CROSS_WIDTH)


def draw_scoreboard(screen, current_player, game_mode):
    # רקע ללוח הניקוד
    pygame.draw.rect(screen, SCORE_BG, (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))
    pygame.draw.line(screen, LINE_COLOR, (0, BOARD_SIZE), (WIDTH, BOARD_SIZE), 3)

    font = pygame.font.SysFont("Arial", 20, bold=True)

    # יצירת הניקוד בחלקים
    label_wins = font.render("Wins -> ", True, YELLOW)

    x_txt = font.render("X: ", True, RED)
    x_val = font.render(f"{scores['X']}", True, YELLOW)

    o_txt = font.render("O: ", True, RED)
    o_val = font.render(f"{scores['O']}", True, YELLOW)

    t_txt = font.render("Ties: ", True, RED)
    t_val = font.render(f"{scores['Ties']}", True, YELLOW)

    # מיקומים מחושבים לרווח שווה (Spacing)
    start_y = BOARD_SIZE + 15
    screen.blit(label_wins, (20, start_y))

    # חלוקת השטח לשלושה עמודות שוות אחרי ה-"Wins ->"
    col_x = 110
    col_o = 210
    col_ties = 310

    # הדפסת X
    screen.blit(x_txt, (col_x, start_y))
    screen.blit(x_val, (col_x + 25, start_y))

    # הדפסת O
    screen.blit(o_txt, (col_o, start_y))
    screen.blit(o_val, (col_o + 25, start_y))

    # הדפסת Ties
    screen.blit(t_txt, (col_ties, start_y))
    screen.blit(t_val, (col_ties + 55, start_y))

    # תור נוכחי
    mode_str = "VS Computer" if game_mode == "AI" else "PvP"
    turn_render = font.render(f"Turn: {current_player} ({mode_str})", True, (180, 180, 180))
    screen.blit(turn_render, (20, BOARD_SIZE + 50))


def show_game_over(screen, winner):
    overlay = pygame.Surface((WIDTH, BOARD_SIZE), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("Arial", 45, bold=True)
    font_small = pygame.font.SysFont("Arial", 22, bold=True)

    if winner == "Tie":
        text = font_big.render("IT'S A TIE!", True, TIE_MSG_COLOR)
    else:
        text = font_big.render(f"PLAYER {winner} WINS!", True, WIN_MSG_COLOR)

    restart_text = font_small.render("Press 'R' to Restart", True, TEXT_COLOR)
    menu_text = font_small.render("Press 'M' for Menu", True, TEXT_COLOR)

    screen.blit(text, text.get_rect(center=(WIDTH // 2, BOARD_SIZE // 2 - 40)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, BOARD_SIZE // 2 + 30)))
    screen.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, BOARD_SIZE // 2 + 70)))


def check_winner(board, symbol):
    win_options = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    return any(all(board[i] == symbol for i in combo) for combo in win_options)


def is_tie(board):
    return all(spot is not None for spot in board)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe - Final Version')

    board = create_board()
    current_turn = "X"
    game_over = False
    winner = None
    game_mode = None

    while True:
        if game_mode is None:
            screen.fill(BG_COLOR)
            menu_font = pygame.font.SysFont("Arial", 32, bold=True)
            t1 = menu_font.render("1: VS Computer", True, PLAYER_COLOR)
            t2 = menu_font.render("2: VS Player", True, TEXT_COLOR)
            screen.blit(t1, (WIDTH // 2 - 110, HEIGHT // 2 - 60))
            screen.blit(t2, (WIDTH // 2 - 110, HEIGHT // 2 + 10))
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

        if game_over:
            show_game_over(screen, winner)

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
                            winner = current_turn
                        elif is_tie(board):
                            scores["Ties"] += 1
                            game_over = True
                            winner = "Tie"
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
                                        winner = "O"
                                    elif is_tie(board):
                                        scores["Ties"] += 1
                                        game_over = True
                                        winner = "Tie"
                                    current_turn = "X"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = create_board()
                    game_over = False
                    winner = None
                    current_turn = "X"
                if event.key == pygame.K_m:
                    game_mode = None
                    board = create_board()
                    game_over = False
                    winner = None
                    current_turn = "X"

        pygame.display.update()


if __name__ == "__main__":
    main()