import tkinter as tkinter
import ttkbootstrap as tk
import motor
from ttkbootstrap.dialogs import Messagebox

def build_app():
    """
        Cette fonction crée et configure la fenêtre principale de l'application.

        Retourne :
            tk.Window : La fenêtre principale de l'application, centrée avec un thème défini.
        """
    global root
    root = tk.Window(
        title="Mon gestionnaire de recette",
        themename="morph",
        minsize=(400,650),
    )

    build_frame(root) # onglets

    root.place_window_center()

    return root

def create_tab_accueil(notebook):
    """
        Cette fonction crée l'onglet 'Accueil' avec un bouton pour afficher une recette aléatoire.

        Paramètres :
            notebook (tk.Notebook) : Le conteneur d'onglets auquel ajouter l'onglet 'Accueil'.

        Effet :
            Ajoute un onglet avec un label, un bouton pour afficher une recette aléatoire et une zone de texte pour afficher les détails.
        """

    tab = tk.Frame(notebook)

    presentation_label = tk.Label(tab, justify="center",font=("Arial", 16) ,
                        text="Si vous désirez une recette aléatoire cliquez sur le bouton ci-dessous, sinon visitez un des onglets !")
    presentation_label.pack()

    button_random = tk.Button(tab, text="Affiche une recette aléatoire !", style="primary", command=show_random_recipe)
    button_random.pack(pady=15, padx=200, ipadx=5, ipady=5, anchor="center", fill="x")

    # Frame pour contenir le Text et la Scrollbar
    text_frame = tk.Frame(tab)
    text_frame.pack(pady=10)

    # Ajout widget Text pour afficher la recette aléatoire
    global recipe_text
    recipe_text = tk.Text(text_frame, height=20, width=80, state="disabled") # state = lecture seule
    recipe_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=recipe_text.yview)
    scrollbar.pack(side="right", fill="y")

    # Configurer la Scrollbar pour le text
    recipe_text.config(yscrollcommand=scrollbar.set)

    notebook.add(tab, text="Accueil")

def show_random_recipe():
    """
        Cette fonction affiche une recette aléatoire dans la zone de texte de l'onglet 'Accueil'.

        Effet :
            Récupère une recette aléatoire via motor.get_random_recipe() et l'affiche dans la zone de texte.
            Si aucune recette n'est disponible, affiche un message d'erreur.
        """
    recipe = motor.get_random_recipe()
    if recipe:
        recipe_text.config(state='normal')  # Réactiver pour insérer du texte // disabled
        recipe_text.delete(1.0, tk.END)  # Effacer l'affichage d'avant
        recipe_text.insert(tk.END, f"""
Nom: {recipe[1]}

Nombre de personnes: {recipe[2]}

Temps de préparation: {recipe[3]} minutes

Ingrédients:

{recipe[4]}

Instructions:

{recipe[5]}""""")
        recipe_text.config(state='disabled')  # on rebloque pour pas pouvoir écrire
    else: # si rien de disponible
        recipe_text.config(state='normal')
        recipe_text.delete(1.0, tk.END)
        recipe_text.insert(tk.END, "Aucune recette disponible.")
        recipe_text.config(state='disabled')

