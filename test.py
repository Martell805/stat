from config import GENERATIONS_PER_EPOCH, EPOCHS, BRANCHES, MAX_START_ELEMENT, MIN_START_ELEMENT, START_POPULATION, \
    VARIABLES
from simulation import Simulation


def foo(x, y, z, w):
    return 6 * x ** 3 - 9 * y ** 2 + 90 * z + w - 25


def restriction(x, y, z, w):
    return x > 0 and z > 10


def fitness(tup):
    ans = abs(foo(*tup))

    if not restriction(*tup):
        ans += 10000

    return ans


simulation = Simulation()
simulation.initialize_branches(BRANCHES)
solutions = simulation.run(MIN_START_ELEMENT, MAX_START_ELEMENT, START_POPULATION, VARIABLES, EPOCHS,
                           GENERATIONS_PER_EPOCH, fitness)

solutions.sort(key=fitness)
print(f"Final:")
print(fitness(solutions[0]), solutions[0])
