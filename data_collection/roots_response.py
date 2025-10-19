from pydantic import BaseModel

class RootsResponse(BaseModel):
    Shoresh: str
    Binyanim: list[str]
    Info: str

    def as_entries(self):
        return [(self.Shoresh, binyan) for binyan in self.Binyanim]