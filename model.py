from pydantic import BaseModel

class BookCreate(BaseModel):
    name: str
    author: str
    year: int = None

class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    year: int = None