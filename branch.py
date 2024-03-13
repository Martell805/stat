import random

from solution_manager import SolutionManager


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

    best_score_in_generation: list
    average_score_in_generation: list
    average_best_score_in_generation: list

    best_score_in_epoch: list
    average_score_in_epoch: list
    average_best_score_in_epoch: list

    solution_manager: SolutionManager

    def __init__(self, configuration, solution_manager):
        self.name = configuration["name"]
        self.set_breed(configuration["breed"])
        self.set_best_population(configuration["best_population"])
        self.set_best_population_guaranteed_percent(configuration["best_population_guaranteed_percent"])
        self.set_random_population(configuration["random_population"])
        self.set_population(configuration["population"])
        self.set_mutation_percent(configuration["mutation_percent"])
        self.set_mutation_addition(configuration["mutation_addition"])

        self.best_score_in_generation = []
        self.average_score_in_generation = []
        self.average_best_score_in_generation = []

        self.best_score_in_epoch = []
        self.average_score_in_epoch = []
        self.average_best_score_in_epoch = []

        self.solutions = []

        self.solution_manager = solution_manager

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

    def step(self):
        self.solution_manager.sort_solutions(self.solutions)

        best_solutions = self.solutions[:self.best_population]
        best_solutions += random.sample(self.solutions, self.random_population)

        best_guaranteed_population = int(self.best_population * self.best_population_guaranteed_modifier)
        self.solutions = []
        for _ in range(self.population - best_guaranteed_population):
            element1 = random.choice(best_solutions)

            if self.breed:
                element1 = self.solution_manager.breed_selected_solution(element1, best_solutions)

            self.solutions.append(self.solution_manager.mutate_solution(
                element1,
                self.min_mutation_modifier,
                self.max_mutation_modifier,
                self.mutation_addition
            ))

        self.solutions += best_solutions[:best_guaranteed_population]

        self.solution_manager.sort_solutions(self.solutions)

        self.average_score_in_generation.append(self.solution_manager.get_average_score(self.solutions))
        self.average_best_score_in_generation.append(
            self.solution_manager.get_average_score(self.solutions[:max(self.best_population, 1)]))
        self.best_score_in_generation.append(self.solution_manager.score_solution(self.solutions[0]))

    def run(self, generations, solutions):
        if self.solutions:
            self.solutions = self.solutions[:self.population // 2] + solutions.copy()[:self.population // 2]
        else:
            self.solutions = solutions.copy()

        self.solution_manager.sort_solutions(self.solutions)

        for _ in range(generations):
            self.step()

        self.solution_manager.sort_solutions(self.solutions)

        self.average_score_in_epoch.append(self.solution_manager.get_average_score(self.solutions))
        self.average_best_score_in_epoch.append(
            self.solution_manager.get_average_score(self.solutions[:max(self.best_population, 1)]))
        self.best_score_in_epoch.append(self.solution_manager.score_solution(self.solutions[0]))
