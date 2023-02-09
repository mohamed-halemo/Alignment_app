import numpy as np

directions = {"_": "not in optimal path",
              "D": np.array([-1, -1]),
              "H": np.array([-1, 0]),
              "V": np.array([0, -1]),
              "0": np.array([-1, -1])
              }


def _init_mat(seq1, seq2, alignment, gap):
    value = np.empty((), dtype=object)
    value[()] = [0, 0]  # change from tuple to list to be mutable
    mat = np.full((len(seq1)+1, len(seq2)+1), value, dtype=object)
    mat[0][0] = [0, 0]
    if alignment == 'global':
        for i in range(1, mat.shape[1]):
            mat[0][i] = [gap*i, 0]
        for i in range(1, mat.shape[0]):
            mat[i][0] = [gap*i, 0]
    return mat


def _calc_score(seq1, seq2, gap, matching, mismatching):
    score = 0
    for i in range(len(seq1)):
        if seq1[i] == seq2[i]:
            score += matching
        elif seq1[i] == '-' or seq2[i] == '-':
            score += gap
        else:
            score += mismatching
    return score


def _fill_mat(mat, seq1, seq2, alignment, gap, matching, mismatching):

    max_val = 0
    max_x = 0
    max_y = 0
    for j in range(1, mat.shape[1]):  # seq2
        for i in range(1, mat.shape[0]):  # seq1
            if seq1[i-1] == seq2[j-1]:
                val = matching
            else:
                val = mismatching
            result = [
                mat[i-1][j-1][0] + val,  # diagonal
                mat[i-1][j][0] + gap,  # horizontal
                mat[i][j-1][0] + gap  # vertical
            ]
            final_result = (max(0, np.max(result)) if alignment == 'local' else np.max(result))
            # if alignment == 'local':
            # for r in result:
            #     if r == final_result:
            #         if r == 0:
            #             pass
            #         else:
            #             c += 1
            if final_result >= max_val:
                max_val = final_result
                max_x = i
                max_y = j
            # if c > 1:
            #     ds = []
            #     result.sort(reverse=True)
            #     dirs = result[:c]
            #     ddd = 0
            #     for d in dirs:
            #         if d == result[ddd]:
            #             ds.append(list(directions)[ddd + 1])
            #         ddd += 1
            #     mat[i][j] = [final_result, ds]
            #
            # else:
            mat[i][j] = [final_result, list(directions)[np.argmax(result) + 1]]  # list(direction) to access a dict key
    return mat, ((max_val, max_x, max_y) if alignment == 'local' else None)


def _traceback(mat, seq, seq2, dictionary, alignment, start=None):
    sequence1 = ''
    sequence2 = ''
    x = ((mat.shape[0] - 2) if alignment == 'global' else start[1]-1)
    y = ((mat.shape[1] - 2) if alignment == 'global' else start[2]-1)

    while (x >= 0 and y >= 0) if alignment == 'global' else mat[x, y][0] > 0:
        direction = (mat[x+1][y+1][1] if alignment == 'global' else mat[x+1, y+1][1])
        if direction != 'D':
            if direction == 'V':
                sequence1 += '-'
                sequence2 += seq2[y]
            elif direction == 'H':
                sequence2 += "-"
                sequence1 += seq[x]
        else:
            sequence1 += seq[x]
            sequence2 += seq2[y]
        # if len(direction) > 1:
        #     alignments = []
        #     for d in direction:
        #         x1 = x
        #         y1 = y
        #         s1 = ''
        #         s2 = ''
        #         while (x1 >= 0 and y1 >= 0) if alignment == 'global' else mat[x1+1, y1+1][0] > 0:
        #             d = (mat[x1 + 1][y1 + 1][1] if alignment == 'global' else mat[x1 + 1, y1 + 1][1])
        #
        #             if d != 'D':
        #                 if d == 'V':
        #                     s1 += '-'
        #                     s2 += seq2[y1]
        #                 elif d == 'H':
        #                     s2 += "-"
        #                     s1 += seq[x1]
        #             else:
        #                 s1 += seq[x1]
        #                 s2 += seq2[y1]
        #             x1 = np.add(dictionary[f'{d}'][0], x1)
        #             y1 = np.add(dictionary[f'{d}'][1], y1)
        #         if alignment == 'local':
        #             s1 += seq[x1]
        #             s2 += seq2[y1]
        #         score = _calc_score(sequence1+s1, sequence2+s2, -2, 2, -1)
        #         alignments.append((s1[::-1], s2[::-1], score, x1, y1, d))
        #     max_score = 0
        #     for a in alignments:
        #         score = a[2]
        #         if score > max_score:
        #             max_score = score
        #             sequence1 = a[0]
        #             sequence2 = a[1]
        #             direction = a[5]

        x = np.add(dictionary[f'{direction}'][0], x)
        y = np.add(dictionary[f'{direction}'][1], y)
        # try:
        #     print(max_score)
        # except:
        #     pass
    if alignment == 'local':
        sequence1 += seq[x]
        sequence2 += seq2[y]
    return sequence1[::-1], sequence2[::-1]


def pairwise_alignment(seq1, seq2, alignment, gap, matching, mismatching):

    mat = _init_mat(seq1, seq2, alignment, gap)
    mat, start = _fill_mat(mat, seq1, seq2, alignment, gap, matching, mismatching)
    seq1, seq2 = _traceback(mat, seq1, seq2, directions, alignment, start)
    score = _calc_score(seq1, seq2, gap, matching, mismatching)
    return (seq1, seq2), score
