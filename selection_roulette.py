import random


def selection_roulette(population, fitness_values):
    """
    Selection par loterie (Roulette Wheel Selection).

    population : liste des chromosomes
    fitness_values : liste des fitness correspondantes

    Retourne un chromosome choisi selon sa probabilite de selection.
    Plus la fitness est grande, plus la probabilite d'etre selectionne
    est elevee.
    """

    # Verifier que les deux listes ont la meme taille
    if len(population) != len(fitness_values):
        raise ValueError("La population et les fitness doivent avoir la meme taille.")

    if len(population) == 0:
        raise ValueError("La population ne doit pas etre vide.")

    # Les fitness negatives sont considerees comme nulles
    fitness_values = [max(0, fitness) for fitness in fitness_values]

    # Calculer la somme des fitness
    total_fitness = sum(fitness_values)

    # Si toutes les fitness sont nulles, choisir au hasard
    if total_fitness == 0:
        return random.choice(population)

    # Generer un nombre aleatoire entre 0 et la somme des fitness
    roulette = random.uniform(0, total_fitness)

    # Parcourir la roulette pour trouver le chromosome selectionne
    somme = 0
    for chromosome, fitness in zip(population, fitness_values):
        somme += fitness

        if somme >= roulette:
            return chromosome

    # Securite : retourner le dernier chromosome
    return population[-1]


if __name__ == "__main__":
    # Exemple simple pour tester la selection par loterie
    population = [
        "1100 | 0110 | 0010",
        "0011 | 1100 | 0100",
        "1000 | 0100 | 0010",
        "0110 | 0011 | 0001"
    ]

    fitness_values = [25, 15, 10, 5]

    chromosome_choisi = selection_roulette(population, fitness_values)

    print("Selection par loterie (Roulette Wheel Selection)")
    print("Population :", population)
    print("Fitness :", fitness_values)
    print("Chromosome selectionne :", chromosome_choisi)
