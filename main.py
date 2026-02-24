from fastapi import FastAPI, Depends, Form , Query
from sqlalchemy.orm import Session
from .model import  BookResponse
from .database import Base , engine , SessionLocal , BookDB
from .cache import SampleCaching

caching = SampleCaching()

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()

@app.post("/books/", response_model=BookResponse)
def create_book(  name: str = Form(min_length=3, max_length=100  ),
                  author: str = Form(...),
                  year: int = Form(...),
                  db: Session = Depends(get_db)):
    

      db_book = BookDB(name=name, author = author, year = year)
      db.add(db_book)
      db.commit()
      db.refresh(db_book)
      if caching.get(name) is None:
            caching.delete(name)

      return db_book

@app.get("/books/")
def search_books(
      db: Session = Depends(get_db),
      q: str = Query(..., min_length=3, max_length=100),
      page: int = Query(1, ge=1),
      size: int = Query(10, ge=1, le=50)
):

      if caching.get(q) is not None:
            return caching.get(q)


      base = db.query(BookDB).filter(BookDB.name.like(f"%{q}%"))
      total = base.count()
      start = (page - 1) * size
      results = base.order_by(BookDB.id).offset(start).limit(size).all()
      caching.set(q,results)
      return {
            "total": total,
            "page": page,
            "results": results
      }     


@app.get("/authors/search/")
def search_authors(
      db: Session = Depends(get_db),
      author: str = Query(..., min_length=1, max_length=100),
):
      count = db.query(BookDB).filter(BookDB.author == author).count()
      return {
            "results": {"author": author, "count": count}
      }