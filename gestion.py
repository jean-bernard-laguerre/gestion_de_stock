import mysql.connector
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import csv

bdd = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "Boutique"
)
db = bdd.cursor(prepared=True)

fenetre = Tk()
fenetre.title("Gestion de stock")


#Fonctions de gestion
def ajouter_produit():

    try:
        nom = nom_entry.get()
        description = desc_entry.get()
        prix = int(prix_entry.get())
        quantite = int(quantite_entry.get())
        cat = cats[cat_select.get()]

        if nom != "" and description != "":
            db.execute("INSERT INTO Produits (nom, description, prix, quantite, id_categorie)\
                       VALUES (?,?,?,?,?)", [nom, description, prix, quantite, cat])
            bdd.commit()
            actualiser()
    except:
        print("erreur")

def modifier_produit():
    produit = selection_produit()

    try:
        nom = nom_entry.get()
        description = desc_entry.get()
        prix = int(prix_entry.get())
        quantite = int(quantite_entry.get())
        cat = cats[cat_select.get()]

        if nom != "" and description != "":
            db.execute("UPDATE Produits SET nom = ?, description = ?, prix = ?, quantite = ?, id_categorie = ?\
                       WHERE id = ?", [nom, description, prix, quantite, cat, produit[0]])
            bdd.commit()
            actualiser()
    except:
        print("erreur")
    
def supprimer_produit():
    try:
        produit = selection_produit()
        db.execute("DELETE FROM Produits WHERE id = ?", [produit[0]])
        bdd.commit()
        actualiser()
    except:
        print("aucun produit selectionné")

def ajouter_categorie():

    nom = nom_cat_entry.get()
    if nom != "":
        db.execute("INSERT INTO Categories (nom) VALUES (?)", [nom])
        bdd.commit()
        actualiser()

def modifier_categorie():
    categorie = selection_categorie()
    nom = nom_cat_entry.get()
    if nom != "":
        db.execute("UPDATE Categories SET nom = ? WHERE id = ?", [nom, categorie[1]])
        bdd.commit()
        actualiser()

def supprimer_categorie():
    try:
        categorie = selection_categorie()
        db.execute("DELETE FROM Categories WHERE id = ?", [categorie[1]])
        bdd.commit()
        actualiser()
    except:
        print("aucune categorie selectionné")


#Actualise les produits
def actualiser(c_nom = ""):
    global arbre_produits, produits, arbre_categories, categories, cats


    arbre_produits.destroy()
    arbre_produits = Treeview(frame_produit, columns=colonnes_produits, show='headings')

    produits = recup_produits(c_nom)
    arbre_produits.grid(row=1,column=0, padx=10)

    arbre_categories.destroy()
    arbre_categories = Treeview(frame_cat, columns=colonnes_catégories, show="headings")

    categories =  recup_categories()
    cats = dict(categories)
    arbre_categories.grid(row=0, column=0, padx=10)
    
    cat_options = OptionMenu(form_prod_frame, cat_select, categories[0][0],*[categorie[0] for categorie in categories])
    filtre_options = OptionMenu(filtre_frame, filtre_select, categories[0][0],*[categorie[0] for categorie in categories]+[""])
    cat_options.grid(row=5, column=1, columnspan=2)
    filtre_options.grid(row=0, column=1, columnspan=2)
    

#Retourne le produit selectionné
def selection_produit():
    for prod in arbre_produits.selection():
        select_prod = arbre_produits.item(prod)
        retour = select_prod['values']
    return retour

#Retourne la categorie selectionnée
def selection_categorie():
    for cat in arbre_categories.selection():
        select_cat = arbre_categories.item(cat)
        retour = select_cat['values']
    return retour

#Rentre les propriétés du produit selectionné dans le formulaire
def auto_comp_prod(event):

    produit = selection_produit()
    
    nom_entry.delete(0, END)
    nom_entry.insert(0, produit[1])

    desc_entry.delete(0, END)
    desc_entry.insert(0, produit[2])
    
    prix_entry.delete(0, END)
    prix_entry.insert(0, produit[3])

    quantite_entry.delete(0, END)
    quantite_entry.insert(0, produit[4])

    cat_select.set(produit[5])

def exporter_produits():
    f = open("produits.csv", "w")
    export = csv.writer(f, lineterminator="\n")
    export.writerow(colonnes_produits)
    for produit in produits:
        export.writerow(produit)
    f.close()

#Vue Produits
frame_produit = LabelFrame(fenetre, text="Produits")
colonnes_produits = ('id', 'nom', 'description', 'prix', 'quantité', 'catégorie')


arbre_produits = Treeview(frame_produit, columns=colonnes_produits, show='headings')

