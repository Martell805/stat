import random
from multiprocessing import Process, Queue
from branch import Branch


class Simulation:
    branches: list[Branch]

    min_start_element: int
    max_start_element: int
    start_population: int

    solutions: list[tuple]

    def __init__(self):
        self.solutions = []

    def initialize_branches(self, config):
        self.branches = [
            Branch(branch_config) for branch_config in config
        ]

    def insert_branch(self, branch: Branch):
        self.branches.append(branch)

    def get_branches(self):
        return self.branches.copy()

    def branch_process(self, branch, args, queue):
        print(f"Started branch {branch.name}")
        branch.run(*args)
        queue.put(branch)
        print(f"Ended branch {branch.name} with best {branch.solutions[0]}")

    def epoch(self, generations, variables, fitness, solutions):
        queue = Queue()

        processes = [
            Process(
                target=self.branch_process,
                args=(
                    branch,
                    (generations, variables, fitness, solutions),
                    queue
                )) for branch in self.branches
        ]

        for process in processes:
            process.start()

        self.branches = [
            queue.get() for _ in self.branches
        ]

    def run(self, min_start_element, max_start_element, start_population, variables, epochs, generations_per_epoch,
            fitness):
        self.solutions = [tuple(
            random.uniform(min_start_element, max_start_element) for _ in range(variables)
        ) for _ in range(start_population)]

        for epoch in range(epochs):
            self.epoch(generations_per_epoch, variables, fitness, self.solutions)

            self.solutions = []

            print(f"Epoch {epoch}:")
            for branch in self.branches:
                print(branch.name, fitness(branch.solutions[0]), branch.solutions[0])
                self.solutions += branch.solutions[:start_population // len(self.branches)]

            self.solutions.sort(key=fitness)
