import random

def has_duplicate(birthdays):
    return len(birthdays) != len(set(birthdays))

def run_experiment(n, trials):
    matches = 0
    for _ in range(trials):
        birthdays = [random.randint(1, 365) for _ in range(n)]
        if has_duplicate(birthdays):
            matches += 1
    return matches / trials

def main():
    print("n\tProbability")
    for n in range(5, 205, 5):
        probability = run_experiment(n, 10000)
        print(f"{n}\t{probability:.4f}")

main()