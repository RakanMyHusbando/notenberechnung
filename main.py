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

        self.dn1 = self.calc_durchschnittsnote(*allgemeinbildende_faecher)
        self.dn2 = self.calc_durchschnittsnote(*lernfelder)

        self.gesamtnote = self.calc_gesamtnote(self.dn1,self.dn2)

    def __getitem__(self,key:str) -> float|int:
        if key in self.noten:
            return self.noten[key]
        elif key == "durchschnitt_allgemeinbildende_faecher":
            return self.dn1
        elif key == "durchschnitt_lernfelder":
            return self.dn2
        raise Exception("Es existiert keine Note für den gewählten key")

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
        return dn1 + dn2 + dn2 / 3
