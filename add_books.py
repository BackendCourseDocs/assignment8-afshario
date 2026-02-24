"""
اسکریپت درج ۹۰۰۰ کتاب با نام انگلیسی در دیتابیس MySQL
"""
from database import engine, SessionLocal, Base, BookDB

# لیست نویسندگان انگلیسی (۹۰ نفر — در خروجی ۹۰۰۰ تایی ترکیب با عناوین)
AUTHORS_EN = [
    "Jane Austen", "George Orwell", "Harper Lee", "F. Scott Fitzgerald",
    "Gabriel Garcia Marquez", "J.D. Salinger", "J.R.R. Tolkien", "Aldous Huxley",
    "Charlotte Bronte", "Emily Bronte", "Antoine de Saint-Exupery", "Paulo Coelho",
    "J.K. Rowling", "Dan Brown", "C.S. Lewis", "Khaled Hosseini", "Yann Martel",
    "Markus Zusak", "Margaret Mitchell", "Leo Tolstoy", "Fyodor Dostoevsky",
    "Miguel de Cervantes", "Alexandre Dumas", "Victor Hugo", "Albert Camus",
    "Franz Kafka", "Ernest Hemingway", "John Steinbeck", "Charles Dickens",
    "Herman Melville", "Mark Twain", "Gustave Flaubert", "Oscar Wilde",
    "Bram Stoker", "Mary Shelley", "Daniel Defoe", "Jonathan Swift",
    "Robert Louis Stevenson", "H.G. Wells", "Joseph Conrad", "James Joyce",
    "Virginia Woolf", "William Faulkner", "Toni Morrison", "Alice Walker",
    "Joseph Heller", "Kurt Vonnegut", "Margaret Atwood", "Frank Herbert",
    "Douglas Adams", "Ray Bradbury", "Sylvia Plath", "Vladimir Nabokov",
    "Boris Pasternak", "Umberto Eco", "Italo Calvino", "Milan Kundera",
    "Haruki Murakami", "Hermann Hesse", "Thomas Mann", "Gunter Grass",
    "Carlos Ruiz Zafon", "Isabel Allende", "Mario Vargas Llosa", "Roberto Bolano",
    "Samuel Beckett", "Jean-Paul Sartre", "Mikhail Bulgakov", "John Grisham",
    "Stephen King", "Agatha Christie", "Arthur Conan Doyle", "Isaac Asimov",
    "Philip K. Dick", "Ursula K. Le Guin", "Neil Gaiman", "Terry Pratchett",
    "Zadie Smith", "Ian McEwan", "Kazuo Ishiguro", "Salman Rushdie",
    "John Updike", "Philip Roth", "Don DeLillo", "Cormac McCarthy",
    "Michael Chabon", "Jonathan Franzen", "Donna Tartt", "Gillian Flynn",
]

# عناوین کتاب انگلیسی (برای ترکیب با نویسندگان — حداقل ۹۰ تا)
TITLES_EN = [
    "Pride and Prejudice", "1984", "To Kill a Mockingbird", "The Great Gatsby",
    "One Hundred Years of Solitude", "The Catcher in the Rye", "The Lord of the Rings",
    "Animal Farm", "Brave New World", "The Hobbit", "Jane Eyre", "Wuthering Heights",
    "The Little Prince", "The Alchemist", "Harry Potter and the Philosopher's Stone",
    "The Da Vinci Code", "The Chronicles of Narnia", "The Kite Runner", "Life of Pi",
    "The Book Thief", "Gone with the Wind", "War and Peace", "Anna Karenina",
    "Crime and Punishment", "The Brothers Karamazov", "Don Quixote",
    "The Count of Monte Cristo", "Les Miserables", "The Stranger", "The Plague",
    "The Trial", "The Metamorphosis", "The Old Man and the Sea", "For Whom the Bell Tolls",
    "The Sun Also Rises", "A Farewell to Arms", "The Grapes of Wrath", "Of Mice and Men",
    "East of Eden", "Great Expectations", "Oliver Twist", "A Tale of Two Cities",
    "David Copperfield", "Moby Dick", "The Adventures of Tom Sawyer", "Adventures of Huckleberry Finn",
    "Madame Bovary", "The Picture of Dorian Gray", "Dracula", "Frankenstein",
    "Robinson Crusoe", "Gulliver's Travels", "Treasure Island", "The Time Machine",
    "The Invisible Man", "The War of the Worlds", "Heart of Darkness", "Lord Jim",
    "Ulysses", "A Portrait of the Artist as a Young Man", "Dubliners", "Mrs Dalloway",
    "To the Lighthouse", "Orlando", "The Sound and the Fury", "As I Lay Dying",
    "Light in August", "Beloved", "The Color Purple", "Catch-22", "Slaughterhouse-Five",
    "The Handmaid's Tale", "Dune", "The Hitchhiker's Guide to the Galaxy", "Fahrenheit 451",
    "The Bell Jar", "Lolita", "Doctor Zhivago", "The Name of the Rose",
    "If on a winter's night a traveler", "Invisible Cities", "The Unbearable Lightness of Being",
    "Norwegian Wood", "Kafka on the Shore", "1Q84", "Siddhartha", "Steppenwolf",
    "Demian", "The Magic Mountain", "Death in Venice", "Buddenbrooks", "The Tin Drum",
    "The Shadow of the Wind", "Love in the Time of Cholera", "Chronicle of a Death Foretold",
    "The House of the Spirits", "Conversation in the Cathedral", "The Savage Detectives",
    "Waiting for Godot", "Nausea", "The Fall", "The Myth of Sisyphus", "The Castle",
    "America", "The Master and Margarita", "The Firm", "The Shining", "Murder on the Orient Express",
    "The Hound of the Baskervilles", "Foundation", "Do Androids Dream of Electric Sheep", "The Left Hand of Darkness",
    "American Gods", "Good Omens", "White Teeth", "Atonement", "The Remains of the Day",
]


def build_books_9000():
    """ساخت ۹۰۰۰ رکورد (نام کتاب، نویسنده، سال) با ترکیب نویسندگان و عناوین."""
    books = []
    n_authors = len(AUTHORS_EN)
    n_titles = len(TITLES_EN)
    for i in range(9000):
        author = AUTHORS_EN[i % n_authors]
        title = TITLES_EN[i % n_titles]
        year = 1800 + (i % 224)  # سال بین ۱۸۰۰ تا ۲۰۲۴
        books.append((title, author, year))
    return books


BOOKS_EN = build_books_9000()


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(BookDB).count()
        if existing >= 9000:
            print(f"قبلاً {existing} کتاب در دیتابیس وجود دارد. درج متوقف شد.")
            return
        added = 0
        batch_size = 1000
        for i, (name, author, year) in enumerate(BOOKS_EN):
            book = BookDB(name=name, author=author, year=year)
            db.add(book)
            added += 1
            if (i + 1) % batch_size == 0:
                db.commit()
                print(f"  {added} کتاب ذخیره شد...")
        db.commit()
        print(f"{added} کتاب انگلیسی با موفقیت در دیتابیس ذخیره شد.")
    except Exception as e:
        db.rollback()
        print(f"خطا: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
