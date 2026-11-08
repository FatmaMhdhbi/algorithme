import random


# 1. DONNEES DU PROBLEME


# Capacite de chaque centrale en MW
capacites = [20, 15, 35, 40, 15, 15, 10]

# Nombre d'intervalles de maintenance necessaires
nb_maintenances = [2, 2, 1, 1, 1, 1, 1]

# Demande en puissance pour chaque intervalle
demandes = [80, 90, 65, 70]

# Capacite totale des centrales
capacite_totale = sum(capacites)

# Les genes possibles pour chaque centrale
# Chaque gene contient 4 bits : un bit par intervalle
genes_possibles = [
    ["1100", "0110", "0011"],          # Centrale 1
    ["1100", "0110", "0011"],          # Centrale 2
    ["1000", "0100", "0010", "0001"],  # Centrale 3
    ["1000", "0100", "0010", "0001"],  # Centrale 4
    ["1000", "0100", "0010", "0001"],  # Centrale 5
    ["1000", "0100", "0010", "0001"],  # Centrale 6
    ["1000", "0100", "0010", "0001"]   # Centrale 7
]

# Parametres de l'algorithme genetique
TAILLE_POPULATION = 50
NB_GENERATIONS = 200
PROB_CROISEMENT = 0.8
PROB_MUTATION = 0.1


# 2. CREATION D'UN CHROMOSOME


def creer_chromosome():
    chromosome = []

    for i in range(7):
        gene = random.choice(genes_possibles[i])
        chromosome.append(gene)

    return chromosome



# 3. CREATION DE LA POPULATION


def creer_population():
    population = []

    for i in range(TAILLE_POPULATION):
        chromosome = creer_chromosome()
        population.append(chromosome)

    return population



# 4. CALCUL DE LA RESERVE


def calculer_reserves(chromosome):

    reserves = []

    for intervalle in range(4):

        puissance_maintenance = 0

        for centrale in range(7):

            gene = chromosome[centrale]

            if gene[intervalle] == "1":
                puissance_maintenance += capacites[centrale]

        reserve = (
            capacite_totale
            - puissance_maintenance
            - demandes[intervalle]
        )

        reserves.append(reserve)

    return reserves



# 5. FONCTION OBJECTIVE / FITNESS


def fitness(chromosome):

    reserves = calculer_reserves(chromosome)

    # La reserve doit etre strictement positive
    if min(reserves) <= 0:
        return 0

    # Performance = reserve minimale
    return min(reserves)



# 6. SELECTION PAR LOTERIE (ROULETTE)


def selection_roulette(population):

    evaluations = [fitness(individu) for individu in population]

    total_fitness = sum(evaluations)

    # Si toutes les fitness sont nulles,
    # on effectue une selection aleatoire
    if total_fitness == 0:
        return random.choice(population)

    # Tirage aleatoire sur la roue de loterie
    valeur = random.uniform(0, total_fitness)

    cumul = 0

    for i in range(len(population)):

        cumul += evaluations[i]

        if cumul >= valeur:
            return population[i]

    return population[-1]



# 7. CROISEMENT EN UN POINT


def croisement(parent1, parent2):

    # Le croisement se fait entre deux genes
    point = random.randint(1, 6)

    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]

    return enfant1, enfant2



# 8. MUTATION PAR INVERSION


def mutation_inversion(chromosome):

    chromosome = chromosome.copy()

    # Choisir une centrale au hasard
    position = random.randint(0, 6)

    # Inverser l'ordre des 4 bits du gene
    gene = chromosome[position]

    chromosome[position] = gene[::-1]

    return chromosome



# 9. ALGORITHME GENETIQUE


def algorithme_genetique():

    population = creer_population()

    meilleur_chromosome = None
    meilleure_fitness = -1

    for generation in range(NB_GENERATIONS):

        # Evaluation de la population
        evaluations = [fitness(individu) for individu in population]

        # Recherche du meilleur individu
        indice = evaluations.index(max(evaluations))

        meilleur_actuel = population[indice]
        fitness_actuelle = evaluations[indice]

        if fitness_actuelle > meilleure_fitness:

            meilleure_fitness = fitness_actuelle
            meilleur_chromosome = meilleur_actuel.copy()

        # Elitisme : conserver le meilleur individu
        nouvelle_population = [meilleur_chromosome.copy()]

        # Creation de la nouvelle population
        while len(nouvelle_population) < TAILLE_POPULATION:

            parent1 = selection_roulette(population)
            parent2 = selection_roulette(population)

            # Croisement
            if random.random() < PROB_CROISEMENT:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1 = parent1.copy()
                enfant2 = parent2.copy()

            # Mutation
            if random.random() < PROB_MUTATION:
                enfant1 = mutation_inversion(enfant1)

            if random.random() < PROB_MUTATION:
                enfant2 = mutation_inversion(enfant2)

            nouvelle_population.append(enfant1)

            if len(nouvelle_population) < TAILLE_POPULATION:
                nouvelle_population.append(enfant2)

        population = nouvelle_population

    return meilleur_chromosome, meilleure_fitness


# 10. AFFICHAGE DES RESULTATS


def afficher_resultats(chromosome):

    print("\n RESULTATS ")

    print("\nMeilleur chromosome :")

    for i in range(7):
        print("Centrale", i + 1, ":", chromosome[i])

    reserves = calculer_reserves(chromosome)

    print("\nReserves de puissance :")

    for i in range(4):
        print(
            "Intervalle", i + 1,
            ":", reserves[i], "MW"
        )

    print("\nFitness :", fitness(chromosome), "MW")

    print("\nCalendrier de maintenance :")

    for i in range(7):

        intervalles = []

        for j in range(4):

            if chromosome[i][j] == "1":
                intervalles.append(j + 1)

        print(
            "Centrale", i + 1,
            ": maintenance aux intervalles",
            intervalles
        )


# 11. PROGRAMME PRINCIPAL


if __name__ == "__main__":

    # Exemple donne dans le document
    exemple = [
        "0110",
        "0011",
        "0001",
        "1000",
        "0100",
        "0010",
        "1000"
    ]

    print(" VERIFICATION DE L'EXEMPLE DU COURS ")

    afficher_resultats(exemple)

    # Execution de l'algorithme genetique
    print("\n ALGORITHME GENETIQUE ")

    meilleur, valeur = algorithme_genetique()

    print("\nMeilleure fitness trouvee :", valeur)

    afficher_resultats(meilleur)