def create_tab_entree(notebook):
    """
        Cette fonction crée l'onglet 'Entrée' pour afficher et gérer les recettes d'entrées.

        Paramètres :
            notebook (tk.Notebook) : Le conteneur d'onglets auquel ajouter l'onglet 'Entrée'.

        Effet :
            Ajoute un onglet avec une liste des recettes, une zone de texte pour afficher les détails et un bouton de suppression.
        """

    global entree_listbox, entree_recipes

    tab1 = tk.Frame(notebook)

    entree_label = tk.Label(tab1, justify="center", font=("Arial", 16),
                                  text="Voici les différentes recettes que vous possédez dans la catégorie entrée")
    entree_label.pack()

    # Lisbtbox (peut être mieux mais en attendant on met tkinter aussi)
    entree_listbox = tkinter.Listbox(tab1, width=50, height=10)
    entree_listbox.pack(pady=10)

    # Ajouter les recettes à la Listbox
    entree_recipes = motor.get_recipes_by_category("entree")

    for recipe in entree_recipes:
        entree_listbox.insert(tk.END, recipe[1]) #Le 1 permet de montrer le nom (1ere pos)

    entree_frame = tk.Frame(tab1)
    entree_frame.pack(pady=10)

    entree_text = tk.Text(entree_frame, height=20, width=80, state="disabled")
    entree_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(entree_frame, command=entree_text.yview)
    scrollbar.pack(side="right", fill="y")
    entree_text.config(yscrollcommand=scrollbar.set)

    def entree_select(event):
        """
                Cette fonction interne affiche les détails d'une recette sélectionnée dans la Listbox.

                Paramètres :
                    event : Événement de sélection dans la Listbox.

                Effet :
                    Affiche les détails de la recette sélectionnée dans la zone de texte.
                """
        selection = entree_listbox.curselection()
        if selection:
            index = selection[0]
            recipe = entree_recipes[index]
            entree_text.config(state="normal")
            entree_text.delete("1.0", tk.END)
            entree_text.insert(tk.END, f"""
Nom: {recipe[1]}

Nombre de personnes: {recipe[2]}

Temps de préparation: {recipe[3]} minutes
    
Ingrédients:
    
{recipe[4]}

Instructions:

{recipe[5]}""")
        entree_text.config(state="disabled")

    delete_button = tk.Button(entree_frame, text="Supprimer la recette",command=lambda: button_delete("entree", entree_listbox, entree_text, entree_recipes),bootstyle="danger")
    delete_button.pack(pady=5, padx=3)

    # Liaison de l'événement
    entree_listbox.bind("<<ListboxSelect>>", entree_select)


    notebook.add(tab1, text="Entrée")

def create_tab_plat(notebook):
    """
        Cette fonction crée l'onglet 'Plat' pour afficher et gérer les recettes de plats principaux.

        Paramètres :
            notebook (tk.Notebook) : Le conteneur d'onglets auquel ajouter l'onglet 'Plat'.

        Effet :
            Ajoute un onglet avec une liste des recettes, une zone de texte pour afficher les détails et un bouton de suppression.
        """

    global plat_listbox, plat_recipes

    tab2 = tk.Frame(notebook)

    plat_label = tk.Label(tab2, justify="center", font=("Arial", 16),
                            text="Voici les différentes recettes que vous possédez dans la catégorie plat")
    plat_label.pack()

    plat_listbox = tkinter.Listbox(tab2, width=50, height=10)
    plat_listbox.pack(pady=10)

    plat_recipes = motor.get_recipes_by_category("plat")

    for recipe in plat_recipes:
        plat_listbox.insert(tk.END, recipe[1])

    plat_frame = tk.Frame(tab2)
    plat_frame.pack(pady=10)

    plat_text = tk.Text(plat_frame, height=20, width=80, state="disabled")
    plat_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(plat_frame, command=plat_text.yview)
    scrollbar.pack(side="right", fill="y")
    plat_text.config(yscrollcommand=scrollbar.set)

    def plat_select(event):
        """
                Cette fonction interne affiche les détails d'une recette sélectionnée dans la Listbox.

                Paramètres :
                    event : Événement de sélection dans la Listbox.

                Effet :
                    Affiche les détails de la recette sélectionnée dans la zone de texte.
                """
        selection = plat_listbox.curselection()
        if selection:
            plat_recipes = motor.get_recipes_by_category("plat")
            index = selection[0]
            recipe = plat_recipes[index]
            plat_text.config(state="normal")
            plat_text.delete("1.0", tk.END)
            plat_text.insert(tk.END, f"""
Nom: {recipe[1]}

Nombre de personnes: {recipe[2]}

Temps de préparation: {recipe[3]} minutes

Ingrédients:

{recipe[4]}

Instructions:

{recipe[5]}""")
        plat_text.config(state="disabled")

    plat_listbox.bind("<<ListboxSelect>>", plat_select)

    delete_button = tk.Button(plat_frame, text="Supprimer la recette",command=lambda: button_delete("plat", plat_listbox, plat_text, plat_recipes),bootstyle="danger")
    delete_button.pack(pady=5, padx=3)

    notebook.add(tab2, text="Plat")

