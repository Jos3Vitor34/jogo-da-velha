import customtkinter as ctk
import random
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Jogo da Velha com IA")
root.geometry("400x450")  # janela mais compacta

current_player = "X"
human_player = "X"
board = [" " for _ in range(9)]
buttons = []
difficulty = "Médio"

human_score = 0
ai_score = 0

difficulty_label = ctk.CTkLabel(root, text=f"Dificuldade atual: {difficulty}", font=("Arial", 12, "bold"))
player_label = ctk.CTkLabel(root, text=f"Você joga como: {human_player}", font=("Arial", 12, "bold"))
score_label = ctk.CTkLabel(root, text=f"Placar - Você: {human_score} | IA: {ai_score}", font=("Arial", 12, "bold"))

def check_winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return condition
    return None

def is_full():
    return all(space != " " for space in board)

def ai_move():
    if difficulty == "Fácil":
        return random.choice([i for i in range(9) if board[i] == " "])
    elif difficulty == "Médio":
        for i in range(9):
            if board[i] == " ":
                board[i] = human_player
                if check_winner(human_player):
                    board[i] = " "
                    return i
                board[i] = " "
        return random.choice([i for i in range(9) if board[i] == " "])
    else:
        return minimax(board, "O" if human_player == "X" else "X")[0]

def minimax(board_state, player):
    ai_player = "O" if human_player == "X" else "X"
    if check_winner(human_player):
        return (None, -1)
    if check_winner(ai_player):
        return (None, 1)
    if is_full():
        return (None, 0)

    moves = []
    for i in range(9):
        if board_state[i] == " ":
            board_state[i] = player
            score = minimax(board_state, human_player if player == ai_player else ai_player)[1]
            moves.append((i, score))
            board_state[i] = " "
    return max(moves, key=lambda x: x[1]) if player == ai_player else min(moves, key=lambda x: x[1])

def highlight_winner(condition):
    for i in condition:
        buttons[i].configure(fg_color="#2ecc71")

def button_click(i):
    global current_player, human_score
    if board[i] == " " and current_player == human_player:
        board[i] = human_player
        color = "#e74c3c" if human_player == "X" else "#3498db"
        buttons[i].configure(text=human_player, text_color=color)
        condition = check_winner(human_player)
        if condition:
            highlight_winner(condition)
            messagebox.showinfo("Fim de jogo", "🎉 Você venceu!")
            human_score += 1
            update_score()
            root.after(1000, reset_game)
            return
        elif is_full():
            messagebox.showinfo("Fim de jogo", "🤝 Empate!")
            root.after(1000, reset_game)
            return
        current_player = "O" if human_player == "X" else "X"
        ai_turn()

def ai_turn():
    global current_player, ai_score
    ai_player = "O" if human_player == "X" else "X"
    move = ai_move()
    board[move] = ai_player
    color = "#3498db" if ai_player == "O" else "#e74c3c"
    buttons[move].configure(text=ai_player, text_color=color)
    condition = check_winner(ai_player)
    if condition:
        highlight_winner(condition)
        messagebox.showinfo("Fim de jogo", "🤖 A IA venceu!")
        ai_score += 1
        update_score()
        root.after(1000, reset_game)
        return
    elif is_full():
        messagebox.showinfo("Fim de jogo", "🤝 Empate!")
        root.after(1000, reset_game)
        return
    current_player = human_player

def reset_game():
    global board, current_player
    board = [" " for _ in range(9)]
    current_player = human_player
    for btn in buttons:
        btn.configure(text=" ", text_color="black", fg_color="#3c3c3c")

def set_difficulty(level):
    global difficulty
    difficulty = level
    difficulty_label.configure(text=f"Dificuldade atual: {difficulty}")
    reset_game()

def set_player(choice):
    global human_player, current_player
    human_player = choice
    current_player = human_player
    player_label.configure(text=f"Você joga como: {human_player}")
    reset_game()

def update_score():
    score_label.configure(text=f"Placar - Você: {human_score} | IA: {ai_score}")

# Título
title_label = ctk.CTkLabel(root, text="🎮 Jogo da Velha com IA 🎮", font=("Arial", 18, "bold"))
title_label.pack(pady=5)

# Tabuleiro
frame_board = ctk.CTkFrame(root)
frame_board.pack(pady=5)

for i in range(9):
    btn = ctk.CTkButton(frame_board, text=" ", width=80, height=80, font=("Arial", 18, "bold"),
                        fg_color="#3c3c3c", text_color="black", command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3, padx=4, pady=4)
    buttons.append(btn)

# Labels
difficulty_label.pack(pady=2)
player_label.pack(pady=2)
score_label.pack(pady=2)

# Seleção de dificuldade
diff_frame = ctk.CTkFrame(root)
diff_frame.pack(pady=5)
ctk.CTkLabel(diff_frame, text="Dificuldade:", font=("Arial", 12, "bold")).pack(pady=2)

ctk.CTkButton(diff_frame, text="Fácil", fg_color="#27ae60", width=80,
              command=lambda: set_difficulty("Fácil")).pack(side="left", padx=5)
ctk.CTkButton(diff_frame, text="Médio", fg_color="#f39c12", width=80,
              command=lambda: set_difficulty("Médio")).pack(side="left", padx=5)
ctk.CTkButton(diff_frame, text="Difícil", fg_color="#c0392b", width=80,
              command=lambda: set_difficulty("Difícil")).pack(side="left", padx=5)

# Seleção de jogador (X ou O) logo abaixo do placar
player_frame = ctk.CTkFrame(root)
player_frame.pack(pady=5)
ctk.CTkLabel(player_frame, text="Seu símbolo:", font=("Arial", 12, "bold")).pack(pady=2)

ctk.CTkButton(player_frame, text="X", fg_color="#e74c3c", width=80,
              command=lambda: set_player("X")).pack(side="left", padx=5)
ctk.CTkButton(player_frame, text="O", fg_color="#3498db", width=80,
              command=lambda: set_player("O")).pack(side="left", padx=5)

# Reset
reset_btn = ctk.CTkButton(root, text="Resetar", fg_color="#e1b12c", command=reset_game)
reset_btn.pack(pady=5)

root.mainloop()
