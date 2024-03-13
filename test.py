import time
from cmath import log

from config import GENERATIONS_PER_EPOCH, EPOCHS, BRANCHES, MAX_START_ELEMENT, MIN_START_ELEMENT, START_POPULATION, MAX_MATES_AMOUNT, MAX_GRAPH_VALUE, USE_LOG_GRAPH
from simulation import Simulation

import matplotlib.pyplot as plt

from solution_manager import SolutionManager


def foo(x, y, z, w):
    return 6 * x ** 3 - 9 * y ** 2 + 90 * z + w - 25


def restriction(x, y, z, w):
    return True
    # return x > 0 and z > 10


def modify_result(x):
    if USE_LOG_GRAPH:
        return min(log(x, 10).real, MAX_GRAPH_VALUE)
    return min(x, MAX_GRAPH_VALUE)


if __name__ == '__main__':
    solution_manager = SolutionManager(MIN_START_ELEMENT, MAX_START_ELEMENT, MAX_MATES_AMOUNT, foo, restriction)

    simulation = Simulation(solution_manager)
    simulation.initialize_branches(BRANCHES)

    start_time = time.time()
    simulation.run(START_POPULATION, EPOCHS, GENERATIONS_PER_EPOCH)
    print(f"--- {time.time() - start_time} seconds ---")

    print(f"Final:")
    print(solution_manager.score_solution(simulation.solutions[0]), simulation.solutions[0])

    branches = simulation.branches

    fig, axes = plt.subplots(len(branches), 6, figsize=(30, 2 * len(BRANCHES)), layout='constrained')

    for branch, row in zip(branches, axes):
        row = iter(row)

        best_subplot = next(row)
        best_subplot.set_title(f"Best of {branch.name}")
        best_subplot.plot(list(map(modify_result, branch.best_score_in_epoch)))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of {branch.name}")
        average_subplot.plot(list(map(modify_result, branch.average_score_in_epoch)))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of best {branch.best_population} in {branch.name}")
        average_subplot.plot(list(map(modify_result, branch.average_best_score_in_epoch)))

        best_subplot = next(row)
        best_subplot.set_title(f"Best of {branch.name}")
        best_subplot.plot(list(map(modify_result, branch.best_score_in_generation)))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of {branch.name}")
        average_subplot.plot(list(map(modify_result, branch.average_score_in_generation)))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of best {branch.best_population} in {branch.name}")
        average_subplot.plot(list(map(modify_result, branch.average_best_score_in_generation)))

    plt.show()