def create_tab_dessert(notebook):
    """
        Cette fonction crée l'onglet 'Dessert' pour afficher et gérer les recettes de desserts.

        Paramètres :
            notebook (tk.Notebook) : Le conteneur d'onglets auquel ajouter l'onglet 'Dessert'.

        Effet :
            Ajoute un onglet avec une liste des recettes, une zone de texte pour afficher les détails et un bouton de suppression.
        """

    global dessert_listbox, dessert_recipes

    tab3 = tk.Frame(notebook)

    dessert_label = tk.Label(tab3, justify="center", font=("Arial", 16),
                            text="Voici les différentes recettes que vous possédez dans la catégorie dessert")
    dessert_label.pack()

    dessert_listbox = tkinter.Listbox(tab3, width=50, height=10)
    dessert_listbox.pack(pady=10)

    dessert_recipes = motor.get_recipes_by_category("dessert")

    for recipe in dessert_recipes:
        dessert_listbox.insert(tk.END, recipe[1])

    dessert_frame = tk.Frame(tab3)
    dessert_frame.pack(pady=10)

    dessert_text = tk.Text(dessert_frame, height=20, width=80, state="disabled")
    dessert_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(dessert_frame, command=dessert_text.yview)
    scrollbar.pack(side="right", fill="y")
    dessert_text.config(yscrollcommand=scrollbar.set)

    def dessert_select(event):
        """
                Cette fonction interne affiche les détails d'une recette sélectionnée dans la Listbox.

                Paramètres :
                    event : Événement de sélection dans la Listbox.

                Effet :
                    Affiche les détails de la recette sélectionnée dans la zone de texte.
                """
        selection = dessert_listbox.curselection()
        if selection:
            dessert_recipes = motor.get_recipes_by_category("dessert")
            index = selection[0]
            recipe = dessert_recipes[index]
            dessert_text.config(state="normal")
            dessert_text.delete("1.0", tk.END)
            dessert_text.insert(tk.END, f"""
Nom: {recipe[1]}

Nombre de personnes: {recipe[2]}

Temps de préparation: {recipe[3]} minutes

Ingrédients:

{recipe[4]}

Instructions:

{recipe[5]}""")
            dessert_text.config(state="disabled")

    dessert_listbox.bind("<<ListboxSelect>>", dessert_select)

    delete_button = tk.Button(dessert_frame, text="Supprimer la recette",command=lambda: button_delete("dessert", dessert_listbox, dessert_text, dessert_recipes),bootstyle="danger")
    delete_button.pack(pady=5, padx=3)

    notebook.add(tab3, text="Dessert")

