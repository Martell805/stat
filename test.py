from branch import Branch


POPULATION = 1000
BEST_POPULATION = 100
BEST_POPULATION_GUARANTEED_PERCENT = 10
GENERATIONS = 10000

MIN_START_ELEMENT = -1000
MAX_START_ELEMENT = 1000

MUTATION_PERCENT = 50
MUTATION_ADDITION = 0.1

MIN_MUTATION = 1 - MUTATION_PERCENT / 100
MAX_MUTATION = 1 + MUTATION_PERCENT / 100


def foo(x, y, z):
    return 6*x**3 + 9*y**2 + 90*z - 25


def restriction(x, y, z):
    return x > 0 and z > 10


def fitness(tup):
    x, y, z = tup
    ans = abs(foo(x, y, z))

    if not restriction(x, y, z):
        ans += 10000

    return ans


branch = Branch(BEST_POPULATION, BEST_POPULATION_GUARANTEED_PERCENT, POPULATION, MUTATION_PERCENT, MUTATION_ADDITION)

answer = branch.run(GENERATIONS, fitness)[0]

print(fitness(answer))
print(answer)
