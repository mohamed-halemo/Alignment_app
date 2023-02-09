from collections import Counter
from math import log


# def _mutual_information(sequences, i, j):
#     sequences = [s for s in sequences if not '-' in [s[i], s[j]]]
#     p_i = Counter(sequence[i] for sequence in sequences)
#     p_j = Counter(sequence[j] for sequence in sequences)
#     p_ij = Counter((sequence[i], sequence[j]) for sequence in sequences)
#     return sum(p_ij[(x, y)]*log(p_ij[(x, y)]/(p_i[x]*p_j[y])) for x, y in p_ij)


def _entropy(sequences):
    for i in range(len(sequences[0])):    
        column = [sequence[i] for sequence in sequences]
        word_frq = [column.count(w)/len(column) for w in column]
        column_chars_and_freqs = dict(zip(column, word_frq))
        current_entropy = 0
        for key, value in column_chars_and_freqs.items():
            current_entropy += value * log(value, 2)
    return current_entropy


def _sum_of_pairs(pairs):
    sum_of_pairs = 0
    for i in range(len(pairs)):
        if i == (len(pairs)-1):
            break
        for j in range(i+1, len(pairs)):

            for k in range(len(pairs[0])):
                if pairs[i][k] == '-' and pairs[j][k] == '-':
                    sum_of_pairs = sum_of_pairs
                elif pairs[i][k] == pairs[j][k]:
                    sum_of_pairs += 1
                elif pairs[i][k] == '-' and pairs[j][k] != '-':
                    sum_of_pairs -= 2
                elif pairs[i][k] != '-' and pairs[j][k] == '-':
                    sum_of_pairs -= 2
                elif pairs[i][k] != pairs[j][k]:
                    sum_of_pairs -= 1

    return sum_of_pairs


def _percentage_of_no_gaps(sequences):
    final_score = 0
    for k in range(len(sequences[0])):
        column = [sequence[k] for sequence in sequences]
        score = column.count('-')
        final_score += score
    return 100 - (final_score / (len(sequences) * len(sequences[0])) * 100)


def calculate_metrices(sequences):
    entropy = 0
    for k in range(len(sequences)):
        entropy += _entropy(sequences)
    entropy = entropy / len(sequences)
    return entropy, _sum_of_pairs(sequences), _percentage_of_no_gaps(sequences)
