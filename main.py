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

class Klasse:
    schueler:list[Schueler]

    def read_csv_file(self,path:str,seperator=",") ->  None:
        with open(path) as csvfile:
            rows = csvfile.readlines()
            headline = rows[0].split(seperator)
            for i in range(len(rows)):
                name = ""
                noten = {}
                if i == 0:
                    continue
                columns = rows[i].split(seperator)
                for j in range(len(columns)):
                    if j == 0:
                        name = columns[j]
                    else:
                        noten[headline[j]] = columns[j]
                self.schueler.append(Schueler(name,noten))
