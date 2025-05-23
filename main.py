import tkinter as tk
import tkinter.filedialog as filedialog
from decimal import *

class Schueler:
    def __init__(self,name:str,noten:dict) -> None:
        self.name = name
        self.noten = noten

        allgemeinbildende_faecher = []
        lernfelder = []
        for key in noten:
            if noten[key] == "":
                continue
            if "LF" in key:
                lernfelder.append(Decimal(noten[key]))
            else:
                allgemeinbildende_faecher.append(Decimal(noten[key]))

        dn1 = self.__calc_durchschnittsnote(*allgemeinbildende_faecher)
        dn2 = self.__calc_durchschnittsnote(*lernfelder)

        self.durchschnitt_allgemeinbildende_faecher = dn1
        self.durchschnitt_lernfelder = dn2
        self.gesamtnote = self.__calc_gesamtnote(dn1,dn2)

    def __getitem__(self,key:str):
        if key == "DN1":
            return self.durchschnitt_allgemeinbildende_faecher
        elif key == "DN2":
            return self.durchschnitt_lernfelder
        elif key == "GN":
            return self.gesamtnote
        elif key in self.noten:
            return self.noten[key]
        elif key == "Name":
            return self.name
        raise Exception(f"Es existiert keine Note für {key}")

    def __calc_durchschnittsnote(self,*note):
        """
        Die durchschnittsnote wird auf eine Stelle nach dem Komma kaufmännisch gerundet.

        durchschnitt =  sum(note) / len(note)
        durchschnitt = int(abs(durchschnitt) * 100)
        letzte_ziffer = durchschnitt % 10
        durchschnitt = (durchschnitt // 10) + (1 if letzte_ziffer >= 5 else 0)
        return durchschnitt / 10
        """
        result = (Decimal(sum(note)) / Decimal(len(note))).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
        return result

    def __calc_gesamtnote(self,dn1,dn2):
        """
        # Berechnung

        (dn1 + dn2 + dn2) / 3

        :param dn1: durchschnitsnote der allgemeinbildenden Fächer
        :param dn2: durchschnitsnote der Lernfelder

        allgemeinbildender Unterricht:
        * Deutsch
        * Religion/Ethik
        * Sozialkunde
        * Sport
        * Wirtschaftslehre
        """
        result = ((dn1 + Decimal(2) * dn2) / Decimal(3)).quantize(Decimal("0.1"),rounding=ROUND_DOWN)
        return result

class Klasse:
    schueler:list[Schueler] = []

    def read_csv_file(self,path:str,separator=",") ->  None:
        with open(path) as csvfile:
            rows = csvfile.readlines()
            headline = rows[0].replace("\n","").split(separator)
            for i in range(len(rows)):
                name = ""
                noten = {}
                row = rows[i].replace("\n","")
                if i == 0:
                    continue
                columns = row.split(separator)
                for j in range(len(columns)):
                    if j == 0:
                        name = columns[j]
                    else:
                        noten[headline[j]] = Decimal(columns[j]) if columns[j] != "" else ""
                self.schueler.append(Schueler(name,noten))

    def write_csv_file(self,path:str,separator=",") -> None:
        if len(self.schueler) == 0:
            raise Exception("Keine Schüler gefunden.")
        headline = ["Name"]
        result = ""
        for key in self.schueler[0].noten:
            headline.append(key)
        headline.extend(["DN1","DN2","GN"])
        for schueler in self.schueler:
            noten = []
            for key in headline:
                noten.append(str(schueler[key]))
            result += ",".join(noten)+"\n"
        result = ",".join(headline) +"\n" +result
        with open(path,"w") as csvFile:
            csvFile.write(result)
            csvFile.close()

    def __getitem__(self,name:str) -> Schueler :
        result = next((obj for obj in self.schueler if obj.name == name), None)
        if result == None:
            raise Exception("Kein Schueler mit dem Name gefunden")
        return result



klasse = Klasse()
root = tk.Tk()

root.minsize(420,320)

def open_file():
    path = filedialog.askopenfilename()
    if path:
        klasse.read_csv_file(path)

def write_file():
    path = filedialog.asksaveasfilename()
    if path:
        klasse.write_csv_file(path)

file_input_button = tk.Button(
    root,
    text="datei öffnen",
    command=open_file,
)
file_output_button = tk.Button(
    root,
    text="datei speichern",
    command=write_file,
)

file_input_button.pack(side="top")
file_output_button.pack(side="top")


root.mainloop()
