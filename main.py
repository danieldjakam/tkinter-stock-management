# main.py

import tkinter as tk
from auth import StockApp
from pages import MainApp

def main():
    # 1) On lance d'abord l'app de login
    root = tk.Tk()
    login_app = StockApp(root)
    root.mainloop()

    # 2) Quand root est détruit (login réussi), on ouvre la fenêtre principale
    main_app = MainApp()
    main_app.mainloop()

if __name__ == "__main__":
    main()
