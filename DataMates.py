import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
import os

class Gildano:
    def __init__(self, nome, classe, ruolo, data_ingresso, discord, note):
        self.nome = nome
        self.classe = classe
        self.ruolo = ruolo
        self.data_ingresso = data_ingresso
        self.discord = discord
        self.note = note

    def to_dict(self):
        return {
            "nome": self.nome,
            "classe": self.classe,
            "ruolo": self.ruolo,
            "data_ingresso": self.data_ingresso,
            "discord": self.discord,
            "note": self.note
        }

    @staticmethod
    def from_dict(data):
        return Gildano(
            data["nome"],
            data["classe"],
            data["ruolo"],
            data["data_ingresso"],
            data["discord"],
            data.get("note", "")
        )

class GildaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DataMates v0.1.2 By AntoFas87")
        self.gildani = []
        self.file_path = "gildani.json"

        self.tabella = ttk.Treeview(root, columns=("Nome", "Classe", "Ruolo", "Data join", "Discord", "Note"), show="headings")
        for col in ("Nome", "Classe", "Ruolo", "Data join", "Discord", "Note"):
            self.tabella.heading(col, text=col)
            self.tabella.column(col, width=120)
        self.tabella.pack(pady=10, fill="x")

        self.btn_aggiungi = tk.Button(root, text="Aggiungi", command=self.apri_finestra_aggiunta)
        self.btn_aggiungi.pack(pady=5)

        self.carica_dati()

        # Menu contestuale per modifica e elimina
        self.menu_contesto = tk.Menu(root, tearoff=0)
        self.menu_contesto.add_command(label="Modifica", command=self.modifica_gildano_selezionato)
        self.menu_contesto.add_command(label="Elimina", command=self.elimina_gildano_selezionato)

        self.tabella.bind("<Button-3>", self.mostra_menu_contesto)  # tasto destro

    def carica_dati(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                dati = json.load(f)
                for item in dati:
                    gildano = Gildano.from_dict(item)
                    self.gildani.append(gildano)
                    self.tabella.insert("", tk.END, values=(
                        gildano.nome, gildano.classe, gildano.ruolo,
                        gildano.data_ingresso, gildano.discord, gildano.note
                    ))

    def salva_dati(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([g.to_dict() for g in self.gildani], f, indent=4, ensure_ascii=False)

    def apri_finestra_aggiunta(self):
        self.apri_finestra_dati("Aggiungi Gildano", self.aggiungi_gildano, None)

    def apri_finestra_dati(self, titolo, funzione_conferma, gildano_index):
        finestra = tk.Toplevel(self.root)
        finestra.title(titolo)

        labels = ["Nome", "Classe", "Ruolo", "Entrato in gilda dal (gg/mm/aaaa)", "Discord", "Note"]
        entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(finestra, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(finestra, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label_text] = entry

        # Se si sta modificando, precompila i campi
        if gildano_index is not None:
            gildano = self.gildani[gildano_index]
            entries["Nome"].insert(0, gildano.nome)
            entries["Classe"].insert(0, gildano.classe)
            entries["Ruolo"].insert(0, gildano.ruolo)
            entries["Entrato in gilda dal (gg/mm/aaaa)"].insert(0, gildano.data_ingresso)
            entries["Discord"].insert(0, gildano.discord)
            entries["Note"].insert(0, gildano.note)

        btn_text = "Modifica" if gildano_index is not None else "Aggiungi"
        btn_conferma = tk.Button(finestra, text=btn_text, 
                                 command=lambda: funzione_conferma(finestra, entries, gildano_index))
        btn_conferma.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def aggiungi_gildano(self, finestra, entries, _):
        dati = {k: v.get().strip() for k, v in entries.items()}

        if (not dati["Nome"] or not dati["Classe"] or not dati["Ruolo"] 
            or not dati["Entrato in gilda dal (gg/mm/aaaa)"] or not dati["Discord"]):
            messagebox.showerror("Errore", "Gildano non inserito, rivedi i dati.")
            return

        if not re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", dati["Entrato in gilda dal (gg/mm/aaaa)"]):
            messagebox.showerror("Errore", "Data non valida. Usa il formato gg/mm/aaaa.")
            return

        nuovo = Gildano(
            nome=dati["Nome"],
            classe=dati["Classe"],
            ruolo=dati["Ruolo"],
            data_ingresso=dati["Entrato in gilda dal (gg/mm/aaaa)"],
            discord=dati["Discord"],
            note=dati["Note"]
        )

        self.gildani.append(nuovo)
        self.tabella.insert("", tk.END, values=(
            nuovo.nome, nuovo.classe, nuovo.ruolo,
            nuovo.data_ingresso, nuovo.discord, nuovo.note
        ))
        self.salva_dati()
        messagebox.showinfo("Successo", "Gildano inserito correttamente.")
        finestra.destroy()

    def modifica_gildano_selezionato(self):
        selezione = self.tabella.selection()
        if not selezione:
            return
        iid = selezione[0]
        index = self.tabella.index(iid)
        self.apri_finestra_dati("Modifica Gildano", self.modifica_gildano, index)

    def modifica_gildano(self, finestra, entries, index):
        dati = {k: v.get().strip() for k, v in entries.items()}

        if (not dati["Nome"] or not dati["Classe"] or not dati["Ruolo"] 
            or not dati["Entrato in gilda dal (gg/mm/aaaa)"] or not dati["Discord"]):
            messagebox.showerror("Errore", "Gildano non modificato, rivedi i dati.")
            return

        if not re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", dati["Entrato in gilda dal (gg/mm/aaaa)"]):
            messagebox.showerror("Errore", "Data non valida. Usa il formato gg/mm/aaaa.")
            return

        gildano = self.gildani[index]
        gildano.nome = dati["Nome"]
        gildano.classe = dati["Classe"]
        gildano.ruolo = dati["Ruolo"]
        gildano.data_ingresso = dati["Entrato in gilda dal (gg/mm/aaaa)"]
        gildano.discord = dati["Discord"]
        gildano.note = dati["Note"]

        # aggiorna la riga nella tabella
        iid = self.tabella.get_children()[index]
        self.tabella.item(iid, values=(
            gildano.nome, gildano.classe, gildano.ruolo,
            gildano.data_ingresso, gildano.discord, gildano.note
        ))
        self.salva_dati()
        messagebox.showinfo("Successo", "Gildano modificato correttamente.")
        finestra.destroy()

    def elimina_gildano_selezionato(self):
        selezione = self.tabella.selection()
        if not selezione:
            return

        iid = selezione[0]
        index = self.tabella.index(iid)
        valori = self.tabella.item(iid, "values")
        nome = valori[0]

        conferma = tk.Toplevel(self.root)
        conferma.title("Conferma Eliminazione")
        conferma.grab_set()

        label = tk.Label(conferma, text=f"Sicuro di eliminare {nome}?")
        label.pack(padx=20, pady=10)

        def conferma_elimina():
            # Rimuove dalla lista dati e dalla tabella
            del self.gildani[index]
            self.tabella.delete(iid)
            self.salva_dati()
            messagebox.showinfo("Cancellazione", f"{nome} eliminato correttamente.")
            conferma.destroy()

        btn_frame = tk.Frame(conferma)
        btn_frame.pack(pady=10)

        btn_conferma = tk.Button(btn_frame, text="Conferma", command=conferma_elimina)
        btn_conferma.pack(side=tk.LEFT, padx=10)

        btn_annulla = tk.Button(btn_frame, text="Annulla", command=conferma.destroy)
        btn_annulla.pack(side=tk.LEFT, padx=10)

    def mostra_menu_contesto(self, event):
        iid = self.tabella.identify_row(event.y)
        if iid:
            self.tabella.selection_set(iid)
            self.menu_contesto.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = GildaApp(root)
    root.mainloop()
