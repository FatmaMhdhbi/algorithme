import random

# ---------------- 1. Donnees du probleme ----------------

CAPACITES = [20, 15, 35, 40, 15, 15, 10]
NB_MAINTENANCES = [2, 2, 1, 1, 1, 1, 1]
DEMANDES = [80, 90, 65, 70]

PUISSANCE_TOTALE = sum(CAPACITES)
NB_CENTRALES = len(CAPACITES)
NB_PERIODES = 4

# Motifs autorises pour chaque centrale
MOTIFS_AUTORISES = {
    1: ["1000", "0100", "0010", "0001"],
    2: ["1100", "0110", "0011"]
}


# ---------------- 2. Creation d'un chromosome ----------------

def creer_chromosome():
    chromosome = []

    for duree in NB_MAINTENANCES:
        chromosome.append(random.choice(MOTIFS_AUTORISES[duree]))

    return chromosome


def creer_population(taille):
    return [creer_chromosome() for _ in range(taille)]


# ---------------- 3. Fonction objective / Fitness ----------------

def calculer_reserves(chromosome):
    reserves = []

    for periode in range(NB_PERIODES):
        puissance_en_maintenance = 0

        for i in range(NB_CENTRALES):
            if chromosome[i][periode] == "1":
                puissance_en_maintenance += CAPACITES[i]

        reserve = PUISSANCE_TOTALE - puissance_en_maintenance - DEMANDES[periode]
        reserves.append(reserve)

    return reserves


def fitness(chromosome):
    reserves = calculer_reserves(chromosome)

    if min(reserves) < 0:
        return 0

    return min(reserves)


# ---------------- 4. Selection par roulette / loterie ----------------

def selection_roulette(population):
    valeurs = [fitness(ch) for ch in population]
    somme = sum(valeurs)

    if somme == 0:
        return random.choice(population)

    tirage = random.uniform(0, somme)
    cumul = 0

    for chromosome, valeur in zip(population, valeurs):
        cumul += valeur

        if cumul >= tirage:
            return chromosome

    return population[-1]


# ---------------- 5. Croisement ----------------

def croisement(parent1, parent2):
    point = random.randint(1, NB_CENTRALES - 1)

    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]

    return enfant1, enfant2


# ---------------- 6. Mutation par inversion ----------------

def mutation_inversion(chromosome, probabilite):

    resultat = chromosome.copy()

    if random.random() < probabilite:

        # Choisir un gene (bloc de 4 bits)
        indice = random.randrange(NB_CENTRALES)

        gene = resultat[indice]
        duree = NB_MAINTENANCES[indice]

        motifs_valides = MOTIFS_AUTORISES[duree]
        inversions_possibles = []

        # Choisir deux positions et inverser les bits entre elles
        for debut in range(NB_PERIODES):
            for fin in range(debut + 1, NB_PERIODES):

                nouveau_gene = (
                    gene[:debut]
                    + gene[debut:fin + 1][::-1]
                    + gene[fin + 1:]
                )

                # Garder seulement les motifs valides
                if nouveau_gene in motifs_valides and nouveau_gene != gene:
                    inversions_possibles.append(nouveau_gene)

        if inversions_possibles:
            resultat[indice] = random.choice(inversions_possibles)

    return resultat


# ---------------- Mutation alternative ----------------

def mutation_alternative(chromosome):

    resultat = chromosome.copy()
    indice = random.randrange(NB_CENTRALES)

    duree = NB_MAINTENANCES[indice]

    choix = [
        motif for motif in MOTIFS_AUTORISES[duree]
        if motif != resultat[indice]
    ]

    resultat[indice] = random.choice(choix)

    return resultat


# ---------------- 7. Algorithme genetique ----------------

def algorithme_genetique(
    taille_population=49,
    generations=300,
    probabilite_croisement=0.80,
    probabilite_mutation=0.01
):

    population = creer_population(taille_population)
    historique = []

    for generation in range(generations):

        population.sort(key=fitness, reverse=True)

        # Elitisme : garder le meilleur chromosome
        nouvelle_population = [population[0].copy()]

        while len(nouvelle_population) < taille_population:

            # Selection des parents
            parent1 = selection_roulette(population)
            parent2 = selection_roulette(population)

            # Croisement
            if random.random() < probabilite_croisement:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1 = parent1.copy()
                enfant2 = parent2.copy()

            # Mutation
            enfant1 = mutation_inversion(
                enfant1, probabilite_mutation
            )

            enfant2 = mutation_inversion(
                enfant2, probabilite_mutation
            )

            nouvelle_population.append(enfant1)

            if len(nouvelle_population) < taille_population:
                nouvelle_population.append(enfant2)

        population = nouvelle_population

        meilleur = max(population, key=fitness)
        historique.append(fitness(meilleur))

    meilleur = max(population, key=fitness)

    return meilleur, historique


# ---------------- 8. Affichage des resultats ----------------

def afficher_resultat(chromosome):

    reserves = calculer_reserves(chromosome)

    print("\n========== MEILLEURE SOLUTION ==========")

    print("Chromosome :", " | ".join(chromosome))

    print("Fitness (reserve minimale) :", fitness(chromosome), "MW")

    print("\nPlanning de maintenance :")

    for i, gene in enumerate(chromosome):

        periodes = [
            str(j + 1)
            for j, bit in enumerate(gene)
            if bit == "1"
        ]

        print(
            f"Centrale {i + 1} ({CAPACITES[i]} MW) : "
            f"maintenance pendant periode(s) {', '.join(periodes)}"
        )

    print("\nBilan des reserves :")

    for i, reserve in enumerate(reserves):

        print(
            f"Periode {i + 1} : reserve = {reserve} MW "
            f"(demande = {DEMANDES[i]} MW)"
        )


# ---------------- 9. Programme principal ----------------

if __name__ == "__main__":

    random.seed(42)

    meilleur_chromosome, evolution = algorithme_genetique()

    afficher_resultat(meilleur_chromosome)

    print("\nMeilleure fitness par generation :")
    print(evolution)