
import pythonbible as Bible
import random

def get_random_verse():
    # List of all Bible books (canonical order)
    books = list(Bible.Book)
    
    # Randomly select a book
    random_book = random.choice(books)
    
    # Get the number of chapters in the selected book
    num_chapters = Bible.get_number_of_chapters(random_book)
    
    # Randomly select a chapter
    random_chapter = random.randint(1, num_chapters)
    
    # Get the number of verses in the selected chapter
    num_verses = Bible.get_number_of_verses(random_book, random_chapter)
    
    # Randomly select a verse
    random_verse = random.randint(1, num_verses)
    
    # Create a ScriptureReference object
    reference = Bible.get_verse_id(random_book, random_chapter, random_verse)
    
    # Get the verse ID for the selected book, chapter, and verse
    # verse_id = Bible.convert_reference_to_verse_ids([reference])
    
    # Get the verse text using the verse ID
    verse_text = Bible.get_verse_text(reference)
    
    # Format the verse reference
    normanlized_reference = Bible.convert_verse_ids_to_references([reference])

    # Get verse text
    verse = Bible.format_scripture_references(normanlized_reference)
    
    return verse_text, verse

def print_verse():
    reference, verse = get_random_verse()
    print(f"{reference}: {verse}")


def main():
    reference, verse = get_random_verse()
    print(f"{reference}: {verse}")

if __name__ == "__main__":
    main()

print_verse()


