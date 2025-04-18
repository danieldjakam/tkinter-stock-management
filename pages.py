import tkinter as tk
from tkinter import ttk, messagebox

PRIMARY_COLOR = "#5038ED"
BG_COLOR = "#F8F9FC"
TEXT_COLOR = "#1F1F1F"
SIDEBAR_BG = "#FFFFFF"

class Sidebar(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master, bg=SIDEBAR_BG, width=200)
        self.callback = callback
        self.pack_propagate(False)

        logo = tk.Label(self, text="📦 StockApp", bg=SIDEBAR_BG, fg=PRIMARY_COLOR,
                        font=("Segoe UI", 16, "bold"), anchor="w", padx=20)
        logo.pack(pady=(20, 40), anchor="w")

        self.buttons = {}
        for text in ["Categories", "Produits", "Mouvements", "Users", "Fournisseurs"]:
            btn = tk.Button(self, text=text, bg=SIDEBAR_BG, fg=TEXT_COLOR, anchor="w",
                            font=("Segoe UI", 11), bd=0, padx=20,
                            command=lambda t=text: self.callback(t))
            btn.pack(fill="x", pady=2)
            self.buttons[text] = btn

        tk.Label(self, bg=SIDEBAR_BG).pack(expand=True, fill="both")

        help_btn = tk.Button(self, text="❓ Help", bg=SIDEBAR_BG, fg=TEXT_COLOR, font=("Segoe UI", 11), bd=0)
        help_btn.pack(fill="x", padx=20, pady=(0, 5), anchor="s")

        logout_btn = tk.Button(self, text="🚪 Logout", justify="left", bg=SIDEBAR_BG, fg=TEXT_COLOR, font=("Segoe UI", 11), bd=0,
                               command=self.logout)
        logout_btn.pack(fill="x", padx=20, pady=(0, 20), anchor="s")

    def logout(self):
        self.master.destroy()


class Topbar(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR, height=50)
        self.pack_propagate(False)

        self.title = tk.Label(self, text="Produits", bg=BG_COLOR, fg=TEXT_COLOR,
                              font=("Segoe UI", 16, "bold"))
        self.title.pack(side="left", padx=20)

        self.profile = tk.Label(self, text="👤 John Doe", bg=BG_COLOR, fg=TEXT_COLOR,
                                font=("Segoe UI", 11))
        self.profile.pack(side="right", padx=20)


class Tabs(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        self.tabs = []
        for name in ["History", "Scheduled", "Requested"]:
            tab = tk.Label(self, text=name, bg=BG_COLOR, fg=PRIMARY_COLOR if name == "History" else TEXT_COLOR,
                           font=("Segoe UI", 11, "bold" if name == "History" else "normal"), padx=10)
            tab.pack(side="left", padx=5)
            self.tabs.append(tab)

        self.add_btn = tk.Button(self, text="+ Add", bg=PRIMARY_COLOR, fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=3)
        self.add_btn.pack(side="right", padx=10)


class ProductRow(tk.Frame):
    def __init__(self, master, name, date, amount):
        super().__init__(master, bg="white")
        self.pack_propagate(False)
        # self.config(padx=20, pady=15)
        tk.Label(self, text=name, bg="white", fg=TEXT_COLOR, font=("Segoe UI", 10)).pack(side="left", padx=20)
        tk.Label(self, text=date, bg="white", fg="gray", font=("Segoe UI", 9)).pack(side="left", padx=10)
        tk.Label(self, text=amount, bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

        menu = tk.Menubutton(self, text="⋮", bg="white", fg=TEXT_COLOR, relief="flat")
        menu.menu = tk.Menu(menu, tearoff=0)
        menu["menu"] = menu.menu
        menu.menu.add_command(label="Edit")
        menu.menu.add_command(label="Delete")
        menu.pack(side="right", padx=20)


class ProductPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        self.pack(fill="both", expand=True)

        self.topbar = Topbar(self)
        self.topbar.pack(fill="x")

        self.tabs = Tabs(self)
        self.tabs.pack(fill="x", padx=10, pady=10)

        self.list_frame = tk.Frame(self, bg='white')
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(100):
            row = ProductRow(self.list_frame, f"Produit {i+1}", "Avr 18, 2025", f"{(i+1)*10} FCFA")
            row.pack(fill="x", pady=10, ipady=15)

        # Ajouter un Scrollbar pour éviter le débordement
        self.canvas = tk.Canvas(self.list_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Mettre à jour la taille de la fenêtre interne pour éviter le défilement
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_product(self):
        self.show_product_form()

    def edit_product(self, product):
        self.show_product_form(product)

    def show_product_form(self, product=None):
        form = tk.Toplevel(self)
        form.title("Produit")
        form.geometry("300x300")

        name_var = tk.StringVar(value=product["name"] if product else "")
        desc_var = tk.StringVar(value=product["desc"] if product else "")
        price_var = tk.DoubleVar(value=product["price"] if product else 0.0)

        tk.Label(form, text="Nom:").pack()
        tk.Entry(form, textvariable=name_var).pack()
        tk.Label(form, text="Description:").pack()
        tk.Entry(form, textvariable=desc_var).pack()
        tk.Label(form, text="Prix:").pack()
        tk.Entry(form, textvariable=price_var).pack()

class CategoryPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        self.pack(fill="both", expand=True)

        self.topbar = Topbar(self)
        self.topbar.pack(fill="x")

        self.tabs = Tabs(self)
        self.tabs.pack(fill="x", padx=10, pady=10)

        self.list_frame = tk.Frame(self, bg='white')
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Ajouter un Scrollbar pour éviter le débordement
        self.canvas = tk.Canvas(self.list_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Mettre à jour la taille de la fenêtre interne pour éviter le défilement
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Stock Management")
        self.configure(bg=BG_COLOR)

        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "Produits": ProductPage(self.container),
            "Categories": CategoryPage(self.container),
        }

        for page in self.pages.values():
            page.pack(fill="both", expand=True)
        self.show_page("Produits")

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
