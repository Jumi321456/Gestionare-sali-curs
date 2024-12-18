import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Lista inițială de săli
sali = {
    "Sala 101": {"status": "Liberă", "max_persoane": 30, "ocupate": 0, "ocupant": None, "ora_ocupare": None, "ora_eliberare": None},
    "Sala 102": {"status": "Liberă", "max_persoane": 25, "ocupate": 0, "ocupant": None, "ora_ocupare": None, "ora_eliberare": None},
}

# Funcție pentru actualizarea listei
def actualizeaza_lista():
    lista_sali.delete(0, tk.END)
    for sala, info in sali.items():
        text = f"{sala}: {info['status']} (Ocupate: {info['ocupate']}/{info['max_persoane']})"
        if info['ocupant']:
            text += f" | Ocupant: {info['ocupant']}"
        if info["ora_ocupare"] and info["ora_eliberare"]:
            text += f" | Ora ocupare: {info['ora_ocupare']} | Ora eliberare: {info['ora_eliberare']}"

        # Verificare expirare timp
        a_expirat = False
        if info["ora_eliberare"] and info['status'] == "Ocupată":
            ora_eliberare = datetime.strptime(info["ora_eliberare"], "%H:%M:%S").time()
            if datetime.now().time() > ora_eliberare:
                a_expirat = True

        lista_sali.insert(tk.END, text)
        if a_expirat:
            lista_sali.itemconfig(tk.END, {'fg': 'red'})

# Funcție pentru ocuparea sălii
def ocupa_sala():
    selectie = lista_sali.curselection()
    if not selectie:
        messagebox.showwarning("Atenție", "Selectează o sală!")
        return

    sala_selectata = lista_sali.get(selectie).split(":")[0]
    info_sala = sali[sala_selectata]

    if info_sala["status"] == "Ocupată":
        messagebox.showerror("Eroare", "Sala este deja ocupată!")
        return

    try:
        nr_persoane = int(input_persoane.get())
        durata = int(input_durata.get())
        nume_ocupant = input_ocupant.get().strip()

        if nr_persoane <= 0 or durata <= 0 or not nume_ocupant:
            raise ValueError("Datele introduse nu sunt valide.")
        if nr_persoane > info_sala['max_persoane']:
            messagebox.showerror("Eroare", f"Capacitatea maximă a sălii este {info_sala['max_persoane']}!")
            return
    except ValueError:
        messagebox.showerror("Eroare", "Introdu date valide pentru ocupare!")
        return

    # Calcul ora ocupare și eliberare
    ora_curenta = datetime.now()
    ora_eliberare = ora_curenta + timedelta(minutes=durata)
    info_sala.update({
        "status": "Ocupată",
        "ocupate": nr_persoane,
        "ocupant": nume_ocupant,
        "ora_ocupare": ora_curenta.strftime("%H:%M:%S"),
        "ora_eliberare": ora_eliberare.strftime("%H:%M:%S"),
    })
    actualizeaza_lista()

# Funcție pentru eliberarea sălii
def elibereaza_sala():
    selectie = lista_sali.curselection()
    if not selectie:
        messagebox.showwarning("Atenție", "Selectează o sală!")
        return

    sala_selectata = lista_sali.get(selectie).split(":")[0]
    sali[sala_selectata].update({
        "status": "Liberă",
        "ocupate": 0,
        "ocupant": None,
        "ora_ocupare": None,
        "ora_eliberare": None,
    })
    actualizeaza_lista()

# Funcție pentru adăugarea unei săli
def adauga_sala():
    nume = input_nume_sala.get().strip()
    capacitate = input_capacitate_sala.get().strip()
    if not nume or not capacitate.isdigit():
        messagebox.showerror("Eroare", "Introdu un nume valid și o capacitate numerică!")
        return

    sali[nume] = {"status": "Liberă", "max_persoane": int(capacitate), "ocupate": 0, "ocupant": None, "ora_ocupare": None, "ora_eliberare": None}
    actualizeaza_lista()

# Funcție pentru ștergerea unei săli
def sterge_sala():
    selectie = lista_sali.curselection()
    if not selectie:
        messagebox.showwarning("Atenție", "Selectează o sală pentru ștergere!")
        return
    sala_selectata = lista_sali.get(selectie).split(":")[0]
    del sali[sala_selectata]
    actualizeaza_lista()

# Interfață
root = tk.Tk()
root.title("Gestionare Săli")
root.geometry("900x700")
root.configure(bg="#e6f7ff")  # Fundal albastru deschis

# Titlu principal
tk.Label(root, text="Gestionare Săli de Clasă", font=("Arial", 24, "bold"), bg="#e6f7ff", fg="#333").pack(pady=20)

# Listă săli
lista_sali = tk.Listbox(root, width=100, height=15, font=("Arial", 12))
lista_sali.pack(pady=10)
actualizeaza_lista()

# Inputuri pentru ocupare
frame_ocupare = tk.Frame(root, bg="#e6f7ff")
frame_ocupare.pack(pady=10)

tk.Label(frame_ocupare, text="Număr persoane:", font=("Arial", 12), bg="#e6f7ff").grid(row=0, column=0, padx=10)
input_persoane = tk.Entry(frame_ocupare, width=10)
input_persoane.grid(row=0, column=1, padx=10)

tk.Label(frame_ocupare, text="Nume ocupant:", font=("Arial", 12), bg="#e6f7ff").grid(row=0, column=2, padx=10)
input_ocupant = tk.Entry(frame_ocupare, width=15)
input_ocupant.grid(row=0, column=3, padx=10)

tk.Label(frame_ocupare, text="Durată (minute):", font=("Arial", 12), bg="#e6f7ff").grid(row=0, column=4, padx=10)
input_durata = tk.Entry(frame_ocupare, width=10)
input_durata.grid(row=0, column=5, padx=10)

# Butoane pentru ocupare și eliberare
frame_butoane = tk.Frame(root, bg="#e6f7ff")
frame_butoane.pack(pady=10)

tk.Button(frame_butoane, text="Ocupa Sala", bg="#4caf50", fg="white", font=("Arial", 12), command=ocupa_sala).grid(row=0, column=0, padx=20)
tk.Button(frame_butoane, text="Eliberează Sala", bg="#f44336", fg="white", font=("Arial", 12), command=elibereaza_sala).grid(row=0, column=1, padx=20)

# Inputuri pentru gestionarea sălilor
frame_gestionare = tk.Frame(root, bg="#e6f7ff")
frame_gestionare.pack(pady=20)

tk.Label(frame_gestionare, text="Nume sală nouă:", font=("Arial", 12), bg="#e6f7ff").grid(row=0, column=0, padx=10)
input_nume_sala = tk.Entry(frame_gestionare, width=20)
input_nume_sala.grid(row=0, column=1, padx=10)

tk.Label(frame_gestionare, text="Capacitate sală:", font=("Arial", 12), bg="#e6f7ff").grid(row=0, column=2, padx=10)
input_capacitate_sala = tk.Entry(frame_gestionare, width=10)
input_capacitate_sala.grid(row=0, column=3, padx=10)

tk.Button(frame_gestionare, text="Adaugă Sală", bg="#2196f3", fg="white", font=("Arial", 12), command=adauga_sala).grid(row=0, column=4, padx=10)
tk.Button(frame_gestionare, text="Șterge Sală", bg="#f44336", fg="white", font=("Arial", 12), command=sterge_sala).grid(row=0, column=5, padx=10)

root.mainloop()
