import itertools
import random
import time


def generate_recursive_puzzle(number_of_statements, level=8, max_solutions=1):
    if number_of_statements < 3:
        raise Exception('Number of statements must be >= 3')
    if level <= 0 or level >= 9:
        raise Exception('Level must be in 1...8')
    if max_solutions <= 0:
        raise Exception('Max solutions must be >= 1')

    def check_for_exclusive(stmt: list, i: int, slc: slice):
        return all(x != i for x, _ in list(zip(range(len(stmt)), stmt))[slc])

    false_true_arg = 1
    number_of_stmt_arg = 2
    even_odd_arg = 3
    stmt_index_arg = 4
    first_condition = [[
        f"This is a numbered list of {number_of_statements} statements.",
        [],
        lambda stmt, i, args: True,
    ]]
    first_level = [
        # "Exactly X of the previous/next statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:i]) == args[1])) in (0, 2)
            if len(stmt[:i]) > args[1] else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the previous statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:]) == args[1])) in (0, 2)
            if len(stmt[i + 1:]) > args[1] else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the next statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "Exactly X of the first/last/previous/next Y statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:args[2]]) == args[1])) in (0, 2)
            if len(stmt[:args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 and check_for_exclusive(stmt, i, slice(None, args[2])) else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the first {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[-args[2]:]) == args[1])) in (0, 2)
            if len(stmt[-args[2]:]) == args[2] and args[2] > args[1] and args[2] > 1 and i not in range(0, args[2]) and check_for_exclusive(stmt, i, slice(-args[2], None)) else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the last {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i - args[2]:i]) == args[1])) in (0, 2)
            if len(stmt[i - args[2]:i]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the previous {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:i + 1 + args[2]]) == args[1])) in (0, 2)
            if len(stmt[i + 1:i + 1 + args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the next {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "Exactly X of the even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2])::2]) == args[1])) in (0, 2)
            if len(stmt[int(args[2])::2]) >= args[1] and check_for_exclusive(stmt, i, slice(int(args[2]), None, 2)) else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "Exactly X of the previous/next even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2]):i:2]) == args[1])) in (0, 2)
            if len(stmt[int(args[2]):i:2]) > args[1] else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the previous {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1 + ((i % 2) == args[2])::2]) == args[1])) in (0, 2)
            if len(stmt[i + 1 + ((i % 2) == args[2])::2]) > args[1] else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the next {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "Exactly W of the statements X, Y and Z is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, stmt_index_arg, stmt_index_arg, stmt_index_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(stmt[k]) == args[0] for k in args[2:]) == args[1])) in (0, 2)
            if len({i, args[2], args[3], args[4]}) == 4 and args[1] <= 3 else None,
            lambda stmt, i, args:
            f"Exactly {args[1]} of the statements {args[2] + 1}, {args[3] + 1} and {args[4] + 1} {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
    ]
    second_level = [
        # "Either statement X or statement Y is true/false, but not both."
        [
            [stmt_index_arg, stmt_index_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + bool((stmt[args[0]] == args[2]) ^ (stmt[args[1]] == args[2]))) in (0, 2)
            if i != args[0] and i != args[1] and args[0] != args[1] else None,
            lambda stmt, i, args:
            f"Either statement {args[0] + 1} or statement {args[1] + 1} is {'true' if args[2] else 'false'}, but not both."
        ],
        # "Either statement X or statement Y is true/false, or both."
        [
            [stmt_index_arg, stmt_index_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[2]) or (stmt[args[1]] == args[2]))) in (0, 2)
            if i != args[0] and i != args[1] and args[0] != args[1] else None,
            lambda stmt, i, args:
            f"Either statement {args[0] + 1} or statement {args[1] + 1} is {'true' if args[2] else 'false'}, or both."
        ],
        # "Statements X and Y are either both true or both false."
        [
            [stmt_index_arg, stmt_index_arg],
            lambda stmt, i, args:
            (stmt[i] + (stmt[args[0]] == stmt[args[1]])) in (0, 2)
            if i != args[0] and i != args[1] and args[0] != args[1] else None,
            lambda stmt, i, args:
            f"Statements {args[0] + 1} and {args[1] + 1} are either both true or both false."
        ],
    ]
    third_level = [
        # "At least X of the previous/next statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:i]) >= args[1])) in (0, 2)
            if len(stmt[:i]) > args[1] else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the previous statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:]) >= args[1])) in (0, 2)
            if len(stmt[i + 1:]) > args[1] else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the next statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At most X of the previous/next statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:i]) <= args[1])) in (0, 2)
            if len(stmt[:i]) > args[1] else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the previous statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:]) <= args[1])) in (0, 2)
            if len(stmt[i + 1:]) > args[1] else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the next statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At least X of the first/last/previous/next Y statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:args[2]]) >= args[1])) in (0, 2)
            if len(stmt[:args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 and check_for_exclusive(stmt, i, slice(None, args[2])) else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the first {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[-args[2]:]) >= args[1])) in (0, 2)
            if len(stmt[-args[2]:]) == args[2] and args[2] > args[1] and args[2] > 1 and check_for_exclusive(stmt, i, slice(-args[2], None)) else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the last {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i - args[2]:i]) >= args[1])) in (0, 2)
            if len(stmt[i - args[2]:i]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the previous {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:i + 1 + args[2]]) >= args[1])) in (0, 2)
            if len(stmt[i + 1:i + 1 + args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the next {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At most X of the first/last/previous/next Y statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[:args[2]]) <= args[1])) in (0, 2)
            if len(stmt[:args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 and check_for_exclusive(stmt, i, slice(None, args[2])) else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the first {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[-args[2]:]) <= args[1])) in (0, 2)
            if len(stmt[-args[2]:]) == args[2] and args[2] > args[1] and args[2] > 1 and check_for_exclusive(stmt, i, slice(-args[2], None)) else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the last {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i - args[2]:i]) <= args[1])) in (0, 2)
            if len(stmt[i - args[2]:i]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the previous {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, number_of_stmt_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1:i + 1 + args[2]]) <= args[1])) in (0, 2)
            if len(stmt[i + 1:i + 1 + args[2]]) == args[2] and args[2] > args[1] and args[2] > 1 else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the next {args[2]} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At least X of the even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2])::2]) >= args[1])) in (0, 2)
            if len(stmt[int(args[2])::2]) >= args[1] and check_for_exclusive(stmt, i, slice(int(args[2]), None, 2)) else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At most X of the even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2])::2]) <= args[1])) in (0, 2)
            if len(stmt[int(args[2])::2]) >= args[1] and check_for_exclusive(stmt, i, slice(int(args[2]), None, 2)) else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At least X of the previous/next even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2]):i:2]) >= args[1])) in (0, 2)
            if len(stmt[int(args[2]):i:2]) > args[1] else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the previous {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1 + ((i % 2) == args[2])::2]) >= args[1])) in (0, 2)
            if len(stmt[i + 1 + ((i % 2) == args[2])::2]) > args[1] else None,
            lambda stmt, i, args:
            f"At least {args[1]} of the next {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        # "At most X of the previous/next even/odd statements is/are true/false."
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[int(args[2]):i:2]) <= args[1])) in (0, 2)
            if len(stmt[int(args[2]):i:2]) > args[1] else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the previous {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
        [
            [false_true_arg, number_of_stmt_arg, even_odd_arg],
            lambda stmt, i, args:
            (stmt[i] + (sum(bool(x) == args[0] for x in stmt[i + 1 + ((i % 2) == args[2])::2]) <= args[1])) in (0, 2)
            if len(stmt[i + 1 + ((i % 2) == args[2])::2]) > args[1] else None,
            lambda stmt, i, args:
            f"At most {args[1]} of the next {'even' if args[2] else 'odd'} statements {'are' if args[1] > 1 else 'is'} {'true' if args[0] else 'false'}."
        ],
    ]
    fourth_level = [
        # "If statement X is true/false, then statement Y is true/false (sufficient)."
        [
            [stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[2]) <= (stmt[args[1]] == args[3]))) in (0, 2)
            if len({i, args[0], args[1]}) == 3 and args[1] != 0 else None,
            lambda stmt, i, args:
            f"If statement {args[0] + 1} is {'true' if args[2] else 'false'}, then statement {args[1] + 1} is {'true' if args[3] else 'false'} (sufficient)."
        ],
        # "Only if statement X is true/false, then statement Y is true/false (necessary)."
        [
            [stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[2]) >= (stmt[args[1]] == args[3]))) in (0, 2)
            if len({i, args[0], args[1]}) == 3 and args[1] != 0 else None,
            lambda stmt, i, args:
            f"Only if statement {args[0] + 1} is {'true' if args[2] else 'false'}, then statement {args[1] + 1} is {'true' if args[3] else 'false'} (necessary)."
        ],
        # "If and only if statement X is true/false, then statement Y is true/false (sufficient and necessary)."
        [
            [stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[2]) == (stmt[args[1]] == args[3]))) in (0, 2)
            if len({i, args[0], args[1]}) == 3 and args[1] != 0 else None,
            lambda stmt, i, args:
            f"If and only if statement {args[0] + 1} is {'true' if args[2] else 'false'}, then statement {args[1] + 1} is {'true' if args[3] else 'false'} (sufficient and necessary)."
        ],
    ]
    fifth_level = [
        # "If statement X is true/false, then statements Y and Z are both true/false (sufficient)."
        [
            [stmt_index_arg, stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[3]) <= (
                    (stmt[args[1]] == args[4]) and (stmt[args[2]] == args[4])))) in (0, 2)
            if len({i, args[0], args[1], args[2]}) == 4 and args[1] != 0 and args[2] != 0 else None,
            lambda stmt, i, args:
            f"If statement {args[0] + 1} is {'true' if args[3] else 'false'}, then statements {args[1] + 1} and {args[2] + 1} are both {'true' if args[4] else 'false'} (sufficient)."
        ],
        # "Only if statement X is true/false, then statements Y and Z are both true/false (necessary)."
        [
            [stmt_index_arg, stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[3]) >= (
                    (stmt[args[1]] == args[4]) and (stmt[args[2]] == args[4])))) in (0, 2)
            if len({i, args[0], args[1], args[2]}) == 4 and args[1] != 0 and args[2] != 0 else None,
            lambda stmt, i, args:
            f"Only if statement {args[0] + 1} is {'true' if args[3] else 'false'}, then statements {args[1] + 1} and {args[2] + 1} are both {'true' if args[4] else 'false'} (necessary)."
        ],
        # "If and only if statement X is true/false, then statements Y and Z are both true/false (sufficient and necessary)."
        [
            [stmt_index_arg, stmt_index_arg, stmt_index_arg, false_true_arg, false_true_arg],
            lambda stmt, i, args:
            (stmt[i] + ((stmt[args[0]] == args[3]) == (
                    (stmt[args[1]] == args[4]) and (stmt[args[2]] == args[4])))) in (0, 2)
            if len({i, args[0], args[1], args[2]}) == 4 and args[1] != 0 and args[2] != 0 else None,
            lambda stmt, i, args:
            f"If and only if statement {args[0] + 1} is {'true' if args[3] else 'false'}, then statements {args[1] + 1} and {args[2] + 1} are both {'true' if args[4] else 'false'} (sufficient and necessary)."
        ],
    ]
    stmt_conditions = []
    stmt_conditions.extend(first_level)
    if level >= 2:
        stmt_conditions.extend(second_level)
    if level >= 3:
        stmt_conditions.extend(third_level)
    if level >= 4:
        stmt_conditions.extend(fourth_level)
    if level >= 5:
        stmt_conditions.extend(fifth_level)
    if level >= 6:
        stmt_conditions = stmt_conditions[len(first_level):]
    if level >= 7:
        stmt_conditions = stmt_conditions[len(second_level):]
    if level >= 8:
        stmt_conditions = stmt_conditions[len(third_level):]
    products = list(itertools.product(*[(False, True)] * number_of_statements))
    args_list = []
    for args, check_function, format_function in stmt_conditions:
        all_args = []
        for arg in args:
            if arg == false_true_arg or arg == even_odd_arg:
                all_args = [x + [y] for x in all_args for y in (False, True)] \
                    if all_args else [[False], [True]]
            elif arg == number_of_stmt_arg or arg == stmt_index_arg:
                k = int(arg == number_of_stmt_arg)
                all_args = [x + [y] for x in all_args for y in range(k, number_of_statements)] \
                    if all_args else [[x] for x in range(k, number_of_statements)]
        if not all_args:
            all_args = [[]]
        random.shuffle(all_args)
        args_list.append((all_args[:100], check_function, format_function))
    fail = True
    while fail:
        statements_values = []
        while not statements_values or not any(statements_values) or all(statements_values):
            statements_values = [random.choice([False, True]) for _ in range(1, number_of_statements)]
        statements_values = [True] + statements_values
        stmt_variants = [first_condition]
        for i in range(1, number_of_statements):
            variants = []
            for all_args, check_function, format_function in args_list:
                for args in all_args:
                    r = check_function(statements_values, i, args)
                    if r is True:
                        variants.append((format_function(statements_values, i, args), args, check_function))
            if variants:
                random.shuffle(variants)
                stmt_variants.append(variants[:2])
                continue
            stmt_variants = []
            break
        if stmt_variants:
            d = dict()
            for stmt_index, variants in enumerate(stmt_variants):
                for string, args, check_function in variants:
                    products_indices = []
                    for i, prod in enumerate(products):
                        r = check_function(prod, stmt_index, args)
                        if r is True:
                            products_indices.append(i)
                    if products_indices:
                        d.setdefault(stmt_index, dict()).setdefault(string, set()).update(products_indices)
                if stmt_index not in d:
                    break
            if len(d) < number_of_statements:
                continue
            for product_spi in itertools.product(*[list(spi.items()) for spi in d.values()]):
                product_pis = product_spi[0][1].copy()
                for _, p_pi in product_spi[1:]:
                    product_pis.intersection_update(p_pi)
                    if len(product_pis) == 0:
                        break
                if len(product_pis) == 0 or len(product_pis) > max_solutions:
                    continue
                false_check = False
                for pis in product_pis:
                    if not products[pis][0]:
                        false_check = True
                        break
                if false_check:
                    continue
                fail = False
                stmt_values = [products[pis] for pis in product_pis]
                statements = [t[0] for t in product_spi]
                break

    return stmt_values, statements


def main():
    t1 = time.monotonic()
    solutions, statements = generate_recursive_puzzle(number_of_statements=12, level=5, max_solutions=1)
    t2 = time.monotonic()
    indent = len(str(len(statements)))
    print('Statements:')
    for i, statement in enumerate(statements, 1):
        i = str(i).rjust(indent)
        print(f"{i}. {statement}")
    print('Solutions:')
    for i, solution in enumerate(solutions, 1):
        i = str(i).rjust(indent)
        print(', '.join(f"{i}-{x}" for i, x in enumerate(solution, 1)))
    print(f'Time: {t2 - t1:.6f} seconds')


if __name__ == "__main__":
    main()
