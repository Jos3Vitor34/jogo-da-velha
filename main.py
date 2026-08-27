import customtkinter as ctk
import random
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JogoDaVelhaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Jogo da Velha com IA")
        self.geometry("400x450")
        
        # Estado do jogo
        self.current_player = "X"
        self.human_player = "X"
        self.board = [" " for _ in range(9)]
        self.difficulty = "Médio"
        self.human_score = 0
        self.ai_score = 0
        self.buttons = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(self, text="🎮 Jogo da Velha com IA 🎮", font=("Arial", 18, "bold"))
        title_label.pack(pady=5)
        
        # Tabuleiro
        frame_board = ctk.CTkFrame(self)
        frame_board.pack(pady=5)
        
        for i in range(9):
            btn = ctk.CTkButton(frame_board, text=" ", width=80, height=80, font=("Arial", 18, "bold"),
                                fg_color="#3c3c3c", text_color="black", command=lambda i=i: self.button_click(i))
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.buttons.append(btn)
            
        # Labels
        self.difficulty_label = ctk.CTkLabel(self, text=f"Dificuldade atual: {self.difficulty}", font=("Arial", 12, "bold"))
        self.difficulty_label.pack(pady=2)
        
        self.player_label = ctk.CTkLabel(self, text=f"Você joga como: {self.human_player}", font=("Arial", 12, "bold"))
        self.player_label.pack(pady=2)
        
        self.score_label = ctk.CTkLabel(self, text=f"Placar - Você: {self.human_score} | IA: {self.ai_score}", font=("Arial", 12, "bold"))
        self.score_label.pack(pady=2)
        
        # Seleção de dificuldade
        diff_frame = ctk.CTkFrame(self)
        diff_frame.pack(pady=5)
        ctk.CTkLabel(diff_frame, text="Dificuldade:", font=("Arial", 12, "bold")).pack(pady=2)
        
        ctk.CTkButton(diff_frame, text="Fácil", fg_color="#27ae60", width=80,
                      command=lambda: self.set_difficulty("Fácil")).pack(side="left", padx=5)
        ctk.CTkButton(diff_frame, text="Médio", fg_color="#f39c12", width=80,
                      command=lambda: self.set_difficulty("Médio")).pack(side="left", padx=5)
        ctk.CTkButton(diff_frame, text="Difícil", fg_color="#c0392b", width=80,
                      command=lambda: self.set_difficulty("Difícil")).pack(side="left", padx=5)
                      
        # Seleção de jogador
        player_frame = ctk.CTkFrame(self)
        player_frame.pack(pady=5)
        ctk.CTkLabel(player_frame, text="Seu símbolo:", font=("Arial", 12, "bold")).pack(pady=2)
        
        ctk.CTkButton(player_frame, text="X", fg_color="#e74c3c", width=80,
                      command=lambda: self.set_player("X")).pack(side="left", padx=5)
        ctk.CTkButton(player_frame, text="O", fg_color="#3498db", width=80,
                      command=lambda: self.set_player("O")).pack(side="left", padx=5)
                      
        # Reset
        reset_btn = ctk.CTkButton(self, text="Resetar", fg_color="#e1b12c", command=self.reset_game)
        reset_btn.pack(pady=5)

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return condition
        return None
        
    def is_full(self):
        return all(space != " " for space in self.board)
        
    def ai_move(self):
        if self.difficulty == "Fácil":
            return random.choice([i for i in range(9) if self.board[i] == " "])
        elif self.difficulty == "Médio":
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = self.human_player
                    if self.check_winner(self.human_player):
                        self.board[i] = " "
                        return i
                    self.board[i] = " "
            return random.choice([i for i in range(9) if self.board[i] == " "])
        else:
            return self.minimax(self.board, "O" if self.human_player == "X" else "X")[0]
            
    def minimax(self, board_state, player):
        ai_player = "O" if self.human_player == "X" else "X"
        if self.check_winner(self.human_player):
            return (None, -1)
        if self.check_winner(ai_player):
            return (None, 1)
        if self.is_full():
            return (None, 0)
            
        moves = []
        for i in range(9):
            if board_state[i] == " ":
                board_state[i] = player
                score = self.minimax(board_state, self.human_player if player == ai_player else ai_player)[1]
                moves.append((i, score))
                board_state[i] = " "
        return max(moves, key=lambda x: x[1]) if player == ai_player else min(moves, key=lambda x: x[1])

    def highlight_winner(self, condition):
        for i in condition:
            self.buttons[i].configure(fg_color="#2ecc71")
            
    def button_click(self, i):
        if self.board[i] == " " and self.current_player == self.human_player:
            self.board[i] = self.human_player
            color = "#e74c3c" if self.human_player == "X" else "#3498db"
            self.buttons[i].configure(text=self.human_player, text_color=color)
            
            condition = self.check_winner(self.human_player)
            if condition:
                self.highlight_winner(condition)
                messagebox.showinfo("Fim de jogo", "🎉 Você venceu!")
                self.human_score += 1
                self.update_score()
                self.after(1000, self.reset_game)
                return
            elif self.is_full():
                messagebox.showinfo("Fim de jogo", "🤝 Empate!")
                self.after(1000, self.reset_game)
                return
                
            self.current_player = "O" if self.human_player == "X" else "X"
            self.ai_turn()
            
    def ai_turn(self):
        ai_player = "O" if self.human_player == "X" else "X"
        move = self.ai_move()
        self.board[move] = ai_player
        
        color = "#3498db" if ai_player == "O" else "#e74c3c"
        self.buttons[move].configure(text=ai_player, text_color=color)
        
        condition = self.check_winner(ai_player)
        if condition:
            self.highlight_winner(condition)
            messagebox.showinfo("Fim de jogo", "🤖 A IA venceu!")
            self.ai_score += 1
            self.update_score()
            self.after(1000, self.reset_game)
            return
        elif self.is_full():
            messagebox.showinfo("Fim de jogo", "🤝 Empate!")
            self.after(1000, self.reset_game)
            return
            
        self.current_player = self.human_player

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = self.human_player
        for btn in self.buttons:
            btn.configure(text=" ", text_color="black", fg_color="#3c3c3c")
            
    def set_difficulty(self, level):
        self.difficulty = level
        self.difficulty_label.configure(text=f"Dificuldade atual: {self.difficulty}")
        self.reset_game()
        
    def set_player(self, choice):
        self.human_player = choice
        self.current_player = self.human_player
        self.player_label.configure(text=f"Você joga como: {self.human_player}")
        self.reset_game()
        
    def update_score(self):
        self.score_label.configure(text=f"Placar - Você: {self.human_score} | IA: {self.ai_score}")

if __name__ == "__main__":
    app = JogoDaVelhaApp()
    app.mainloop()
