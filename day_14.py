from utils.timer import timer_decorator
from collections import Counter

@timer_decorator
def CalculatePolymers(pair_instertion_rules, polymer_template, steps):

    polymer_counter, current_pairs = Counter(), Counter()

    for polymer in polymer_template:
        polymer_counter[polymer] += 1

    for index in range(0, len(polymer_template) - 1):
        current_pairs[polymer_template[index:index + 2]] += 1

    new_pairs = Counter()

    for _ in range(steps):
        new_pairs.clear()

        for pair in current_pairs:
            # new polymer if formed from pair
            new_polymer = pair_instertion_rules[pair]
            new_polymer_ammount = current_pairs[pair]

            # new polymer pairs are created
            new_pairs[pair[0] + new_polymer] += new_polymer_ammount
            new_pairs[new_polymer + pair[1]] += new_polymer_ammount

            # old polymer pair ceases to exist
            new_pairs[pair] -= new_polymer_ammount

            # count newly created polymer
            polymer_counter[new_polymer] += new_polymer_ammount

        current_pairs += new_pairs

    most_common_poly  = max(polymer_counter, key=polymer_counter.get)
    least_common_poly = min(polymer_counter, key=polymer_counter.get)

    return polymer_counter[most_common_poly] - polymer_counter[least_common_poly]

if __name__ == "__main__":
    with open("input/day_14.txt") as file:    
        data = [line.rstrip() for line in file]

        polymer_template = ''.join(list(data[0]))
        pair_instertion_rules = {}

        for line in data[2:]:
            pair, resulting_polymer = line.split(' -> ')
            pair_instertion_rules[pair] = resulting_polymer

        print("Part 1:", CalculatePolymers(pair_instertion_rules, polymer_template, 10))
        print("Part 2:", CalculatePolymers(pair_instertion_rules, polymer_template, 40))
    