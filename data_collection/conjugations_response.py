from pydantic import BaseModel

class ConjugationsResponse(BaseModel):
    KodHatayot: int
    Shoresh: str
    ShoreshWithShinType: str
    Hehara: str
    Mashmaut: str
    class BinyanModel(BaseModel):
        BinyanKod: int
        BinyanName: str
    Binyan: BinyanModel
    class ZmanimModel(BaseModel):
        KodZman: int
        class InnerZmanimModel(BaseModel):
            Zman: str
            class GufimModel(BaseModel):
                GufHebrew: str
                class HatayaMenukkadModel(BaseModel):
                    Text: str
                    HaeimMutham: bool
                HatayaMenukkad: list[list[HatayaMenukkadModel]]
                class HatayaKtivMaleModel(BaseModel):
                    Text: str
                    HaeimMutham: bool
                HatayaKtivMale: list[list[HatayaKtivMaleModel]]

                def get_hataya_menukkad(self):
                    return [''.join(x.Text for x in i) for i in self.HatayaMenukkad]
            Gufim: list[GufimModel]
        Zmanim: list[InnerZmanimModel]
    Zmanim: list[ZmanimModel]

    def get_entries(self):
        entries = []
        root = self.ShoreshWithShinType.strip()
        stem = self.Binyan.BinyanName.strip()
        for z1 in self.Zmanim:
            for z2 in z1.Zmanim:
                tense = z2.Zman.strip()
                for g in z2.Gufim:
                    for pronoun in g.GufHebrew.split('/'):
                        for conjugation in g.get_hataya_menukkad():
                            entries.append((root, stem, tense, pronoun.strip(), conjugation.strip()))
        return entries