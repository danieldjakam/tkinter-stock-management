import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
import os
import mysql.connector
import re
import bcrypt
from mysql.connector import Error


email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
mdp_regex = r'^.{8,}$'


class StockApp():
    def __init__(self, root):
        super().__init__()

        # self.title("Login")
        # self.geometry("1000x600")
        # self.minsize(800, 500)
        # self.configure(bg="white")

        self.root = root
        self.root.title("Stock Management App")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.root.configure(bg="white")

        # Charger les images
        self.login_img = self.load_image("assets/login.png")
        self.register_img = self.load_image("assets/register.png")

        # Container principal pour le slide
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(fill="both", expand=True)

        # Création des deux frames (login/register)
        self.login_frame = tk.Frame(self.main_container, bg="white")
        self.register_frame = tk.Frame(self.main_container, bg="white")

        # Afficher la page de login initiale
        self.build_login_form()
        self.build_register_form()
        self.show_login_page(False)

        # Connexion DB
        self.db = self.connect_db()
        self.current_user = None  # Stocke l'utilisateur connecté

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",  # Remplace par ton user MySQL
                password="",  # Remplace par ton mot de passe
                database="gestion_stock"
            )
        except Error as e:
            messagebox.showerror("Erreur DB", f"Impossible de se connecter à MySQL: {e}")
            return None
        
    def login_user(self, username, password):
        if not self.db:
            messagebox.showerror("Erreur", "Base de données non connectée")
            return

        cursor = self.db.cursor()
        try:

            if not username or not password :
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return
            
            cursor.execute("SELECT * FROM Users WHERE username_Users=%s OR email_Users=%s", 
                          (username, username))
            user = cursor.fetchone()
            

            if user:
                mdp = user[3]
                mdp = mdp.encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), mdp):
                    # self.current_user = user[0]  # Stocke l'ID de l'utilisateur
                    # messagebox.showinfo("Succès", "Connexion réussie!")
                    # self.show_main_interface()
                    
                    self.current_user = user[0]
                    messagebox.showinfo("Succès", "Connexion réussie!")
                    # on ferme la fenêtre de login pour passer à MainApp
                    self.root.destroy()
                else:
                    messagebox.showerror("Erreur", "Mot de passe incorrect")
            else:
                messagebox.showerror("Erreur", "Utilisateur inexistant")
        except Error as e:
            messagebox.showerror("Erreur DB", f"Erreur lors de la connexion: {e}")
        finally:
            cursor.close()

    def register_user(self, username, email, password, password_confirm):
        if not self.db:
            messagebox.showerror("Erreur", "Base de données non connectée")
            return

        cursor = self.db.cursor()
        try:
            #verifie tous les champs sont remplis
            if not username or not email or not password:
                messagebox.showerror("Erreur", "Veuiller remplir tous les champs.")
                return
            if not re.match(email_regex, email):
                messagebox.showerror("Erreur", "Veuillez entrer un email valide.")
                return
            if not re.match(mdp_regex, password):
                messagebox.showerror("Erreur", "Votre mot de passe doit avoir minimum 8 caracteres.")
                return
            if not password_confirm == password:
                messagebox.showerror("Erreur", "Votre mot de passe doit avoir minimum 8 caracteres.")
                return
            # Vérifie si l'utilisateur existe déjà
            cursor.execute("SELECT * FROM Users WHERE username_Users=%s", 
                          (username,))
            if cursor.fetchone():
                messagebox.showerror("Erreur", "Nom d'utilisateur déjà existant")
                return
            # Vérifie si l'utilisateur existe déjà
            cursor.execute("SELECT * FROM Users WHERE email_Users=%s", 
                          (email,))
            if cursor.fetchone():
                messagebox.showerror("Erreur", "Email déjà existant")
                return


            #hashage
            mdp_bytes = password.encode('utf-8')
            hash = bcrypt.hashpw(mdp_bytes, bcrypt.gensalt())

            # Ajoute le nouvel utilisateur
            cursor.execute(
                "INSERT INTO Users (username_Users, email_Users, password_Users) VALUES (%s, %s, %s)",
                (username, email, hash)
            )
            
            self.db.commit()
            messagebox.showinfo("Succès", "Compte créé avec succès!")
            self.show_login_page()
        except Error as e:
            messagebox.showerror("Erreur DB", f"Erreur lors de l'inscription: {e}")
        finally:
            cursor.close()

    def load_image(self, path):
        if os.path.exists(path):
            return Image.open(path)
        return None

    def slide_animation(self, from_frame, to_frame, direction, x_sart = 300):
        """Effectue le slide entre deux frames"""
        x_start = x_sart if direction == "left" else -x_sart
        x_end = 0
        
        # Position initiale
        to_frame.place(x=x_start, y=0, relwidth=1, relheight=1)
        
        def animate(frame_x):
            if (direction == "left" and frame_x > x_end) or (direction == "right" and frame_x < x_end):
                from_frame.place(x=frame_x - x_end if direction == "left" else frame_x + x_end)
                to_frame.place(x=frame_x)
                self.root.after(5, lambda: animate(frame_x - 25 if direction == "left" else frame_x + 25))
            else:
                from_frame.place_forget()
                to_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        animate(x_start)

    def show_login_page(self, anim):
        if anim:
            self.slide_animation(self.register_frame, self.login_frame, "right")
        else:
            self.slide_animation(self.register_frame, self.login_frame, "right", x_sart=0)

    def show_register_page(self):
        self.slide_animation(self.login_frame, self.register_frame, "left")
    def show_main_interface(self):
    # Effacer le contenu actuel (login/register)
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Créer le frame principal de l'app
        self.main_app_frame = tk.Frame(self.main_container, bg="white")
        self.main_app_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(self.main_app_frame, text=f"Bienvenue, utilisateur {self.current_user} !", font=("Arial", 18), bg="white")
        welcome_label.pack(pady=30)
        logout_btn = ctk.CTkButton(self.main_app_frame, text="Déconnexion", command=self.logout_user,
                           fg_color="#E74C3C", hover_color="#C0392B", text_color="white",
                           font=("Arial", 12), corner_radius=10, width=150, height=40)
        logout_btn.pack(pady=10)
    def logout_user(self):
        confirm = messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?")
        if confirm:
            self.current_user = None


    def build_login_form(self):
        self.current_image = self.login_img

        # Frame image droite
        right_frame = tk.Frame(self.login_frame, bg="black")
        right_frame.pack(side="right", fill="both", expand=True)

        if self.current_image:
            self.login_tk_image = ImageTk.PhotoImage(self.current_image.resize((500, 600)))
            bg_label = tk.Label(right_frame, image=self.login_tk_image)
            bg_label.place(relwidth=1, relheight=1)
        def resize_login_image(event):
            if self.login_img:
                img_resized = self.login_img.resize((event.width, event.height))
                self.login_tk_image = ImageTk.PhotoImage(img_resized)
                bg_label.config(image=self.login_tk_image)

        bg_label = tk.Label(right_frame)
        bg_label.place(relwidth=1, relheight=1)
        right_frame.bind("<Configure>", resize_login_image)

        # Frame formulaire gauche
        left_frame = tk.Frame(self.login_frame, bg="white")
        left_frame.pack(side="left", fill="both", expand=True)

        form_container = ctk.CTkFrame(left_frame, fg_color="white", corner_radius=0)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        title = ctk.CTkLabel(form_container, text="SE CONNECTER", font=("Arial", 24, "bold"), text_color="#1C1C1C")
        title.pack(pady=(0, 10))

        # Sous-titre
        subtitle = ctk.CTkLabel(form_container, 
                              text="Bienvenue ! Veuillez vous connecter à votre compte.",
                              font=("Arial", 10), text_color="#525252")
        subtitle.pack()

        # Champ utilisateur
        self.login_username = ctk.CTkEntry(form_container, 
                                         placeholder_text="Nom d'utilisateur ou email",
                                         fg_color="#F0EDFF", 
                                         text_color="#1C1C1C",
                                         border_width=0, 
                                         corner_radius=10, 
                                         width=240, 
                                         height=40)
        self.login_username.pack(pady=10)

        # Champ mot de passe
        self.login_password = ctk.CTkEntry(form_container, 
                                         placeholder_text="Mot de passe",
                                         fg_color="#F0EDFF", 
                                         text_color="#1C1C1C",
                                         border_width=0, 
                                         corner_radius=10, 
                                         width=240, 
                                         height=40,
                                         show="*")
        self.login_password.pack(pady=10)

        # Bouton connexion
        login_btn = ctk.CTkButton(form_container, 
                                 text="Se connecter",
                                 fg_color="#5038ED", 
                                 hover_color="#3d2fc2",
                                 text_color="white", 
                                 corner_radius=10,
                                 font=("Arial", 12, "bold"), 
                                 width=240, 
                                 height=40, 
                                 command=lambda: self.login_user(
                                      self.login_username.get(),
                                      self.login_password.get()
                                  )
                                )
        login_btn.pack(pady=20)

        # Lien inscription
        register_link = ctk.CTkLabel(form_container,
                                   text="Vous n'avez pas de compte ? Inscrivez-vous.",
                                   text_color="#5038ED", 
                                   font=("Arial", 10, "bold"),
                                   cursor="hand2")
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.show_register_page())

    def build_register_form(self):
        """Construction COMPLÈTE de votre formulaire register"""
        self.current_image = self.register_img

        # Frame image gauche
        left_frame = tk.Frame(self.register_frame, bg="black")
        left_frame.pack(side="left", fill="both", expand=True)

        if self.current_image:
            self.register_tk_image = ImageTk.PhotoImage(self.current_image.resize((500, 600)))
            bg_label = tk.Label(left_frame, image=self.register_tk_image)
            bg_label.place(relwidth=1, relheight=1)
            
        def resize_login_image(event):
            if self.register_img:
                img_resized = self.register_img.resize((event.width, event.height))
                self.register_tk_image = ImageTk.PhotoImage(img_resized)
                bg_label.config(image=self.register_tk_image)

        bg_label = tk.Label(left_frame)
        bg_label.place(relwidth=1, relheight=1)
        left_frame.bind("<Configure>", resize_login_image)

        # Frame formulaire droite
        right_frame = tk.Frame(self.register_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        form_container = ctk.CTkFrame(right_frame, fg_color="white", corner_radius=0)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        title = ctk.CTkLabel(form_container, text="INSCRIPTION", font=("Arial", 24, "bold"), text_color="#1C1C1C")
        title.pack(pady=(0, 10))

        # Sous-titre
        subtitle = ctk.CTkLabel(form_container, 
                               text="Créez votre compte pour commencer.",
                               font=("Arial", 10), 
                               text_color="#525252")
        subtitle.pack()

        # Champ nom d'utilisateur
        self.register_username = ctk.CTkEntry(form_container,
                                            placeholder_text="Nom d'utilisateur",
                                            fg_color="#F0EDFF",
                                            text_color="#1C1C1C",
                                            border_width=0,
                                            corner_radius=10,
                                            width=240,
                                            height=40)
        self.register_username.pack(pady=10)

        # Champ email
        self.register_email = ctk.CTkEntry(form_container,
                                         placeholder_text="E-mail",
                                         fg_color="#F0EDFF",
                                         text_color="#1C1C1C",
                                         border_width=0,
                                         corner_radius=10,
                                         width=240,
                                         height=40)
        self.register_email.pack(pady=10)

        # Champ mot de passe
        self.register_password = ctk.CTkEntry(form_container,
                                            placeholder_text="Mot de passe",
                                            fg_color="#F0EDFF",
                                            text_color="#1C1C1C",
                                            border_width=0,
                                            corner_radius=10,
                                            width=240,
                                            height=40,
                                            show="*")
        self.register_password.pack(pady=10)

        # confirmation mot de passe
        self.register_password_confirm = ctk.CTkEntry(form_container,
                                            placeholder_text="Confirmer le mot de passe",
                                            fg_color="#F0EDFF",
                                            text_color="#1C1C1C",
                                            border_width=0,
                                            corner_radius=10,
                                            width=240,
                                            height=40,
                                            show="*")
        self.register_password_confirm.pack(pady=10)

        # Bouton inscription
        register_btn = ctk.CTkButton(form_container,
                                    text="Créer son compte",
                                    fg_color="#5038ED",
                                    hover_color="#3d2fc2",
                                    text_color="white",
                                    corner_radius=10,
                                    font=("Arial", 12, "bold"),
                                    width=240,
                                    height=40, 
                                    command=lambda: self.register_user(
                                        self.register_username.get(),
                                        self.register_email.get(),
                                        self.register_password.get(),
                                        self.register_password_confirm.get()
                                    )
                                    )
        register_btn.pack(pady=20)

        # Lien connexion
        login_link = ctk.CTkLabel(form_container,
                                text="Vous avez déjà un compte ? Se connecter",
                                text_color="#5038ED",
                                font=("Arial", 10, "bold"),
                                cursor="hand2")
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.show_login_page(True))

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()