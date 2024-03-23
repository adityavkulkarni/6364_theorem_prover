"""
https://github.com/nomaanakhan/Theorem-Prover-for-Clause-Logic
https://github.com/codeCollision4/resolution_solver
"""
import argparse
import time

OUTPUT = []


def parse_kb_file(filepath):
    initial_kb = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            clause = []
            current_literal = ""
            for char in line:
                if char == ' ':
                    clause.append(current_literal.strip())
                    current_literal = ""
                else:
                    current_literal += char
            if current_literal:
                clause.append(current_literal.strip())

            initial_kb.append(clause)
    last_clause = initial_kb[-1]
    initial_kb = initial_kb[:-1]
    return initial_kb, last_clause


def negate_clause(clause):
    n = []
    for literal in clause:
        n.append(f"~{literal}" if "~" not in literal else f"{literal[1]}")
    return n


def theorem_prover(kb, clause_to_test):
    ind = 1
    negated_clause = negate_clause(clause_to_test)
    for cl in kb:
        print_stdout(f"{ind}. {' '.join(cl)} {{}}")
        ind += 1
    for c in negated_clause:
        kb.append([c])
        print_stdout(f"{ind}. {c} {{}}")
        ind += 1
    cli = 1
    while cli < ind - 1:
        clj = 0
        while clj < cli:
            result = resolve(kb[cli], kb[clj], kb)
            if result is False:
                print_stdout(f"{ind}. Contradiction {{{cli+1}, {clj+1}}}")
                ind += 1
                print_stdout("Valid")
                return
            elif result is True:
                clj += 1
                continue
            else:
                print_stdout(f"{ind}. {' '.join(result)} {{{cli+1}, {clj+1}}}")
                ind += 1
                kb.append(result)
            clj += 1
        cli += 1
    print_stdout('Not Valid')


def resolve(c1, c2, clauses):
    resolved2 = c1 + c2
    hashmap = {}
    for r1 in resolved2:
        if r1 not in hashmap.keys():
            hashmap[r1] = 0

    resolved = list(hashmap.keys())
    ors = list(hashmap.keys())
    for l1 in c1:
        for l2 in c2:
            if is_contradiction(l1, l2):
                resolved.remove(l1)
                resolved.remove(l2)
                if len(resolved) == 0:
                    return False
                elif impTrue(resolved):
                    return True
                else:
                    for cl in clauses:
                        if not Diff(resolved, cl):
                            return True
                    return resolved

    if resolved == ors:
        return True


def is_contradiction(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    else:
        return False



def impTrue(resolved):
    for r1 in resolved:
        for r2 in resolved[resolved.index(r1) + 1:]:  # Start from next element
            if is_contradiction(r1, r2):
                return True
    return False


def Diff(li1, li2):
    li1 = list(li1)
    li2 = list(li2)
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def print_stdout(txt):
    global OUTPUT
    print(txt)
    OUTPUT.append(txt)


def test(path):
    print("Execution time: {:.3f} seconds".format(time.time() - start_time))
    with open(path.replace("in", "out"), "r") as f:
        lines = [x.replace("\n", "") for x in f.readlines()]
    if len(lines) != len(OUTPUT):
        print("Lists are not equal in length.")
        l_str = '\n'.join(lines)
        print(f"Expected:\n{l_str}\n")
        l_str = '\n'.join(OUTPUT)
        print(f"Actual:\n{l_str}\n")
    else:
        unequal_elements = [(elem1, elem2) for elem1, elem2 in zip(lines, OUTPUT) if elem1 != elem2]
        if not unequal_elements:
            print("Lists are equal.")
        else:
            print("Lists are not equal.")
            print("Elements that are not equal:")
            for elem1, elem2 in unequal_elements:
                print(f"{elem1} (Expected) != {elem2} (Actual)")


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("kb_file",
                        type=str,
                        help="Path to kb file")
    args = parser.parse_args()
    init_kb, ct = parse_kb_file(args.kb_file)
    theorem_prover(init_kb, ct)
    test(args.kb_file)
