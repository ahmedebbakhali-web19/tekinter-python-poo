import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def connecter_db():
    conn = sqlite3.connect("stagiaires.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS notes
                   (
                       matricule
                       TEXT
                       PRIMARY
                       KEY,
                       nom
                       TEXT,
                       filiere
                       TEXT,
                       note
                       TEXT
                   )
                   """)
    conn.commit()
    conn.close()


def charger_donnees():
    for ligne in tableau.get_children():
        tableau.delete(ligne)

    conn = sqlite3.connect("stagiaires.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    lignes = cursor.fetchall()

    for ligne in lignes:
        tableau.insert("", tk.END, values=ligne)
    conn.close()



def ajouter_stagiaire():
    mat = ent_matricule.get()
    nom = ent_nom.get()
    fil = ent_filiere.get()
    note = ent_note.get()

    if mat == "" or nom == "" or fil == "" or note == "":
        messagebox.showwarning("تنبيه", "الرجاء ملء جميع الحقول!")
        return

    try:
        conn = sqlite3.connect("stagiaires.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes VALUES (?, ?, ?, ?)", (mat, nom, fil, note))
        conn.commit()
        conn.close()
        charger_donnees()  # تحديث الجدول فوراً
        vider_champs()
        messagebox.showinfo("نجاح", "تمت إضافة المتدرب بنجاح!")
    except sqlite3.IntegrityError:
        messagebox.showerror("خطأ", "رقم التسجيل هذا موجود مسبقاً!")


def supprimer_stagiaire():
    element_selectionne = tableau.selection()
    if not element_selectionne:
        messagebox.showwarning("تنبيه", "الرجاء تحديد متدرب!")
        return

    confirmation = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد؟")
    if confirmation:
        conn = sqlite3.connect("stagiaires.db")
        cursor = conn.cursor()
        valeurs = tableau.item(element_selectionne[0], 'values')
        cursor.execute("DELETE FROM notes WHERE matricule=?", (valeurs[0],))
        conn.commit()
        conn.close()
        charger_donnees()
        vider_champs()


def modifier_stagiaire():
    element_selectionne = tableau.selection()
    if not element_selectionne:
        messagebox.showwarning("تنبيه", "الرجاء تحديد متدرب!")
        return

    mat = ent_matricule.get()
    nom = ent_nom.get()
    fil = ent_filiere.get()
    note = ent_note.get()

    ancien_mat = tableau.item(element_selectionne[0], 'values')[0]

    conn = sqlite3.connect("stagiaires.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET matricule=?, nom=?, filiere=?, note=? WHERE matricule=?",
                   (mat, nom, fil, note, ancien_mat))
    conn.commit()
    conn.close()
    charger_donnees()
    vider_champs()
    messagebox.showinfo("نجاح", "تم التعديل!")


def rechercher_stagiaire(event=None):
    query = ent_recherche.get()
    conn = sqlite3.connect("stagiaires.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE matricule LIKE ? OR nom LIKE ?",
                   ('%' + query + '%', '%' + query + '%'))
    lignes = cursor.fetchall()

    for ligne in tableau.get_children():
        tableau.delete(ligne)
    for ligne in lignes:
        tableau.insert("", tk.END, values=ligne)
    conn.close()


def selectionner_stagiaire(event):
    element_selectionne = tableau.selection()
    if element_selectionne:
        vider_champs()
        valeurs = tableau.item(element_selectionne[0], 'values')
        ent_matricule.insert(0, valeurs[0])
        ent_nom.insert(0, valeurs[1])
        ent_filiere.insert(0, valeurs[2])
        ent_note.insert(0, valeurs[3])


def vider_champs():
    ent_matricule.delete(0, tk.END)
    ent_nom.delete(0, tk.END)
    ent_filiere.delete(0, tk.END)
    ent_note.delete(0, tk.END)


fenetre = tk.Tk()
fenetre.title("إدارة نقاط المتدربين")
fenetre.geometry("800x750")
fenetre.configure(bg="#f0f0f0")

connecter_db()

titre = tk.Label(fenetre, text="نظام إدارة نقاط المتدربين", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
titre.pack(pady=10)

frame_form = tk.Frame(fenetre, bg="#f0f0f0")
frame_form.pack(pady=10)

tk.Label(frame_form, text="رقم التسجيل:", bg="#f0f0f0").grid(row=0, column=0)
ent_matricule = tk.Entry(frame_form);
ent_matricule.grid(row=0, column=1)
tk.Label(frame_form, text="الاسم:", bg="#f0f0f0").grid(row=1, column=0)
ent_nom = tk.Entry(frame_form);
ent_nom.grid(row=1, column=1)
tk.Label(frame_form, text="التخصص:", bg="#f0f0f0").grid(row=2, column=0)
ent_filiere = tk.Entry(frame_form);
ent_filiere.grid(row=2, column=1)
tk.Label(frame_form, text="النقطة:", bg="#f0f0f0").grid(row=3, column=0)
ent_note = tk.Entry(frame_form);
ent_note.grid(row=3, column=1)

frame_boutons = tk.Frame(frame_form, bg="#f0f0f0")
frame_boutons.grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(frame_boutons, text="إضافة", command=ajouter_stagiaire).grid(row=0, column=0)
tk.Button(frame_boutons, text="تعديل", command=modifier_stagiaire).grid(row=0, column=1)
tk.Button(frame_boutons, text="حذف", command=supprimer_stagiaire).grid(row=0, column=2)

frame_recherche = tk.Frame(fenetre, bg="#f0f0f0")
frame_recherche.pack(pady=5)
tk.Label(frame_recherche, text="بحث (اسم أو رقم):", bg="#f0f0f0").pack(side=tk.LEFT)
ent_recherche = tk.Entry(frame_recherche, width=30)
ent_recherche.pack(side=tk.LEFT, padx=10)
ent_recherche.bind("<KeyRelease>", rechercher_stagiaire)

frame_tableau = tk.Frame(fenetre)
frame_tableau.pack(pady=10)
tableau = ttk.Treeview(frame_tableau, columns=("mat", "nom", "fil", "note"), show="headings", height=10)
tableau.heading("mat", text="رقم التسجيل");
tableau.column("mat", width=100)
tableau.heading("nom", text="الاسم");
tableau.column("nom", width=150)
tableau.heading("fil", text="التخصص");
tableau.column("fil", width=100)
tableau.heading("note", text="النقطة");
tableau.column("note", width=50)
tableau.pack()

tableau.bind("<ButtonRelease-1>", selectionner_stagiaire)
charger_donnees()
fenetre.mainloop()