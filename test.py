from config import GENERATIONS_PER_EPOCH, EPOCHS, BRANCHES, MAX_START_ELEMENT, MIN_START_ELEMENT, START_POPULATION
from simulation import Simulation


def foo(x, y, z):
    return 6*x**3 - 9*y**2 + 90*z - 25


def restriction(x, y, z):
    return x > 0 and z > 10


def fitness(tup):
    x, y, z = tup
    ans = abs(foo(x, y, z))

    if not restriction(x, y, z):
        ans += 10000

    return ans


simulation = Simulation()
simulation.initialize_branches(BRANCHES)
solutions = simulation.run(MIN_START_ELEMENT, MAX_START_ELEMENT, START_POPULATION, EPOCHS, GENERATIONS_PER_EPOCH, fitness)

solutions.sort(key=fitness)
print(f"Final:")
print(fitness(solutions[0]), solutions[0])
