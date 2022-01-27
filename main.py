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

invalid_letters = []
greens = ['-' for i in range(length)]
columns = [[] for i in range(length)]
alphabet = 'abcdefghijklmnopqrstuvwxyz'


def next_word():
    remaining_letters = [i for i in alphabet if i not in invalid_letters and i not in greens]
    combos = get_combos(''.join(remaining_letters))
    combos = [i for i in combos if i[1] == length]
    if not combos:
        r = [i for i in alphabet if i not in greens]
        combos = get_combos(''.join(r))
        combos = [i for i in combos if i[1] == length]

    combos = [i[0] for i in combos]
    ranked = []
    for combo in combos:
        score = sum(char in remaining_letters for char in combo)
        ranked.append((combo, score))
    ranked = sorted(ranked, key=lambda i: i[1])  # worst to best
    top = [i[0] for i in ranked[-5:]]
    print(f'Recommended next moves: {", ".join(top)}')


def check():
    global invalid_letters
    reduced_list = []

    print()
    invalid_letters.extend(list(input('Gray in row     (Ex:abc): ').lower()))
    invalid_letters = list(set(invalid_letters))

    yellows = input('Orange in row (Ex:-ab--): ').lower()
    if yellows:
        for index, i in enumerate(yellows):
            if i in alphabet:
                columns[index].append(i)
            columns[index] = list(set(columns[index]))

    row_greens = input('Greens in row (Ex:a---b): ').lower()
    if row_greens:
        for index, i in enumerate(row_greens):
            if i in alphabet:
                greens[index] = i

    # must haves are all yellow tiles
    must_haves = []
    for col in columns:
        for i in col:
            must_haves.append(i)

    # invalid word check and must have check
    for word in words:
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
    max_list = 100
    reduced_list = list(set(reduced_list))
    reduced_list = reduced_list[:max_list] if len(reduced_list) > max_list else reduced_list
    print('\n' * 3 + '-' * 100)
    print(f'All possible answers ({len(reduced_list)}{"+" if len(reduced_list) == max_list else ""}):',
          ', '.join(reduced_list))
    next_word()
    check()


print('Word Length:', length)
check()
