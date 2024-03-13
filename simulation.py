from multiprocessing import Process, Queue
from branch import Branch
from solution_manager import SolutionManager


class Simulation:
    branches: list[Branch]

    start_population: int

    solutions: list[tuple[float, ...]]

    solution_manager: SolutionManager

    def __init__(self, solution_manager):
        self.solutions = []
        self.solution_manager = solution_manager

    def initialize_branches(self, config):
        self.branches = [
            Branch(branch_config, self.solution_manager) for branch_config in config
        ]

    def insert_branch(self, branch: Branch):
        self.branches.append(branch)

    def inject_solution_manager(self, solution_manager: SolutionManager):
        self.solution_manager = solution_manager

    def get_branches(self):
        return self.branches.copy()

    def branch_process(self, branch, args, queue):
        print(f"Started branch {branch.name}")
        branch.run(*args)
        queue.put(branch)
        print(f"Ended branch {branch.name} with best {branch.solutions[0]}")

    def epoch(self, generations, solutions):
        queue = Queue()

        processes = [
            Process(
                target=self.branch_process,
                args=(
                    branch,
                    (generations, solutions),
                    queue
                )) for branch in self.branches
        ]

        for process in processes:
            process.start()

        self.branches = [
            queue.get() for _ in self.branches
        ]

    def run(self, start_population, epochs, generations_per_epoch):
        self.solutions = self.solution_manager.generate_solutions(start_population)

        for epoch in range(epochs):
            self.epoch(generations_per_epoch, self.solutions)

            self.solutions = []

            print(f"Epoch {epoch}:")
            for branch in self.branches:
                print(branch.name, self.solution_manager.score_solution(branch.solutions[0]), branch.solutions[0])
                self.solutions += branch.solutions[:start_population // len(self.branches)]

            self.solution_manager.sort_solutions(self.solutions)
