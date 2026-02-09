import datetime
import json as js

class Artist:
    def __init__(self, first_name: str, family_name: str, artworks: list, birth_year: int, death_year = None):
        self.first_name: str = first_name
        self.family_name: str = family_name
        self.artworks: list = artworks
        self.birth_year: int = birth_year
        self.death_year = death_year
def calculate_age(self) -> int:
        if self.death_year is None:
            current_year: int = datetime.datetime.now().year
            return current_year - self.birth_year
        elif self.death_year > self.birth_year:
            return self.death_year - self.birth_year
        else:
            raise ValueError("Unable to calculate age.")

def add_artist():
    artist = Artist(first_name="", family_name="", artworks=[], birth_year=0, death_year=None)
    
    artist.first_name = input("First Name: ")
    artist.family_name = input("Family Name: ")
    artist.birth_year = int(input("Birth Year: "))
    death_year_input = input("Death Year (leave blank if still alive): ")
    if death_year_input:
        artist.death_year = int(death_year_input)
    else:
        artist.death_year = None
    artworks_input = input("Artworks (comma separated): ")
    artist.artworks = [artwork.strip() for artwork in artworks_input.split(",")]
    print(f"Artist {artist.first_name} {artist.family_name} added successfully.")
    dump_info(artist)

def dump_info(artist):
    try:
        try:
            with open("artist_info.json", "r") as f:
                data = js.load(f)
                if not isinstance(data, list):
                    # Convert old format (single artist) to list format
                    data = [data]
        except FileNotFoundError:
            data = []
        
        data.append(artist.__dict__)
        
        # Write updated list back to file
        with open("artist_info.json", "w") as f:
            js.dump(data, f, indent=4)
        print(f"Artist information saved to artist_info.json")
        print("\nReturning to main menu.\n")
        return main()
    except Exception as e:
        print(f"Error saving artist information: {e}")
        
def display_info(artist):
    info = (
        f"Artist: {artist.first_name} {artist.family_name}\n"
        f"Birth Year: {artist.birth_year}\n"
        f"Death Year: {artist.death_year if artist.death_year else 'N/A'}\n"
        f"Age: {artist.age}\n"
        f"Artworks: {', '.join(artist.artworks) if artist.artworks else 'None'}"
    )
    print(info)

def main():
    artists = []
    try:
        with open("artist_info.json", "r") as f:
            data = js.load(f)
            if isinstance(data, list):
                artists = [Artist(**artist_data) for artist_data in data]
            else:
                artists = [Artist(**data)]
            print("\nMain menu: \nLoaded information from file.\n")
    except FileNotFoundError:
        artists = []
    main_menu = input("Choose an action - (a)dd artist, (d)isplay info: (a/d)\n Or any other key to exit the program.").strip().lower()
    if main_menu == "a":
        artist = add_artist()
    elif main_menu == "d":
        if artists:
            for i, artist in enumerate(artists, 1):
                print(f"\n----| Artist {i} |----")
                display_info(artist)
        else:
            print("No artist information available. Please add an artist first.")
        return main()
    else:
        print("Exiting program.")
        
if __name__ == "__main__":
    main()