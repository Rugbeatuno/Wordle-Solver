from unscrambler import get_combos

'''
This is a very poorly written program.
It is designed to narrow down possible guesses in the game Wordle

How to use: 
1) run the main.py
2) play any starting 5 letter word 
3) enter all gray letters in the row without spaces
4) enter all orange letters, use "-" as placeholders for gray or green letters Ex: --a--
5) then do the same for green letters, apply same format as orange (step 4)
* Press Enter to skip any steps from 3-5
'''

length = input('Enter word length(default=5): ') or 5
length = int(length)
with open('scrabble_words.txt', 'r') as f:
    words = f.readlines()
    words = [i.replace('\n', '') for i in words]
    words = [i for i in words if len(i) == length]

with open('legal.txt', 'r') as f:
    legal = f.readlines()
    legal = [i.replace('\n', '') for i in legal]

invalid_letters = []
greens = ['-' for i in range(length)]
columns = [[] for i in range(length)]
next_moves_ = []
alphabet = 'abcdefghijklmnopqrstuvwxyz'


# def next_word(possible_words):
#
#
#     remaining_letters = [i for i in alphabet if i not in invalid_letters and i not in greens]
#     combos = get_combos(''.join(remaining_letters))
#     combos = [i for i in combos if i[1] == length]
#     if not combos:
#         r = [i for i in alphabet if i not in greens]
#         combos = get_combos(''.join(r))
#         combos = [i for i in combos if i[1] == length]
#
#     combos = [i[0] for i in combos]
#     ranked = []
#     for combo in combos:
#         score = sum(char in remaining_letters for char in combo)
#         ranked.append((combo, score))
#
#     # ranked = add_weighted(possible_words, ranked)
#     ranked = sorted(ranked, key=lambda i: i[1])  # worst to best
#     top = [i[0] for i in ranked[-5:]]
#     print(f'Recommended next moves: {", ".join(top)}')
#



def next_move(possible_words):
    global next_moves_

    indexes = []
    for index in range(length):
        index_letter_occurrences = {}
        for word in possible_words:
            char = word[index]
            if char not in index_letter_occurrences:
                index_letter_occurrences[char] = 0
            index_letter_occurrences[char] += 1

        occurrences = sorted(list(index_letter_occurrences.items()), key=lambda i: i[1])
        indexes.append(dict(occurrences))

    ranked = []
    for word in possible_words:
        score = sum(indexes[index][char] for index, char in enumerate(word))
        ranked.append((word, score))
    ranked = sorted(ranked, key=lambda i: i[1])  # worst to best
    next_moves_ = [i[0] for i in ranked[-5:]]
    if __name__ == '__main__':
        print(f'Recommended next moves: {", ".join(next_moves_)}')


def get_user_input(grays_='', yellows_='', greens_=''):
    global invalid_letters

    invalid_letters.extend(list((input('Gray in row     (Ex:abc): ').lower() if not grays_ else grays_.lower())))
    invalid_letters = list(set(invalid_letters))

    yellows = input('Orange in row (Ex:-ab--): ').lower() if not yellows_ else yellows_.lower()
    if yellows:
        for index, i in enumerate(yellows):
            if i in alphabet:
                columns[index].append(i)
            columns[index] = list(set(columns[index]))
            if i in invalid_letters:
                invalid_letters.remove(i)

    row_greens = input('Greens in row (Ex:a---b): ').lower() if not greens_ else greens_.lower()
    if row_greens:
        for index, i in enumerate(row_greens):
            if i in alphabet:
                greens[index] = i
            if i in invalid_letters:
                invalid_letters.remove(i)


def check(remaining_words):
    global invalid_letters
    reduced_list = []

    if __name__ == '__main__':
        print()
        get_user_input()

    # must haves are all yellow tiles
    must_haves = []
    for col in columns:
        for i in col:
            must_haves.append(i)

    # invalid word check and must have check
    for word in remaining_words:
        for invalid in invalid_letters:
            if invalid in word:
                break
        else:
            for char in must_haves:
                if char not in word:
                    break
            else:
                reduced_list.append(word)

    # yellow check
    survived = []
    for word in reduced_list:
        fail = False
        for col_index, col in enumerate(columns):
            for green_char in col:
                if word[col_index] == green_char:
                    fail = True
        if not fail:
            survived.append(word)
    reduced_list = survived

    # green check
    more_reductions = []
    if len(greens) == length:
        for word in reduced_list:
            for index, char in enumerate(word):
                if greens[index] not in ['-', ' ', '.', char]:
                    break
            else:
                more_reductions.append(word)
        reduced_list = more_reductions

    # output
    max_list = 30
    reduced_list = list(set(reduced_list))
    full_list = [i for i in reduced_list if i in legal]
    list_length = len(full_list)
    reduced_list = reduced_list[:max_list] if len(reduced_list) > max_list else reduced_list
    if __name__ == '__main__':
        print('\n' * 3 + '-' * 100)
        print(f'All possible answers ({list_length}):', ', '.join(reduced_list))

        next_move(full_list)
        check(full_list)
    else:
        next_move(full_list)
        return next_moves_, full_list



if __name__ == '__main__':
    print('Word Length:', length)
    check(words)
