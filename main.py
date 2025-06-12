def add_recipe_button():
    try:
        # Validation du nom de la recette (lettres, espaces, et certains caractères spéciaux)
        name_input = name.get().strip()
        if not name_input:
            raise ValueError("Le nom de la recette est requis.")
        if any(char.isdigit() for char in name_input):
            raise ValueError("Le nom de la recette ne doit pas contenir de chiffres.")

        # Validation du nombre de personnes (doit être un entier positif)
        people_input = people.get().strip()
        if not people_input:
            raise ValueError("Notez un nombre de personne(s).")
        try:
            people_value = int(people_input)
            if people_value <= 0:
                raise ValueError("Le nombre de personnes doit être un entier positif.")
        except ValueError:
            raise ValueError("Le nombre de personnes doit être un entier valide.")

        # Validation du temps de préparation (doit être un nombre positif, entier ou flottant)
        time_input = time.get().strip()
        if not time_input:
            raise ValueError("Notez un temps de préparation estimé.")
        try:
            time_value = float(time_input)
            if time_value <= 0:
                raise ValueError("Le temps de préparation doit être un nombre positif.")
        except ValueError:
            raise ValueError("Le temps de préparation doit être un nombre valide.")

        # Validation des champs ingrédients et instructions
        if not ing_text.get("1.0", tk.END).strip():
            raise ValueError("Remplissez la liste d'ingrédients.")
        if not ins_text.get("1.0", tk.END).strip():
            raise ValueError("Remplissez un minimum les instructions pour faire la recette.")

        # Ajout de la recette
        motor.add_recipe(
            table_var.get(),
            name_input,
            people_value,
            time_value,
            ing_text.get("1.0", tk.END).strip(),
            ins_text.get("1.0", tk.END).strip()
        )

        # Vider les champs après ajout
        name_entry.delete(0, tk.END)
        ppl_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        ing_text.delete("1.0", tk.END)
        ins_text.delete("1.0", tk.END)

        Messagebox.show_info(title="Succès", message="Recette ajoutée avec succès !")
    except ValueError as ve:
        Messagebox.show_error(title="Erreur", message=str(ve))