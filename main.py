import csv

class Schueler:
    def __init__(self,name:str,noten:dict) -> None:
        self.name = name
        self.noten = noten

        allgemeinbildende_faecher = []
        lernfelder = []
        for key in noten:
            if "LF" in key:
                lernfelder.append(noten[key])
            else:
                allgemeinbildende_faecher.append(noten[key])

        dn1 = self.calc_durchschnittsnote(*allgemeinbildende_faecher)
        dn2 = self.calc_durchschnittsnote(*lernfelder)

        self.durchschnitt_allgemeinbildende_faecher = dn1
        self.durchschnitt_lernfelder = dn2
        self.gesamtnote = self.calc_gesamtnote(dn1,dn2)

    def __getitem__(self,key:str) -> float|int:
        if key in self.noten:
            return self.noten[key]
        raise Exception("Es existiert keine Note für den gewählten Fach")

    def calc_durchschnittsnote(self,*note:int) -> float:
        """
        Die durchschnittsnote wird auf eine Stelle nach dem Komma kaufmännisch gerundet.
        """
        durchschnitt =  sum(note) / len(note)
        durchschnitt = int(abs(durchschnitt) * 100)
        letzte_ziffer = durchschnitt % 10
        durchschnitt = (durchschnitt // 10) + (1 if letzte_ziffer >= 5 else 0)
        return durchschnitt / 10

    def calc_gesamtnote(self,dn1:float|int,dn2:float|int) -> float:
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
        return (float(dn1) + 2 * float(dn2)) / 3

class CsvManager:
    def getStudentsFromCsv(path):
        with open(path, 'w', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            a = []
            for row in spamreader:
                print(', '.join(row))
                a.append(Schueler("ralf", {"de": 1, "en": 4}))
                        
        return a
