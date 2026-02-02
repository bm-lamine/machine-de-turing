import os


class TuringMachine:
    def __init__(
        self,
        states,
        tape_symbols,
        blank_symbol,
        initial_state,
        final_states,
        transitions,
    ):
        """
        Initialise la machine de Turing.

        :param states: Liste des états (list[str])
        :param tape_symbols: Symboles autorisés sur le ruban (list[str])
        :param blank_symbol: Symbole vide '_' (str)
        :param initial_state: État initial (str)
        :param final_states: États finaux (list[str])
        :param transitions: Dictionnaire des règles de transition
                            Format : {(état, symbole): (nouvel_état, symbole_écrit, direction)}
        """
        self.states = states
        self.tape_symbols = tape_symbols
        self.blank = blank_symbol
        self.current_state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.tape = []
        self.head_position = 0

    def initialize_tape(self, input_string):
        """
        Initialise le ruban avec la chaîne d'entrée.

        :param input_string: Chaîne de symboles à placer sur le ruban
        """
        # Convertit la chaîne en liste de symboles
        self.tape = list(input_string)
        # Ajoute un symbole vide à la fin pour simuler l'infini
        self.tape.append(self.blank)
        self.head_position = 0

    def step(self):
        """
        Exécute une étape de la machine.
        Retourne True si la machine doit continuer, False si elle s'arrête.
        """
        # Si dans un état final, on s'arrête
        if self.current_state in self.final_states:
            return False

        # Lit le symbole sous la tête
        if self.head_position >= len(self.tape):
            # Si hors du ruban actuel, considère le symbole vide
            current_symbol = self.blank
        else:
            current_symbol = self.tape[self.head_position]

        # Cherche la transition correspondante
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            # Pas de transition = rejet (arrêt)
            return False

        # Applique la transition
        new_state, write_symbol, direction = self.transitions[key]

        # Écrit le nouveau symbole
        if self.head_position >= len(self.tape):
            self.tape.append(write_symbol)
        else:
            self.tape[self.head_position] = write_symbol

        # Met à jour l'état
        self.current_state = new_state

        # Déplace la tête
        if direction == "R":
            self.head_position += 1
        elif direction == "L":
            self.head_position -= 1

        # Si on va à gauche du début, étend le ruban
        if self.head_position < 0:
            self.tape.insert(0, self.blank)
            self.head_position = 0

        # Si on va à droite de la fin, étend le ruban
        if self.head_position >= len(self.tape):
            self.tape.append(self.blank)

        return True

    def run(self, input_string, verbose=True):
        """
        Exécute la machine sur une entrée donnée.

        :param input_string: Chaîne d'entrée
        :param verbose: Afficher les étapes si True
        :return: True si accepté, False si rejeté
        """
        # Initialise le ruban
        self.initialize_tape(input_string)
        step_count = 0

        if verbose:
            print(f"Entrée: {input_string}")
            print(f"État initial: {self.current_state}")
            self.print_tape()

        # Exécute les étapes
        while self.step():
            step_count += 1
            if verbose:
                print(f"\nÉtape {step_count}:")
                print(f"État: {self.current_state}")
                self.print_tape()

        # Vérifie le résultat
        accepted = self.current_state in self.final_states

        if verbose:
            print("\n" + "=" * 50)
            print(f"Machine {'accepte' if accepted else 'rejette'} l'entrée.")
            print(f"État final: {self.current_state}")
            print(f"Nombre d'étapes: {step_count}")

        return accepted

    def print_tape(self):
        """Affiche le ruban avec la position de la tête."""
        tape_str = "".join(self.tape)
        head_indicator = " " * self.head_position + "^"
        print(f"Ruban: {tape_str}")
        print(f"Tête : {head_indicator}")


