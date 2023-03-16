import mysql.connector
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

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
            db.execute("UPDATE Produits SET nom = ? description = ? prix = ? quantite = ? id_categorie = ?)\
                       WHERE id = ?", [nom, description, prix, quantite, cat, produit[0]])
    except:
        print("erreur")
    

def supprimer_produit():
    try:
        produit = selection_produit()
        db.execute("DELETE FROM Produits WHERE id = ?", [produit[0]])
        bdd.commit()
    except:
        print("aucun produit selectionné")


def ajouter_categorie():

    nom = nom_cat_entry.get()
    if nom != "":
        db.execute("INSERT INTO Categories (nom) VALUES (?)", [nom])
        bdd.commit()


def modifier_categorie():
    categorie = selection_categorie()
    nom = nom_cat_entry.get()
    if nom != "":
        db.execute("UPDATE Categories SET nom = ? WHERE id = ?", [nom, categorie[1]])
        bdd.commit()

def supprimer_categorie():
    try:
        categorie = selection_categorie()
        db.execute("DELETE FROM Categories WHERE id = ?", [categorie[1]])
        bdd.commit()
    except:
        print("aucune categorie selectionné")


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


#Vue Produits
frame_produit = Frame(fenetre)
colonnes_produits = ('id', 'nom', 'prix', 'quantité', 'catégorie')

arbre_produits = Treeview(frame_produit, columns=colonnes_produits, show='headings')

db.execute("SELECT Produits.id, Produits.nom, prix, quantite, Categories.nom \
           FROM Produits JOIN Categories ON id_categorie = Categories.id")
produits = db.fetchall()

for item in colonnes_produits:
    arbre_produits.heading(item, text=item.upper())
for produit in produits:
    arbre_produits.insert('', END, values=produit)

arbre_produits.pack()
frame_produit.grid(row=0, column=0)



#Vue Categories
frame_cat = Frame(fenetre)
colonnes_catégories = ('nom', 'id')
arbre_categories = Treeview(frame_cat, columns=colonnes_catégories, show="headings")

db.execute("SELECT nom, id FROM Categories")
categories = db.fetchall()
cats = dict(categories)

for item in colonnes_catégories:
    arbre_categories.heading(item, text=item.upper())
for categorie in categories:
    arbre_categories.insert('', END, values=categorie)

arbre_categories.pack()

frame_cat.grid(row=0, column=1)



#Formulaire Produit
form_prod_frame = Frame(fenetre)

Label(form_prod_frame, text="Nom: ").grid(row=0, column=0)
nom_entry = Entry(form_prod_frame)
nom_entry.grid(row=0, column=1, columnspan=2)

Label(form_prod_frame, text="Description: ").grid(row=1, column=0)
desc_entry = Entry(form_prod_frame)
desc_entry.grid(row=1, column=1, columnspan=2)

Label(form_prod_frame, text="Prix: ").grid(row=2, column=0)
prix_entry = Entry(form_prod_frame)
prix_entry.grid(row=2, column=1, columnspan=2)

Label(form_prod_frame, text="Quantité: ").grid(row=3, column=0)
quantite_entry = Entry(form_prod_frame)
quantite_entry.grid(row=3, column=1, columnspan=2)

cat_select = StringVar()
Label(form_prod_frame, text="Catégorie: ").grid(row=4, column=0)
cat_options = OptionMenu(form_prod_frame, cat_select, categories[0][0],*[categorie[0] for categorie in categories])
cat_options.grid(row=4, column=1, columnspan=2)

btn_ajout_produit = Button(form_prod_frame, text="Ajouter", command= ajouter_produit).grid(row=5, column=0)
btn_modif_produit = Button(form_prod_frame, text="Modifier", command= modifier_produit).grid(row=5, column=1)
btn_suppr_produit = Button(form_prod_frame, text="Supprimer", command= supprimer_produit).grid(row=5, column=2)

form_prod_frame.grid(row=1,column=0)



#Formulaire Categories
form_cat_frame = Frame(fenetre)

Label(form_cat_frame, text="Nom: ").grid(row=0, column=0)
nom_cat_entry = Entry(form_cat_frame)
nom_cat_entry.grid(row=0, column=1, columnspan=2)

btn_ajout_cat = Button(form_cat_frame, text="Ajouter", command= ajouter_categorie).grid(row=1, column=0)
btn_modif_cat = Button(form_cat_frame, text="Modifier", command= modifier_categorie).grid(row=1, column=1)
btn_suppr_cat = Button(form_cat_frame, text="Supprimer", command= supprimer_categorie).grid(row=1, column=2)

form_cat_frame.grid(row=1, column=1)



fenetre.mainloop()