def create_tab_ajout(notebook):
    """
        Cette fonction crée l'onglet 'Ajout' pour permettre l'ajout de nouvelles recettes.

        Paramètres :
            notebook (tk.Notebook) : Le conteneur d'onglets auquel ajouter l'onglet 'Ajout'.

        Effet :
            Ajoute un onglet avec des champs pour entrer les détails d'une recette et un bouton pour l'ajouter à la base de données.
        """

    tab4 = tk.Frame(notebook)

    add_label = tk.Label(tab4, justify="center", font=("Arial", 16),
                            text="Ici vous pourrez ajouter une recette")
    add_label.pack()

    choice_lab = tk.Label(tab4, justify="center", text="Choisissez une catégorie :")
    choice_lab.pack()

    table_options = ["entree", "plat", "dessert"]

    table_var = tk.StringVar(value=table_options[0]) # on initie à entrée, on evite les erreurs de mauvaise table

    table_combo = tk.Combobox(tab4, values=table_options, textvariable=table_var, bootstyle="secondary", width=30)
    table_combo.pack(pady=5)

    #Variables pour récupérer les données

    name = tk.StringVar()

    #Label + entry pour récup les données et aider à la compréhension des champs

    name_lab = tk.Label(tab4, text="Nom de la recette: ")
    name_lab.pack(pady = 5)

    name_entry = tk.Entry(tab4, textvariable=name)
    name_entry.pack(pady = 2)

    ppl_lab = tk.Label(tab4, text="Nombre de personnes: ")
    ppl_lab.pack(pady = 5)

    #pour éviter des erreurs à cause de str sur des int on ne met pas de textvariable

    ppl_entry = tk.Entry(tab4)
    ppl_entry.pack(pady = 2)

    time_lab = tk.Label(tab4, text="Temps de préparation (min): ")
    time_lab.pack(pady = 5)

    time_entry = tk.Entry(tab4)
    time_entry.pack(pady = 2)

    # comme text, on peut pas récup les données, on doit les prendre avec un .get()

    ing_label = tk.Label(tab4, text="Ingrédients: ")
    ing_label.pack(pady=5)

    ing_frame = tk.Frame(tab4)
    ing_frame.pack(pady=2)

    ing_text = tk.Text(ing_frame, height=5, width=50)
    ing_text.pack(side="left")

    ing_scrollbar = tk.Scrollbar(ing_frame, orient="vertical", command=ing_text.yview)
    ing_scrollbar.pack(side="right", fill="y")

    ing_text.config(yscrollcommand=ing_scrollbar.set)

    ins_lab = tk.Label(tab4, text="Instructions:")
    ins_lab.pack(pady = 5)

    ins_frame = tk.Frame(tab4)
    ins_frame.pack(pady=2)

    ins_text = tk.Text(ins_frame, height=5, width=50)
    ins_text.pack(side="left")

    ins_scrollbar = tk.Scrollbar(ins_frame, orient="vertical", command=ins_text.yview)
    ins_scrollbar.pack(side="right", fill = "y")

    ins_text.config(yscrollcommand=ins_scrollbar.set)


    def add_recipe_button():
        """
                Cette fonction interne valide et ajoute une recette à la base de données.

                Effet :
                    Vérifie les entrées utilisateur, ajoute la recette via motor.add_recipe() et affiche un message de succès ou d'erreur.
                """
        try:
            name_input = name.get().strip()
            if not name_input:
                raise ValueError("Le nom de la recette est requis.")
            if any(char.isdigit() for char in name_input):
                raise ValueError("Le nom de la recette ne doit pas contenir de chiffres.")

            # Validation du champ 'nombre de personnes'
            people_input = ppl_entry.get().strip()  # Récupérer directement depuis l'Entry
            if not people_input:
                raise ValueError("Le nombre de personnes est requis.")
            try:
                people_val = int(people_input)
                if people_val <= 0:
                    raise ValueError("Le nombre de personnes doit être un entier positif.")
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError("Le nombre de personnes doit être un nombre entier valide.")
                raise ValueError("Le nombre de personnes doit être un entier positif.")

            # Validation du champ 'temps de préparation'
            time_input = time_entry.get().strip()  # Récupérer directement depuis l'Entry
            if not time_input:
                raise ValueError("Le temps de préparation est requis.")
            try:
                time_val = int(time_input)
                if time_val <= 0:
                    raise ValueError("Le temps de préparation doit être un entier positif.")
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError("Le temps de préparation doit être un nombre entier valide.")
                raise ValueError("Le temps de préparation doit être un entier positif.")

            ing_input = ing_text.get("1.0", tk.END).strip()
            if not ing_input:
                raise ValueError("Remplissez la liste d'ingrédients.")

            ins_input = ins_text.get("1.0", tk.END).strip()
            if not ins_input:
                raise ValueError("Remplissez un minimum les instructions pour faire la recette.")

            motor.add_recipe(
                table_var.get(),
                name_input,
                people_val,
                time_val,
                ing_input,
                ins_input
            )
            global entree_recipes, plat_recipes, dessert_recipes
            if table_var.get() == "entree":
                entree_recipes = motor.get_recipes_by_category("entree")
            elif table_var.get() == "plat":
                plat_recipes = motor.get_recipes_by_category("plat")
            elif table_var.get() == "dessert":
                dessert_recipes = motor.get_recipes_by_category("dessert")

            # Vider les champs après ajout
            name_entry.delete(0, tk.END)
            ppl_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)
            ing_text.delete("1.0", tk.END)
            ins_text.delete("1.0", tk.END)

            Messagebox.show_info(title="Succès", message="Recette ajoutée avec succès !")

        except ValueError as ve:
            Messagebox.show_error(title="Erreur", message=str(ve))


    add_button = tk.Button(tab4, text="Ajouter la recette", command=add_recipe_button, bootstyle="success")
    add_button.pack(pady=10)

    notebook.add(tab4, text="Ajout")

