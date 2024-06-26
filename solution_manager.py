import random
from inspect import signature

from breed_strategy import BreedStrategy


class SolutionManager:
    min_element: int
    max_element: int
    max_mates_amount: int
    max_mutation_tries: int
    variables: int
    function: callable
    restriction: callable

    def __init__(self, min_element, max_element, max_mates_amount, max_mutation_tries, function, restriction):
        self.min_element = min_element
        self.max_element = max_element
        self.variables = len(signature(function).parameters)
        self.max_mates_amount = max_mates_amount
        self.max_mutation_tries = max_mutation_tries
        self.function = function
        self.restriction = restriction

    def generate_solution(self) -> tuple:
        result = tuple(
            random.uniform(self.min_element, self.max_element) for _ in range(self.variables)
        )

        while not self.restriction(*result):
            result = tuple(
                random.uniform(self.min_element, self.max_element) for _ in range(self.variables)
            )

        return result

    def breed_solutions(self, solution1, solution2, breed_strategy) -> tuple[float, ...] | None:
        result = None

        match breed_strategy:
            case BreedStrategy.AVERAGE:
                result = tuple(
                    (solution1[i] + solution2[i]) / 2 for i in range(self.variables)
                )
            case BreedStrategy.CHOOSE:
                result = tuple(
                    random.choice([solution1[i], solution2[i]]) for i in range(self.variables)
                )

        if self.restriction(*result):
            return result

        return None

    def breed_selected_solution(self, solution1, solutions, breed_strategy):
        if breed_strategy == BreedStrategy.NONE:
            return solution1

        solutions = random.sample(solutions, self.max_mates_amount)

        for solution2 in solutions:
            result = self.breed_solutions(solution1, solution2, breed_strategy)
            if result is not None:
                return result

        return solution1

    def generate_solutions(self, n) -> list[tuple[float, ...]]:
        return [self.generate_solution() for _ in range(n)]

    def score_solution(self, solution):
        return self.function(*solution)

    def mutate_solution(self, solution, min_mutation_modifier, max_mutation_modifier, mutation_addition):
        for _ in range(self.max_mutation_tries):
            result = tuple((
                solution[i] * random.uniform(min_mutation_modifier, max_mutation_modifier) +
                random.uniform(-mutation_addition, mutation_addition)
                for i in range(self.variables)
            ))

            if self.restriction(*result):
                return result

        return solution

    def sort_solutions(self, solutions):
        solutions.sort(key=self.score_solution)

    def get_average_score(self, solutions):
        return sum(map(self.score_solution, solutions)) / len(solutions)
