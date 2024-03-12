import time
from cmath import log

from config import GENERATIONS_PER_EPOCH, EPOCHS, BRANCHES, MAX_START_ELEMENT, MIN_START_ELEMENT, START_POPULATION, \
    VARIABLES
from simulation import Simulation

import matplotlib.pyplot as plt


def foo(x, y, z, w):
    return 6 * x ** 3 - 9 * y ** 2 + 90 * z + w - 25


def restriction(x, y, z, w):
    return x > 0 and z > 10
    # return True


def fitness(tup):
    ans = abs(foo(*tup))

    if not restriction(*tup):
        ans += 10000

    return ans


if __name__ == '__main__':
    simulation = Simulation()
    simulation.initialize_branches(BRANCHES)

    start_time = time.time()
    simulation.run(MIN_START_ELEMENT, MAX_START_ELEMENT, START_POPULATION, VARIABLES, EPOCHS,
                               GENERATIONS_PER_EPOCH, fitness)
    print(f"--- {time.time() - start_time} seconds ---")

    print(f"Final:")
    print(fitness(simulation.solutions[0]), simulation.solutions[0])

    branches = simulation.get_branches()

    fig, axes = plt.subplots(len(branches), 3, figsize=(15, 2 * len(BRANCHES)), layout='constrained')

    for branch, row in zip(branches, axes):
        row = iter(row)

        best_subplot = next(row)
        best_subplot.set_title(f"Best of {branch.get_name()}")
        best_subplot.plot(list(map(lambda x: log(x, 10), branch.get_best_score_in_epoch())))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of {branch.get_name()}")
        average_subplot.plot(list(map(lambda x: log(x, 10), branch.get_average_score_in_epoch())))

        average_subplot = next(row)
        average_subplot.set_title(f"Avg of best {branch.best_population} in {branch.get_name()}")
        average_subplot.plot(list(map(lambda x: log(x, 10), branch.get_average_best_score_in_epoch())))

    plt.show()
