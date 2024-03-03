BRANCHES = [
    {
        "name": "Extreme",
        "best_population": 100,
        "best_population_guaranteed_percent": 0,
        "random_population": 100,
        "population": 1000,
        "mutation_percent": 200,
        "mutation_addition": 1,
    },
    {
        "name": "Normal",
        "best_population": 100,
        "best_population_guaranteed_percent": 10,
        "random_population": 50,
        "population": 1000,
        "mutation_percent": 50,
        "mutation_addition": 0.1,
    },
    {
        "name": "Super safe",
        "best_population": 200,
        "best_population_guaranteed_percent": 10,
        "random_population": 0,
        "population": 1000,
        "mutation_percent": 10,
        "mutation_addition": 0,
    }
]

GENERATIONS_PER_EPOCH = 1000
EPOCHS = 10

MIN_START_ELEMENT = -1000
MAX_START_ELEMENT = 1000
START_POPULATION = 1000

VARIABLES = 3