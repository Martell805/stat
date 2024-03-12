import random
from multiprocessing import Process, Queue
from branch import Branch


class Simulation:
    branches: list[Branch]

    min_start_element: int
    max_start_element: int
    start_population: int

    plot_data: dict

    def __init__(self):
        self.plot_data = dict()

    def initialize_branches(self, config):
        self.branches = [
            Branch(branch_config) for branch_config in config
        ]

    def insert_branch(self, branch: Branch):
        self.branches.append(branch)

    def get_branches(self):
        return self.branches.copy()

    def branch_process(self, branch, args, queue):
        print(f"Started branch {branch.get_name()}")
        result = branch.run(*args)
        queue.put((branch.get_name(), result))
        print(f"Ended branch {branch.get_name()} with best {result[0]}")

    def __get_average_score(self, fitness, solutions):
        return sum(map(fitness, solutions)) / len(solutions)

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

        answers = [
            queue.get() for _ in self.branches
        ]

        for branch_name, answer in answers:
            for branch in self.branches:
                if branch_name == branch.get_name():
                    branch.get_average_score_in_epoch().append(self.__get_average_score(fitness, answer))
                    branch.get_average_best_score_in_epoch().append(
                        self.__get_average_score(fitness, answer[:max(branch.best_population, 1)]))
                    branch.get_best_score_in_epoch().append(fitness(answer[0]))

        return answers

    def run(self, min_start_element, max_start_element, start_population, variables, epochs, generations_per_epoch,
            fitness):
        solutions = [tuple(
            random.uniform(min_start_element, max_start_element) for _ in range(variables)
        ) for _ in range(start_population)]

        for epoch in range(epochs):
            answers = self.epoch(generations_per_epoch, variables, fitness, solutions)

            solutions = []

            print(f"Epoch {epoch}:")
            for branch_name, answer in answers:
                print(branch_name, fitness(answer[0]), answer[0])
                solutions += answer[:start_population // len(self.branches)]

        solutions.sort(key=fitness)

        return solutions
