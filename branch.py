import random


class Branch:
    best_population: int
    best_population_guaranteed_percent: int
    best_population_guaranteed_modifier: int
    best_population_guaranteed_spots: int

    random_population: int

    population: int

    name: str

    mutation_percent: int
    min_mutation_modifier: float
    max_mutation_modifier: float

    mutation_addition: float

    def __init__(self, configuration):
        self.name = configuration["name"]
        self.set_best_population(configuration["best_population"])
        self.set_best_population_guaranteed_percent(configuration["best_population_guaranteed_percent"])
        self.set_random_population(configuration["random_population"])
        self.set_population(configuration["population"])
        self.set_mutation_percent(configuration["mutation_percent"])
        self.set_mutation_addition(configuration["mutation_addition"])

    def set_parameters(self, best_population, best_population_guaranteed_percent, random_population, population,
                       mutation_percent, mutation_addition):
        self.set_best_population(best_population)
        self.set_best_population_guaranteed_percent(best_population_guaranteed_percent)
        self.set_random_population(random_population)
        self.set_population(population)
        self.set_mutation_percent(mutation_percent)
        self.set_mutation_addition(mutation_addition)

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

    def step(self, fitness, solutions):
        solutions.sort(key=fitness)

        best_solutions = solutions[:self.best_population]
        best_solutions += random.sample(solutions, self.random_population)

        best_guaranteed_population = int(self.best_population * self.best_population_guaranteed_modifier)
        new_gen = []
        for _ in range(self.population - best_guaranteed_population):
            el = random.choice(best_solutions)

            el0 = (el[0] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))
            el1 = (el[1] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))
            el2 = (el[2] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))

            new_gen.append((el0, el1, el2))

        new_gen += best_solutions[:best_guaranteed_population]

        return new_gen

    def run(self, generations, fitness, solutions):
        solutions = solutions.copy()

        for _ in range(generations):
            solutions = self.step(fitness, solutions)

        solutions.sort(key=fitness)

        return solutions
