from tkinter import *
from PIL import ImageTk, Image
import phonenumbers

from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone

from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz



# configurações da janela
app = Tk()
app.geometry("400x600")
app.resizable(False,False)
app.title("Rastreio de Telefone")

def rastreio(): 
    try:
        numero = entry.get().strip()

        telefone = phonenumbers.parse(numero)

        if not phonenumbers.is_valid_number(telefone):
            pais.config(text="País: Número inválido")
            cidade.config(text="Região: -")
            operadora.config(text="Operadora: -")
            horas.config(text="Horário: -")
            return

        # País real
        nome_pais = geocoder.country_name_for_number(telefone, "pt")

        # Região aproximada do prefixo
        regiao = geocoder.description_for_number(telefone, "pt")

        pais.config(text=f"País: {nome_pais}")
        cidade.config(text=f"Região: {regiao}")

        # Operadora (pode vir vazia)
        sim = carrier.name_for_number(telefone, "pt")
        sim = sim if sim else "Não disponível"
        operadora.config(text=f"Operadora: {sim}")

        # Horário local aproximado
        fusos = timezone.time_zones_for_number(telefone)
        if fusos:
            tz = pytz.timezone(fusos[0])
            hora_local = datetime.now(tz).strftime("%H:%M:%S")
        else:
            hora_local = "Desconhecido"

        horas.config(text=f"Horário: {hora_local}")

    except Exception as e:
        pais.config(text="País: Erro ao processar")
        cidade.config(text="Região: -")
        operadora.config(text="Operadora: -")
        horas.config(text="Horário: -")
        print("Erro:", e)
    

# adicionando ícone
icon = Image.open("smartphone.png")
photo = ImageTk.PhotoImage(icon)
app.wm_iconphoto(False, photo)  

# logo do sistema
logo = PhotoImage(file='smartphone_logo.png')
Label(app, image=logo).place(x=-50, y=35)

titulo = Label(app, text="Rastreio de Telefone", font="verdana 15 bold", fg="black", bg="white")
titulo.place(x=90, y=80)

# entrada de telefone
entry = StringVar()
entrada_numero = Entry(app, textvariable=entry, width=14, font="verdana 15", fg="black", bg="white", justify="center")
entrada_numero.place(x=180, y=260)

# botão de rastreio
rastrear = PhotoImage(file='push.png')
botao_rastreio = Button(app, image=rastrear, width=50, height=50, bg="gray", activebackground="green", cursor="hand2", bd=2, command=rastreio)
botao_rastreio.place(x=180, y=490)

# resultados da pesquisa
pais = Label(app, text="País: ", font="verdana 8", fg="black", bg="white")
pais.place(x=90, y=390)

cidade = Label(app, text="Cidade: ", font="verdana 8", fg="black", bg="white")
cidade.place(x=90, y=410)

operadora= Label(app, text="Operadora: ", font="verdana 8", fg="black", bg="white")
operadora.place(x=90, y=430)

horas = Label(app, text="Horário: ", font="verdana 8", fg="black", bg="white")
horas.place(x=90, y=450)





app.mainloop()