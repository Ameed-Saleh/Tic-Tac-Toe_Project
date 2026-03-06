import random
import time
BOLD = "\033[1m"
MAROON = "\033[07m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
LIME = "\033[93m"
RESET = "\033[0;0m"

def create_board(): #🧊
    board = ['1 ','2 ','3 ','4 ' ,'5 ','6 ','7 ','8 ','9 ']
    return board

def print_board(board) : #🖼️
    for i in range(0, 9, 3):
        print(f"{CYAN}     {board[i]} | {board[i + 1]} | {board[i + 2]}{RESET}")
        if i < 6:
            print(f"{CYAN}    ----+----+----{RESET}")

def display_menu():
    print(f"\n{PURPLE}game mode menu💣:{RESET}")
    print(f"{BLUE}1. Player vs Player{RESET}")
    print(f"{BLUE}2. Player vs Computer🖥️{RESET}")
    print(f"{RED}3. Exit{RESET}")

def get_main_choice():
    while True:
        choice = input(f'{PURPLE}\nChoose game mode [1-2-3]:{RESET}')
        if choice == '3':
            break
        if choice == '1' or choice == '2':
            break
        print(f'{RED}invalid choice please try again [1-2-3]{RESET}')
    return choice

def get_player_move(player_name, sympol , board) : #🎮
    while True:
        choice = input(f"{BLUE}->{player_name}[{sympol}] choose a spot (1-9): \n{RESET}")
        if choice.lower() == "reset" or choice.lower() == "r":
            return "reset"
        if not choice.isdigit():
            print(f'{RED}That is not a number. Try again.{RESET}')
            continue
        move = int(choice) -1
        if move < 0 or move > 9:
            print(f'{RED}Please choose a number between 1 and 9.{RESET}')
            continue
        if board[move] == "❌" or board[move] == "⭕":
            print(f'{RED}That spot is already taken, choose another one!{RESET}')
            continue
        return move

def get_computer_move(board): #🖥️
    available_moves = []
    for comp in range(9):
        if board[comp] != "❌" and board[comp] != "⭕":
            available_moves.append(comp)
    return random.choice(available_moves)

def make_move(board, position, symbol) : #🧲
    board[position] = symbol

def check_winner(board, symbol): #🏆
    win_options = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # WIN BY ROW
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # WIN BY COLUMN
        [0, 4, 8], [2, 4, 6]             # WIN BY DIAGONAL
    ]
    for combo in win_options:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == symbol:
            return True
    return False

def is_tie(board): #🤝
    return all(spot == "❌" or spot == "⭕" for spot in board)


def play_game(): #🚀
    print(f"\n{MAROON}{BOLD} *** Welcome to Tic Tac Toe game‼️🚀 ***{RESET}")
    _round = 1 # THIS PARAMETER COUNT THE NUMBER OF GAMES
    # THIS THREE PARAMETERS FOR -> SCOREBOARD
    o_wins = 0
    x_wins = 0
    ties = 0
    while True:
        print(f'\n{RED}***********   GAME NUMBER {_round}   ***********{RESET}')
        print(f"{LIME}Current Score:  ❌: {x_wins} |   ⭕: {o_wins} |  🤝: {ties}\n{RESET}")
        board = create_board()
        print_board(board)
        display_menu()
        main_choice = get_main_choice()
        if main_choice == '3': # IF CHOICE EXIT == NO PLAYING
            print(f'{RED}GOOD BYE BABY! {RESET}')
            break
        # ENTER NAME FOR PLAYER
        name1 = input(f"{BLUE}Enter Player 1 name:\n {RESET}").capitalize ()
        if main_choice == '2': # PLAYER VS COMPUTER🖥️
            name2 = "Computer🖥️"
        else:                # PLAYER VS PLAYER
            name2 = input(f"{BLUE}Enter Player 2 name:\n{RESET}").capitalize()
        current_player_num = 1
        # USUALLY, THE PLAYER WITH ❌ GOES FIRST
        print(f'\n{YELLOW}*** ❌ makes the first move!!!{RESET}')
        while True: # CHOOSING A VALID SYMBOL
            symbol1 = input(f"{YELLOW}{name1} -> type [1-❌] or type [2-⭕] ? {RESET}")
            if symbol1 != "1" and symbol1 != "2":
                print(f'{RED}invalid choice, please type (1 or 2){RESET}\n')
                continue
            if symbol1 == "1":
                symbol1 , symbol2 = ("❌" ,"⭕")
                break
            else:
                symbol1 , symbol2 = ("⭕" ,"❌")
                current_player_num = 2
                break
        time.sleep(1)
        print(f'\n{RED}if you wish to restart the game, enter [r] or [reset]{RESET}')
        print(f"{BLUE}{name1}'s symbol is{symbol1}  |  {name2}'s symbol is{symbol2}{RESET}\n")
        time.sleep(2)
        board = create_board()
        game_on = True
        while game_on:
            # START GAME WITH THE GIVEN NAMES AND SYMBOLS
            print_board(board)
            if current_player_num == 1:
                current_name = name1
                current_symbol = symbol1
            else:
                current_name = name2
                current_symbol = symbol2
            if main_choice == '2' and current_name == "Computer🖥️":
                print(f"{YELLOW}Computer🖥️ is thinking...⌛️{RESET}")
                time.sleep(2)
                position = get_computer_move(board)
                print(f"{YELLOW}Computer🖥️ chose a spot ->  {position + 1}\n{RESET}")
            else:
                position = get_player_move(current_name, current_symbol, board)
            # CHECK IF RESET IS CHOSEN
            if position == "reset" :
                print(f"{RED}Game Resetting...{RESET}")
                time.sleep(2)
                _round -= 1
                break
            make_move(board, position, current_symbol)
            # CHECK WHO IS THE WINNER!
            if check_winner(board, current_symbol):
                print_board(board)
                print(f"{CYAN}\nCongratulations! {current_name} {current_symbol} wins!🏆💥{RESET}")
                if current_symbol == "❌":
                    x_wins += 1
                else:
                    o_wins += 1
                time.sleep(1)
                game_on = False
            # IF NO WINNER -> IS A TIE!
            elif is_tie(board):
                print_board(board)
                print(f"{CYAN}It's a tie!🤝{RESET}")
                ties += 1
                time.sleep(1)
                game_on = False
            else: # SWITCHING PLAYERS
                if current_player_num == 1:
                    current_player_num = 2
                else:
                    current_player_num = 1
        # PRINTING TEMPORARY SCOREBOARD !
        print(f"{LIME}\n--- SCOREBOARD ---")
        print(f"❌ Wins:   {x_wins}")
        print(f"⭕ Wins:   {o_wins}")
        print(f"🤝 Ties:   {ties}")
        print(f"------------------\n{RESET}")
        # ASKING FOR PLAY AGAIN!
        _round += 1
        while True:
            again = input(f"{PURPLE}Do you want to play again️❓ (yes/no): {RESET}")
            if again.lower() != "yes" and again.lower() != "no":
                print(f"{RED}invalid choice, please enter (yes or no){RESET}")
                continue
            else:
                break
        if  again.lower() == "no":
            print(f"{MAROON}Thanks for playing‼️️{RESET}")
            break
        if again.lower() == "yes":
            continue
play_game()