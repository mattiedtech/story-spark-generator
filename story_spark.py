import json
import random #used to pick a random prompt
from pathlib import Path

#Constant file paths for prompts and faves
PROMPTS_PATH = Path("prompts.json")
FAVES_PATH = Path("favorites.json")

#open json file
def load_json(path, default):
    if not path.exists():
        return default
    try:
        with path.open("r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[!] Could not read {path.name}. Starting fresh.")
        return default

#save faves to list    
def save_json(path, data):
    with path.open("w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#pick a random item from the prompts list
def pick_prompt(prompts):
    if not prompts:
        return None
    return random.choice(prompts)

#displays menu each loop
#shows current prompt if you've drawn one, or tells you how to start
def print_menu(current):
    print("\n=== Story Spark Generator ===")
    if current:
        print(f"Current spark:\n - {current}")
    else:
        print("No prompt yet. Press N for a new one.")
    print("\nOptions:")
    print("[N] New prompt   [F] Favorite this   [L] List favorites")
    print("[E] Export favorites   [Q] Quit")

#dump faves to .txt, numbered. If none, warns you
def export_favorites(faves):
    if not faves:
        print("No favorites to export yet.")
        return
    out_path = Path("favorites.txt")
    with out_path.open('w') as f:
        for i, p in enumerate(faves, 1):
            f.write(f"{i}.{p}\n")
        print(f"Exported {len(faves)} favorites -> {out_path.resolve()}")

#main driver
def main():
    prompts = load_json(PROMPTS_PATH, [])
    favorites = load_json(FAVES_PATH, [])
    current = None

#infinite loop with menu each time
    while True:
        print_menu(current)
        choice = input("\nEnter choice:").strip().lower()

        #N choice, warning if prompts.json empty
        if choice == "n":
            current = pick_prompt(prompts)
            if current is None:
                print ("Add some prompts to prompts.json first!")

        #F choice: guards agains no prompt yet and already faved
        elif choice == "f":
            if not current:
                print("Nothing to favorite yet—press N first.")
            elif current in favorites:
                print("Already in favorites.")
            else:
                favorites.append(current)
                save_json(FAVES_PATH, favorites)
                print("Added to favorites.")

        # l choice (list all faves)
        elif choice == "l":
            if not favorites:
                print("No favorites yet.")
            else:
                print("\nYour Favorites:")
                for i, p in enumerate(favorites, 1):
                    print(f"{i}. {p}")

        # e choice: export function
        elif choice == "e":
            export_favorites(favorites)

        # q: quit
        elif choice == "q":
            print("Until next time!")
            break

        #catch all invalid input
        else:
            print("Try N, F, L, E, or Q.")

#standard python entry point
if __name__ == "__main__":
    main()