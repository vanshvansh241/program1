# Tic Tac Toe Game

board = [" " for _ in range(9)]

def print_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()

def check_winner(player):
    win = [
        [0,1,2], [3,4,5], [6,7,8],  # Rows
        [0,3,6], [1,4,7], [2,5,8],  # Columns
        [0,4,8], [2,4,6]            # Diagonals
    ]

    for combination in win:
        if all(board[i] == player for i in combination):
            return True
    return False

def board_full():
    return " " not in board

player = "X"

while True:
    print_board()

    try:
        move = int(input(f"Player {player}, enter position (1-9): ")) - 1

        if move < 0 or move > 8:
            print("Invalid position! Choose 1-9.")
            continue

        if board[move] != " ":
            print("Position already taken!")
            continue

        board[move] = player

        if check_winner(player):
            print_board()
            print(f"🎉 Player {player} wins!")
            break

        if board_full():
            print_board()
            print("🤝 It's a Draw!")
            break

        player = "O" if player == "X" else "X"

    except ValueError:
        print("Please enter a valid number.")