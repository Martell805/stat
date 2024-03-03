import random


class Branch:
    best_population = None
    best_population_guaranteed_percent = None
    best_population_guaranteed_modifier = None
    best_population_guaranteed_spots = None
    population = None

    mutation_percent = None
    min_mutation_modifier = None
    max_mutation_modifier = None

    mutation_addition = None

    def __init__(self, best_population, best_population_guaranteed_percent, population, mutation_percent, mutation_addition):
        self.set_best_population(best_population)
        self.set_best_population_guaranteed_percent(best_population_guaranteed_percent)
        self.set_population(population)
        self.set_mutation_percent(mutation_percent)
        self.set_mutation_addition(mutation_addition)

    def set_parameters(self, best_population, best_population_guaranteed_percent, population, mutation_percent, mutation_addition):
        self.set_best_population(best_population)
        self.set_best_population_guaranteed_percent(best_population_guaranteed_percent)
        self.set_population(population)
        self.set_mutation_percent(mutation_percent)
        self.set_mutation_addition(mutation_addition)

    def set_best_population(self, best_population):
        self.best_population = best_population

    def set_best_population_guaranteed_percent(self, best_population_guaranteed_percent):
        self.best_population_guaranteed_percent = best_population_guaranteed_percent
        self.best_population_guaranteed_modifier = best_population_guaranteed_percent / 100

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

        new_gen = []
        for _ in range(self.population - int(self.best_population * self.best_population_guaranteed_modifier)):
            el = random.choice(best_solutions)

            el0 = (el[0] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))
            el1 = (el[1] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))
            el2 = (el[2] * random.uniform(self.min_mutation_modifier, self.max_mutation_modifier)
                   + random.uniform(-self.mutation_addition, self.mutation_addition))

            new_gen.append((el0, el1, el2))

        new_gen += solutions[:int(self.best_population * self.best_population_guaranteed_modifier)]

        return new_gen

    def run(self, generations, fitness, solutions: list = None):
        if solutions is None:
            solutions = [(
                random.uniform(-1000, 1000),
                random.uniform(-1000, 1000),
                random.uniform(-1000, 1000),
            ) for _ in range(self.population)]

        solutions = solutions.copy()

        for i in range(generations):
            solutions = self.step(fitness, solutions)
            print(f"Gen {i} best: {fitness(min(solutions, key=fitness))} {min(solutions, key=fitness)}")

        solutions.sort(key=fitness)

        return solutions
