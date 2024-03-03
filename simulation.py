import random

from branch import Branch


class Simulation:
    branches: list[Branch]

    min_start_element: int
    max_start_element: int
    start_population: int

    def initialize_branches(self, config):
        self.branches = [
            Branch(branch_config) for branch_config in config
        ]

    def insert_branch(self, branch: Branch):
        self.branches.append(branch)

    def run(self, min_start_element, max_start_element, start_population, epochs, generations_per_epoch, fitness):
        solutions = [(
            random.uniform(min_start_element, max_start_element),
            random.uniform(min_start_element, max_start_element),
            random.uniform(min_start_element, max_start_element),
        ) for _ in range(start_population)]

        for epoch in range(epochs):
            answers = [
                branch.run(generations_per_epoch, fitness, solutions) for branch in self.branches
            ]

            solutions = []

            print(f"Epoch {epoch}:")
            for branch, answer in zip(self.branches, answers):
                print(branch.name, fitness(answer[0]), answer[0])
                solutions += answer[:start_population // len(self.branches)]

        solutions.sort(key=fitness)

        return solutions
