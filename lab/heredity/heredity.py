import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    ans = 1

    gene = {}
    for p in people:
        if p in one_gene:
            gene[p] = 1
        elif p in two_genes:
            gene[p] = 2
        else:
            gene[p] = 0

    prob = [[[0 for _ in range(4)] for __ in range(4)] for ___ in range(3)]
    for i in range(3):
        prob[i][3][3] = PROBS["gene"][i]

    for i in range(3):
        mother_prob = [0, 0]
        if i == 0:
            mother_prob[0] = 1 - PROBS["mutation"]
            mother_prob[1] = PROBS["mutation"]
        elif i == 1:
            mother_prob[0] = mother_prob[1] = 0.5
        else:
            mother_prob[0] = PROBS["mutation"]
            mother_prob[1] = 1 - PROBS["mutation"]

        for j in range(3):
            father_prob = [0, 0]
            if j == 0:
                father_prob[0] = 1 - PROBS["mutation"]
                father_prob[1] = PROBS["mutation"]
            elif j == 1:
                father_prob[0] = father_prob[1] = 0.5
            else:
                father_prob[0] = PROBS["mutation"]
                father_prob[1] = 1 - PROBS["mutation"]

            for k in range(2):
                for l in range(2):
                    prob[k + l][i][j] += mother_prob[k] * father_prob[l]

    for _, p in people.items():
        if p["mother"] and p["father"]:
            if p["mother"] in one_gene:
                mother_genes = 1
            elif p["mother"] in two_genes:
                mother_genes = 2
            else:
                mother_genes = 0
            if p["father"] in one_gene:
                father_genes = 1
            elif p["father"] in two_genes:
                father_genes = 2
            else:
                father_genes = 0

        if p["name"] in one_gene:
            if not p["mother"] and not p["father"]:
                ans *= PROBS["gene"][1]
            else:
                ans *= prob[1][mother_genes][father_genes]

            ans *= PROBS["trait"][1][p["name"] in have_trait]
        elif p["name"] in two_genes:
            if not p["mother"] and not p["father"]:
                ans *= PROBS["gene"][2]
            else:
                ans *= prob[2][mother_genes][father_genes]

            ans *= PROBS["trait"][2][p["name"] in have_trait]
        else:
            if not p["mother"] and not p["father"]:
                ans *= PROBS["gene"][0]
            else:
                ans *= prob[0][mother_genes][father_genes]

            ans *= PROBS["trait"][0][p["name"] in have_trait]

    return ans


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person, prob in probabilities.items():
        if person in one_gene:
            prob["gene"][1] += p
        elif person in two_genes:
            prob["gene"][2] += p
        else:
            prob["gene"][0] += p

        prob["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, prob in probabilities.items():
        for word in ["gene", "trait"]:
            sum = 0
            for _, x in prob[word].items():
                sum += x
            print(sum)
            for each, x in prob[word].items():
                probabilities[person][word][each] /= sum


if __name__ == "__main__":
    main()
