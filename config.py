BRANCHES = [
    {
        "name": "Extreme",
        "breed_strategy": "NONE",
        "best_population": 100,
        "best_population_guaranteed_percent": 1,
        "random_population": 100,
        "population": 1000,
        "mutation_percent": 200,
        "mutation_addition": 1,
    },
    {
        "name": "Normal",
        "breed_strategy": "NONE",
        "best_population": 100,
        "best_population_guaranteed_percent": 10,
        "random_population": 50,
        "population": 1000,
        "mutation_percent": 50,
        "mutation_addition": 0.1,
    },
    {
        "name": "Safe",
        "breed_strategy": "NONE",
        "best_population": 200,
        "best_population_guaranteed_percent": 10,
        "random_population": 0,
        "population": 1000,
        "mutation_percent": 10,
        "mutation_addition": 0,
    },
    {
        "name": "UberSafe",
        "breed_strategy": "NONE",
        "best_population": 200,
        "best_population_guaranteed_percent": 10,
        "random_population": 0,
        "population": 1000,
        "mutation_percent": 1,
        "mutation_addition": 0.0001,
    },
    {
        "name": "AvgBreed",
        "breed_strategy": "AVERAGE",
        "best_population": 200,
        "best_population_guaranteed_percent": 5,
        "random_population": 50,
        "population": 1000,
        "mutation_percent": 10,
        "mutation_addition": 0.1,
    },
    {
        "name": "ChuBreed",
        "breed_strategy": "CHOOSE",
        "best_population": 200,
        "best_population_guaranteed_percent": 5,
        "random_population": 50,
        "population": 1000,
        "mutation_percent": 10,
        "mutation_addition": 0.1,
    },
]

GENERATIONS_PER_EPOCH = 1000
EPOCHS = 10

MIN_START_ELEMENT = -100
MAX_START_ELEMENT = 100
START_POPULATION = 1000

MAX_MATES_AMOUNT = 3

MAX_MUTATION_TRIES = 3

USE_LOG_GRAPH = True
MAX_GRAPH_VALUE = 3