def create_machine_from_input():
    """
    Permet à l'utilisateur de créer une machine via des entrées console.
    """
    print("\nCréation d'une machine de Turing personnalisée:")

    # Saisie des états
    states = input("Entrez les états (séparés par des virgules): ").split(",")
    states = [s.strip() for s in states]

    # Saisie des symboles
    tape_symbols = input(
        "Entrez les symboles du ruban (séparés par des virgules): "
    ).split(",")
    tape_symbols = [s.strip() for s in tape_symbols]

    # Symbole vide
    blank = input("Entrez le symbole vide (par défaut '_'): ").strip()
    if not blank:
        blank = "_"

    # État initial
    initial_state = input("Entrez l'état initial: ").strip()

    # États finaux
    final_states = input("Entrez les états finaux (séparés par des virgules): ").split(
        ","
    )
    final_states = [s.strip() for s in final_states]

    # Transitions
    transitions = {}
    print("\nEntrez les transitions (format: état,symbole→état,symbole,direction)")
    print("Exemple: q0,0→q1,1,R")
    print("Tapez 'fin' pour terminer")

    while True:
        rule = input("Transition: ").strip()
        if rule.lower() == "fin":
            break

        try:
            # Parse la règle
            left, right = rule.split("→")
            state, symbol = left.split(",")
            new_state, write_symbol, direction = right.split(",")

            # Ajoute à la table de transition
            transitions[(state.strip(), symbol.strip())] = (
                new_state.strip(),
                write_symbol.strip(),
                direction.strip().upper(),
            )
        except ValueError:
            print("Format incorrect! Utilisez: état,symbole→état,symbole,direction")

    # Crée la machine
    return TuringMachine(
        states, tape_symbols, blank, initial_state, final_states, transitions
    )


def load_machine_from_file(file_path):
    transitions = {}
    states = []
    tape_symbols = []
    blank = "_"
    initial_state = ""
    final_states = []
    reading_transitions = False

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # ignore empty lines or comments

            if line.startswith("states:"):
                states = [s.strip() for s in line.split(":")[1].split(",")]
            elif line.startswith("tape symbols:"):
                tape_symbols = [s.strip() for s in line.split(":")[1].split(",")]
            elif line.startswith("blank symbol:"):
                blank = line.split(":")[1].strip()
            elif line.startswith("initial state:"):
                initial_state = line.split(":")[1].strip()
            elif line.startswith("final state:") or line.startswith("final states:"):
                final_states = [s.strip() for s in line.split(":")[1].split(",")]
            elif line.startswith("transition rules:"):
                reading_transitions = True
            elif reading_transitions:
                if line.startswith("]"):
                    reading_transitions = False
                    continue
                if "→" in line:
                    left, right = line.split("→")
                    state, symbol = left.split(",")
                    new_state, write_symbol, direction = right.split(",")
                    transitions[(state.strip(), symbol.strip())] = (
                        new_state.strip(),
                        write_symbol.strip(),
                        direction.strip().upper(),
                    )

    return TuringMachine(
        states, tape_symbols, blank, initial_state, final_states, transitions
    )


def main():
    """
    Affiche un menu pour créer ou charger une machine de Turing.
    """
    while True:
        print("\n=== Turing Machine CLI ===")
        print("1. Créer une machine personnalisée")
        print("2. Charger une machine depuis un fichier")
        print("3. Quitter")

        choice = input("Choix: ").strip()

        if choice == "1":
            tm = create_machine_from_input()
        elif choice == "2":
            # Lister les fichiers dans tests
            test_dir = "tests"
            files = [f for f in os.listdir(test_dir) if f.endswith(".txt")]
            if not files:
                print("Aucun fichier de test trouvé dans le dossier 'tests'.")
                continue

            print("\nFichiers disponibles:")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")

            file_choice = input("Choisissez un fichier: ").strip()
            try:
                idx = int(file_choice) - 1
                if idx < 0 or idx >= len(files):
                    print("Choix invalide.")
                    continue
                file_path = os.path.join(test_dir, files[idx])
                tm = load_machine_from_file(file_path)
            except ValueError:
                print("Choix invalide.")
                continue
        elif choice == "3":
            print("Au revoir!")
            break
        else:
            print("Option invalide.")
            continue

        # Demander l'entrée pour exécuter la machine
        input_str = input("Entrez la chaîne d'entrée: ")
        tm.run(input_str, verbose=True)


if __name__ == "__main__":
    main()
