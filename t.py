import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FinX - Gestion de Transactions")
        self.root.geometry("1200x800")
        
        # Configuration du style
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.create_sidebar()
        self.create_main_content()
    
    def create_sidebar(self):
        """Crée la barre latérale de navigation"""
        sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        logo_label = ctk.CTkLabel(sidebar, text="FinX", font=("Arial", 20, "bold"))
        logo_label.pack(pady=40)
        
        buttons = [
            ("Transactions", self.show_transactions),
            ("Portfolio", self.show_portfolio),
            ("Wallet", self.show_wallet),
            ("Help", self.show_help)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(sidebar, text=text, command=command,
                               fg_color="transparent", hover_color="#f0f0f0",
                               anchor="w")
            btn.pack(fill="x", padx=10, pady=5)
    
    def create_main_content(self):
        """Crée le contenu principal avec les transactions"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # En-tête
        header = ctk.CTkFrame(self.main_frame, height=80)
        header.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(header, text="Transactions", font=("Arial", 24))
        title.pack(side="left")
        
        filter_menu = ctk.CTkOptionMenu(header, 
                                       values=["All", "Income", "Expenses"],
                                       width=150)
        filter_menu.pack(side="right", padx=10)
        
        # Tableau des transactions
        self.create_transactions_table()
    
    def create_transactions_table(self):
        """Crée le tableau de transactions avec style moderne"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="black",
                       rowheight=40,
                       fieldbackground="#ffffff",
                       bordercolor="#e1e1e1",
                       borderwidth=1)
        style.map("Treeview", background=[("selected", "#f0f0f0")])
        
        columns = ("name", "date", "amount", "fee", "channel")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)
        
        # Configuration des colonnes
        self.tree.heading("name", text="Name/Business")
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("fee", text="Fee")
        self.tree.heading("channel", text="Channel")
        
        self.tree.column("name", width=250)
        self.tree.column("date", width=150)
        self.tree.column("amount", width=120, anchor="e")
        self.tree.column("fee", width=80, anchor="e")
        self.tree.column("channel", width=150)
        
        # Ajout des données
        transactions = [
            ("Car loans", "Jan 29, 2022 At 08:00 AM", "$13.10", "$1.1", "Offline"),
            ("Bitcoin buy 1,000 investment", "Jan 29, 2022 At 08:00 AM", "$24,800.15", "$0.0", "Internet"),
            ("Mortgage real estate", "Jan 29, 2022 At 08:00 AM", "$512.21", "$1.5", "House office"),
            ("Starbuck coffee", "Jan 29, 2022 At 08:00 AM", "$3.10", "$2.0", "Offline"),
            ("Facebook charge Advertising", "Jan 29, 2022 At 08:00 AM", "$515.04", "$4.2", "Internet"),
            ("Bank of Merica Fee charged", "Jan 29, 2022 At 08:00 AM", "$513.16", "$1.2", "Bank"),
            ("Water bills", "Jan 29, 2022 At 08:00 AM", "$19.65", "$0.1", "Internet by app"),
            ("Gas Wildraw", "Jan 29, 2022 At 08:00 AM", "$10.40", "$0.8", "Offline")
        ]
        
        for transaction in transactions:
            self.tree.insert("", "end", values=transaction)
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
    
    def show_transactions(self):
        """Affiche la vue des transactions"""
        pass
    
    def show_portfolio(self):
        """Affiche la vue portfolio"""
        pass
    
    def show_wallet(self):
        """Affiche la vue wallet"""
        pass
    
    def show_help(self):
        """Affiche la vue d'aide"""
        pass

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()