def recup_produits(c_nom = ""):

    if c_nom != "":
        db.execute("SELECT Produits.id, Produits.nom, description, prix, quantite, Categories.nom \
                FROM Produits JOIN Categories ON id_categorie = Categories.id \
                WHERE Categories.nom = ?", [c_nom])
    else:
        db.execute("SELECT Produits.id, Produits.nom, description, prix, quantite, Categories.nom \
                FROM Produits JOIN Categories ON id_categorie = Categories.id")

    produits = db.fetchall()

    for i,item in enumerate(colonnes_produits):
        arbre_produits.column(f"#{i}",width= 100)
        arbre_produits.heading(item, text=item.upper())
    for produit in produits:
        arbre_produits.insert('', END, values=produit)

    arbre_produits.bind('<<TreeviewSelect>>', auto_comp_prod)

    return produits

produits = recup_produits()

arbre_produits.grid(row=1,column=0, padx=10)
frame_produit.grid(row=0, column=0, columnspan=2, pady=5)



#Vue Categories
frame_cat = Labelframe(fenetre, text="Categories", padding=5)
colonnes_catégories = ('nom', 'id')
arbre_categories = Treeview(frame_cat, columns=colonnes_catégories, show="headings")

def recup_categories():
    db.execute("SELECT nom, id FROM Categories")
    categories = db.fetchall()
    

    for item in colonnes_catégories:
        arbre_categories.heading(item, text=item.upper())
    for categorie in categories:
        arbre_categories.insert('', END, values=categorie)

    return categories

categories = recup_categories()
cats = dict(categories)

arbre_categories.grid(row=0, column=0, padx=10)
frame_cat.grid(row=1, column=0, pady=5, sticky="w")



#Formulaire Produit
form_prod_frame = Frame(frame_produit)

Label(form_prod_frame, text="Nom: ").grid(row=1, column=0)
nom_entry = Entry(form_prod_frame)
nom_entry.grid(row=1, column=1, columnspan=2)

Label(form_prod_frame, text="Description: ").grid(row=2, column=0)
desc_entry = Entry(form_prod_frame)
desc_entry.grid(row=2, column=1, columnspan=2)

Label(form_prod_frame, text="Prix: ").grid(row=3, column=0)
prix_entry = Entry(form_prod_frame)
prix_entry.grid(row=3, column=1, columnspan=2)

Label(form_prod_frame, text="Quantité: ").grid(row=4, column=0)
quantite_entry = Entry(form_prod_frame)
quantite_entry.grid(row=4, column=1, columnspan=2)

cat_select = StringVar()
Label(form_prod_frame, text="Catégorie: ").grid(row=5, column=0)
cat_options = OptionMenu(form_prod_frame, cat_select, categories[0][0],*[categorie[0] for categorie in categories])
cat_options.grid(row=5, column=1, columnspan=2)

btn_ajout_produit = Button(form_prod_frame, text="Ajouter", command= ajouter_produit).grid(row=0, column=0)
btn_modif_produit = Button(form_prod_frame, text="Modifier", command= modifier_produit).grid(row=0, column=1)
btn_suppr_produit = Button(form_prod_frame, text="Supprimer", command= supprimer_produit).grid(row=0, column=2)

form_prod_frame.grid(row=1,column=1, padx=10)



#Formulaire Categories
form_cat_frame = Frame(frame_cat)

Label(form_cat_frame, text="Nom: ").grid(row=0, column=0)
nom_cat_entry = Entry(form_cat_frame)
nom_cat_entry.grid(row=0, column=1, columnspan=2)

btn_ajout_cat = Button(form_cat_frame, text="Ajouter", command= ajouter_categorie).grid(row=1, column=0)
btn_modif_cat = Button(form_cat_frame, text="Modifier", command= modifier_categorie).grid(row=1, column=1)
btn_suppr_cat = Button(form_cat_frame, text="Supprimer", command= supprimer_categorie).grid(row=1, column=2)

form_cat_frame.grid(row=0, column=1, padx=10)

#Filtre
filtre_frame = Frame(frame_produit)
filtre_select = StringVar()
Label(filtre_frame, text="Filtre: ").grid(row=0, column=0)
filtre_options = OptionMenu(filtre_frame, filtre_select, categories[0][0],*[categorie[0] for categorie in categories]+[""])
filtre_options.grid(row=0, column=1, columnspan=2)
btn_filtre = Button(filtre_frame, text="Filtrer", command= lambda: actualiser(filtre_select.get())).grid(row=0, column=3)
filtre_frame.grid(row=0, column=0)

#Export
btn_export_produit = Button(fenetre, text="Export CSV Produits", command= exporter_produits).grid(row=1, column=1)



fenetre.mainloop()
db.close()