def button_delete(table, listbox, text_widget, recipes):
    """
        Cette fonction supprime une recette sélectionnée dans une Listbox et met à jour l'affichage.

        Paramètres :
            table (str) : Nom de la table ('entree', 'plat' ou 'dessert').
            listbox (tk.Listbox) : Listbox contenant les recettes.
            text_widget (tk.Text) : Zone de texte affichant les détails de la recette.
            recipes (list) : Liste des recettes de la catégorie.

        Effet :
            Supprime la recette sélectionnée de la base de données et de la Listbox, puis met à jour l'affichage.
        """
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        recipe = recipes[index]
        motor.delete_recipe(table, recipe[0])
        # Rafraichir la liste des recettes
        listbox.delete(index)
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.config(state="disabled")
        Messagebox.show_info(title="Succès", message="Recette supprimée avec succès !")


def refresh_tab_content(event):
    """
        Cette fonction rafraîchit le contenu des onglets 'Entrée', 'Plat' et 'Dessert' lorsqu'ils sont sélectionnés.

        Paramètres :
            event : Événement de changement d'onglet dans le Notebook.

        Effet :
            Met à jour la Listbox de l'onglet actif avec les recettes actuelles de la catégorie correspondante.
        """
    global entree_recipes, plat_recipes, dessert_recipes
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]

    if selected_tab == "Entrée":
        entree_listbox.delete(0, tk.END)
        entree_recipes = motor.get_recipes_by_category("entree")
        for recipe in entree_recipes:
            entree_listbox.insert(tk.END, recipe[1])

    elif selected_tab == "Plat":
        plat_listbox.delete(0, tk.END)
        plat_recipes = motor.get_recipes_by_category("plat")
        for recipe in plat_recipes:
            plat_listbox.insert(tk.END, recipe[1])

    elif selected_tab == "Dessert":
        dessert_listbox.delete(0, tk.END)
        dessert_recipes = motor.get_recipes_by_category("dessert")
        for recipe in dessert_recipes:
            dessert_listbox.insert(tk.END, recipe[1])


def build_frame(parent:tk.Window):
    """
        Cette fonction crée un Notebook et ajoute les onglets pour l'application.

        Paramètres :
            parent (tk.Window) : La fenêtre principale où placer le Notebook.

        Effet :
            Crée un Notebook avec les onglets 'Accueil', 'Entrée', 'Plat', 'Dessert' et 'Ajout', et lie l'événement de changement d'onglet.
        """

    my_notebook = tk.Notebook(root)
    my_notebook.pack(pady=5, fill = "both", expand = True)

    create_tab_accueil(my_notebook)
    create_tab_entree(my_notebook)
    create_tab_plat(my_notebook)
    create_tab_dessert(my_notebook)
    create_tab_ajout(my_notebook)
    my_notebook.bind("<<NotebookTabChanged>>", refresh_tab_content)


if __name__ == '__main__':
    """
        Point d'entrée principal de l'application.

        Effet :
            Configure la base de données, lance l'application Tkinter et ferme la connexion à la base de données à la fin.
        """
    motor.setup_db()
    app = build_app()
    app.mainloop()
    motor.close_db()