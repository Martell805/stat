import random


class Branch:
    name: str

    breed: bool

    best_population: int
    best_population_guaranteed_percent: int
    best_population_guaranteed_modifier: int
    best_population_guaranteed_spots: int

    random_population: int

    population: int

    mutation_percent: int
    min_mutation_modifier: float
    max_mutation_modifier: float

    mutation_addition: float

    solutions: list[tuple]

    def __init__(self, configuration):
        self.name = configuration["name"]
        self.set_breed(configuration["breed"])
        self.set_best_population(configuration["best_population"])
        self.set_best_population_guaranteed_percent(configuration["best_population_guaranteed_percent"])
        self.set_random_population(configuration["random_population"])
        self.set_population(configuration["population"])
        self.set_mutation_percent(configuration["mutation_percent"])
        self.set_mutation_addition(configuration["mutation_addition"])

    def set_breed(self, breed):
        self.breed = breed

    def set_best_population(self, best_population):
        self.best_population = best_population

    def set_best_population_guaranteed_percent(self, best_population_guaranteed_percent):
        self.best_population_guaranteed_percent = best_population_guaranteed_percent
        self.best_population_guaranteed_modifier = best_population_guaranteed_percent / 100

    def set_random_population(self, random_population):
        self.random_population = random_population

    def set_population(self, population):
        self.population = population

    def set_mutation_percent(self, mutation_percent):
        self.mutation_percent = mutation_percent
        self.min_mutation_modifier = 1 - self.mutation_percent / 100
        self.max_mutation_modifier = 1 + self.mutation_percent / 100

    def set_mutation_addition(self, mutation_addition):
        self.mutation_addition = mutation_addition

    def get_solutions(self):
        return self.solutions.copy()

    def step(self, variables, fitness):
        self.solutions.sort(key=fitness)

        best_solutions = self.solutions[:self.best_population]
        best_solutions += random.sample(self.solutions, self.random_population)

        best_guaranteed_population = int(self.best_population * self.best_population_guaranteed_modifier)
        new_gen = []
        for _ in range(self.population - best_guaranteed_population):
            element1 = random.choice(best_solutions)

            if self.breed:
                element2 = random.choice(best_solutions)
                element1 = tuple(
                    (element1[i] + element2[i]) / 2 for i in range(variables)
                )

            new_gen.append(tuple((
                element1[i] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier) + random.uniform(
                    -self.mutation_addition, self.mutation_addition)
                for i in range(variables)
            )))

        new_gen += best_solutions[:best_guaranteed_population]

        return new_gen

    def run(self, generations, variables, fitness, solutions):
        self.solutions = solutions.copy()

        for _ in range(generations):
            self.solutions = self.step(variables, fitness)

        self.solutions.sort(key=fitness)

        return self.solutions
