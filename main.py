import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import os

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Management App")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.root.configure(bg="white")

        # Charger les images
        self.login_img = self.load_image("assets/login.png")
        self.register_img = self.load_image("assets/register.png")

        self.show_login_page()

        # Redimensionnement dynamique
        self.root.bind("<Configure>", self.on_resize)

    def load_image(self, path):
        if os.path.exists(path):
            return Image.open(path)
        return None

    def on_resize(self, event):
        try:
            if hasattr(self, "bg_label") and self.current_image:
                new_width = self.left_frame.winfo_width()
                new_height = self.left_frame.winfo_height()
                resized = self.current_image.resize((new_width, new_height))
                self.tk_image = ImageTk.PhotoImage(resized)
                self.bg_label.configure(image=self.tk_image)
                self.bg_label.image = self.tk_image
        except:
            pass

    def show_login_page(self):
        self.clear_widgets()
        self.build_login_form()

    def show_register_page(self):
        self.clear_widgets()
        self.build_register_form()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_login_form(self):
        self.current_image = self.login_img

        # Frame image droite
        self.right_frame = tk.Frame(self.root, width=self.root.winfo_width() // 2, bg="black")
        self.right_frame.pack(side="right", fill="both", expand=True)

        if self.current_image:
            self.tk_image = ImageTk.PhotoImage(self.current_image.resize((self.root.winfo_width() // 2, self.root.winfo_height())))
            self.bg_label = tk.Label(self.right_frame, image=self.tk_image)
            self.bg_label.place(relwidth=1, relheight=1)

        # Frame formulaire gauche
        self.left_frame = tk.Frame(self.root, width=self.root.winfo_width() // 2, bg="white")
        self.left_frame.pack(side="left", fill="both", expand=True)

        form_container = ctk.CTkFrame(self.left_frame, fg_color="white", corner_radius=0)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(form_container, text="SE CONNECTER", font=("Arial", 24, "bold"), text_color="#1C1C1C")
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(form_container, text="Bienvenue ! Veuillez vous connecter à votre compte..",
                                font=("Arial", 10), text_color="#525252")
        subtitle.pack()

        username_entry = ctk.CTkEntry(form_container, placeholder_text="Nom d'utilisateur",
                                      fg_color="#F0EDFF", text_color="#1C1C1C",
                                      border_width=0, corner_radius=10, width=240, height=40)
        username_entry.pack(pady=10)

        password_entry = ctk.CTkEntry(form_container, placeholder_text="Mot de passe",
                                      fg_color="#F0EDFF", text_color="#1C1C1C",
                                      border_width=0, corner_radius=10, width=240, height=40,
                                      show="*")
        password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(form_container, text="Se connecter",
                                  fg_color="#5038ED", hover_color="#3d2fc2",
                                  text_color="white", corner_radius=10,
                                  font=("Arial", 12, "bold"), width=240, height=40)
        login_btn.pack(pady=20)

        register_link = ctk.CTkLabel(form_container,
                                     text="Vous n'avez pas de compte ? Inscrivez-vous.",
                                     text_color="#5038ED", font=("Arial", 10, "bold"),
                                     cursor="hand2")
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.show_register_page())

    def build_register_form(self):
        self.current_image = self.register_img

        # Frame image gauche
        self.left_frame = tk.Frame(self.root, width=self.root.winfo_width() // 2, bg="black")
        self.left_frame.pack(side="left", fill="both", expand=True)

        if self.current_image:
            self.tk_image = ImageTk.PhotoImage(self.current_image.resize((self.root.winfo_width() // 2, self.root.winfo_height())))
            self.bg_label = tk.Label(self.left_frame, image=self.tk_image)
            self.bg_label.place(relwidth=1, relheight=1)

        # Frame formulaire droite
        self.right_frame = tk.Frame(self.root, width=self.root.winfo_width() // 2, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True)

        form_container = ctk.CTkFrame(self.right_frame, fg_color="white", corner_radius=0)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(form_container, text="INSCRIPTION", font=("Arial", 24, "bold"), text_color="#1C1C1C")
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(form_container, text="Créez votre compte pour commencer.",
                                font=("Arial", 10), text_color="#525252")
        subtitle.pack()

        name_entry = ctk.CTkEntry(form_container, placeholder_text="Nom complet",
                                  fg_color="#F0EDFF", text_color="#1C1C1C",
                                  border_width=0, corner_radius=10, width=240, height=40)
        name_entry.pack(pady=10)

        name_entry = ctk.CTkEntry(form_container, placeholder_text="Nom d'utilisateur",
                                  fg_color="#F0EDFF", text_color="#1C1C1C",
                                  border_width=0, corner_radius=10, width=240, height=40)
        name_entry.pack(pady=10)

        email_entry = ctk.CTkEntry(form_container, placeholder_text="E-mail",
                                   fg_color="#F0EDFF", text_color="#1C1C1C",
                                   border_width=0, corner_radius=10, width=240, height=40)
        email_entry.pack(pady=10)

        password_entry = ctk.CTkEntry(form_container, placeholder_text="Mot de passe",
                                      fg_color="#F0EDFF", text_color="#1C1C1C",
                                      border_width=0, corner_radius=10, width=240, height=40,
                                      show="*")
        password_entry.pack(pady=10)

        register_btn = ctk.CTkButton(form_container, text="Creer son compte",
                                     fg_color="#5038ED", hover_color="#3d2fc2",
                                     text_color="white", corner_radius=10,
                                     font=("Arial", 12, "bold"), width=240, height=40)
        register_btn.pack(pady=20)

        login_link = ctk.CTkLabel(form_container,
                                  text="Vous avez déjà un compte ? Se connecter",
                                  text_color="#5038ED", font=("Arial", 10, "bold"),
                                  cursor="hand2")
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.show_login_page())

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
