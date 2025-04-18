import tkinter as tk
from tkinter import ttk, messagebox

# Données simulées pour les produits
products = [
    {"name": "Produit A", "desc": "Description A", "price": 12.0},
    {"name": "Produit B", "desc": "Description B", "price": 18.0},
]

PRIMARY_COLOR = "#5038ED"
BG_COLOR = "#F9F9FC"
CARD_BG = "#FFFFFF"
FONT = ("Helvetica", 10)

class Sidebar(tk.Frame):
    def __init__(self, master, switch_page):
        super().__init__(master, bg="white", width=200)
        self.pack_propagate(0)
        self.switch_page = switch_page

        logo_frame = tk.Frame(self, bg="white")
        logo_frame.pack(pady=20)
        tk.Label(logo_frame, text="📦", font=("Helvetica", 24), bg="white").pack()
        tk.Label(logo_frame, text="Stock Manager", font=("Helvetica", 14, "bold"), bg="white").pack()

        self.links = {}
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(expand=True)
        for name in ["Categories", "Produits", "Mouvements", "Users", "Fournisseurs"]:
            btn = tk.Button(nav_frame, text=name, font=FONT, anchor="w",
                            bg="white", fg="black", relief="flat", padx=20,
                            command=lambda n=name: self.switch_page(n))
            btn.pack(fill="x", pady=5, ipadx=5, ipady=5)
            self.links[name] = btn

        bottom_frame = tk.Frame(self, bg="white")
        bottom_frame.pack(pady=10, side="bottom")
        tk.Button(bottom_frame, text="Help", bg="white", fg="black", relief="flat").pack(pady=5)
        tk.Button(bottom_frame, text="Logout", bg="white", fg="black", relief="flat", command=self.logout).pack(pady=5)

    def highlight(self, name):
        for link in self.links.values():
            link.configure(bg="white", fg="black")
        self.links[name].configure(bg=PRIMARY_COLOR, fg="white")

    def logout(self):
        self.master.quit()

class ProductCard(tk.Frame):
    def __init__(self, master, product, on_edit, on_delete):
        super().__init__(master, bg=CARD_BG, bd=0, highlightthickness=1, highlightbackground="#ddd")
        self.product = product
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.config(padx=20, pady=15)

        top_frame = tk.Frame(self, bg=CARD_BG)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text=product["name"], font=("Helvetica", 14, "bold"), bg=CARD_BG).pack(anchor="w")
        more_btn = tk.Menubutton(top_frame, text="⋮", font=("Helvetica", 12), bg=CARD_BG, relief="flat")
        more_btn.menu = tk.Menu(more_btn, tearoff=0)
        more_btn.menu.add_command(label="Edit", command=self.edit)
        more_btn.menu.add_command(label="Delete", command=self.delete)
        more_btn["menu"] = more_btn.menu
        more_btn.pack(anchor="e")

        tk.Label(self, text=product["desc"], font=("Helvetica", 10), bg=CARD_BG, fg="gray").pack(anchor="w", pady=(5,0))
        tk.Label(self, text=f"{product['price']} FCFA", font=("Helvetica", 10, "bold"), bg=CARD_BG).pack(anchor="w", pady=5)

    def edit(self):
        self.on_edit(self.product)

    def delete(self):
        if messagebox.askyesno("Confirmation", f"Supprimer {self.product['name']} ?"):
            products.remove(self.product)
            self.on_delete()

class MainContent(tk.Frame):
    def __init__(self, master, page="Produits"):
        super().__init__(master, bg=BG_COLOR)
        self.pack_propagate(0)
        self.page = page
        if page == "Produits":
            self.render_produits()
        else:
            self.render_placeholder()

    def render_placeholder(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=f"Page {self.page} en construction", font=("Helvetica", 18), bg=BG_COLOR).pack(expand=True)

    def render_produits(self):
        self.tabs = ["Tous", "Stock Bas", "Stock Haut"]

        topbar = tk.Frame(self, bg="white")
        topbar.pack(fill="x", pady=10, padx=20)
        tk.Label(topbar, text="Produits", font=("Helvetica", 18, "bold"), bg="white").pack(side="left")
        tk.Label(topbar, text="👤 Admin", bg="white").pack(side="right")

        tabbar = tk.Frame(self, bg=BG_COLOR)
        tabbar.pack(fill="x", padx=20)
        self.active_tab = tk.StringVar(value=self.tabs[0])
        for tab in self.tabs:
            b = tk.Radiobutton(tabbar, text=tab, variable=self.active_tab, value=tab,
                               indicatoron=0, bg="white", fg="black", selectcolor=PRIMARY_COLOR,
                               font=("Helvetica", 10, "bold"), relief="groove", width=15,
                               command=self.render_products)
            b.pack(side="left", padx=5, ipadx=5, ipady=5)

        add_btn = tk.Button(tabbar, text="+ Add", bg=PRIMARY_COLOR, fg="white",
                            font=("Helvetica", 10, "bold"), padx=10, pady=5,
                            command=self.add_product)
        add_btn.pack(side="right")

        self.product_area = tk.Frame(self, bg=BG_COLOR)
        self.product_area.pack(fill="both", expand=True, padx=20, pady=20)
        self.render_products()

    def render_products(self):
        for widget in self.product_area.winfo_children():
            widget.destroy()
        for p in products:
            card = ProductCard(self.product_area, p, self.edit_product, self.render_products)
            card.pack(fill="x", pady=10)

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

        def save():
            data = {"name": name_var.get(), "desc": desc_var.get(), "price": price_var.get()}
            if product:
                product.update(data)
            else:
                products.append(data)
            form.destroy()
            self.render_products()

        tk.Button(form, text="Enregistrer", bg=PRIMARY_COLOR, fg="white", command=save).pack(pady=10)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Manager")
        self.geometry("1000x600")
        self.configure(bg="white")

        self.sidebar = Sidebar(self, self.switch_page)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = MainContent(self, page="Produits")
        self.main_area.pack(side="right", fill="both", expand=True)
        self.sidebar.highlight("Produits")

    def switch_page(self, name):
        self.sidebar.highlight(name)
        self.main_area.destroy()
        self.main_area = MainContent(self, page=name)
        self.main_area.pack(side="right", fill="both", expand=True)

if __name__ == '__main__':
    app = App()
    app.mainloop()