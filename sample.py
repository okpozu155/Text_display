import pythonbible as pb
import random

def get_random_verse():
    # Get all verse IDs
    all_verse_ids = pb.get_verse_id()
    
    # Randomly select a verse ID
    random_verse_id = random.choice(all_verse_ids)
    
    # Get the verse text
    verse_text = pb.get_verse_text(random_verse_id)
    
    # Get the verse reference
    reference = pb.get_references(random_verse_id)[0]
    
    # Format the verse reference
    reference_text = pb.format_scripture_references([reference])
    
    return reference_text, verse_text

def main():
    reference, verse = get_random_verse()
    print(f"{reference}: {verse}")

if __name__ == "__main__":
    main()


pb.get_references("for god so loved the world that")