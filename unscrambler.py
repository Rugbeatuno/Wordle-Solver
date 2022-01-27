import time

filename = "scrabble_words.txt"

starttime = time.time()

words_by_length = {i: [] for i in range(2, 30)}  # at most scrabble row/column is full at 15 + max deck of 7
spellable_words = []  # final list of spellable words
passed_words = []  # these letters will go through a recursive check
letters = []  # available letters to rearrange to make words


def hash_words_by_length():
    with open(filename, 'r') as file:  # stores all legal words in hashtable (hash=word)
        words = file.readlines()
        for word in words:
            word = word.replace('\n', '')
            words_by_length[len(word)].append(word)


def recursive_check(possible_words, current_index):
    global passed_words

    alphabetized_words = {}
    for i in possible_words:
        if current_index < len(i):
            index_as = i[current_index]
            if index_as not in alphabetized_words.keys():
                alphabetized_words[index_as] = []
            alphabetized_words[index_as].append(i)
        else:
            passed_words.append(i)

    considered_words = []
    for letter in letters:
        if letter in alphabetized_words:
            considered_words.extend(alphabetized_words[letter])

    if considered_words:
        considered_words = list(set(considered_words))
        recursive_check(considered_words, current_index + 1)
    passed_words = list(set(passed_words))


def get_legal_words(words):
    global spellable_words

    for word in words:
        chars = list(word)
        for i in letters:
            if i in chars:
                chars.remove(i)
            if not chars:
                spellable_words.append(word)

    spellable_words = list(set(spellable_words))  # removes duplicate words caused from double chars


def pre_processing():
    considered_words = []
    for i in range(2, len(letters) + 1):
        considered_words.extend(words_by_length[i])

    recursive_check(considered_words, 0)
    get_legal_words(passed_words)


def format_words_for_printing():
    global spellable_words

    word_lengths = [(word, len(word)) for word in spellable_words]
    # word_lengths.sort(key=lambda word: word[0])  # sorts alphabetically
    # word_lengths.sort(key=lambda length: length[1])  # sorts words by length
    spellable_words = word_lengths


def print_words():
    duration = round(time.time() - starttime, 2)
    if duration < 1:
        print(f"\nTotal words: {len(spellable_words)} ({round(time.time() - starttime, 2) * 100}ms)")
    else:
        print(f"\nTotal words: {len(spellable_words)} ({round(time.time() - starttime, 2)}s)")

    print('---------------')

    for index, word in enumerate(spellable_words):
        if word[1] > spellable_words[index - 1][1]:
            print('---------------')
        print(f"{word[0]}, {word[1]}")
    print('---------------')



def get_combos(chars):
    global spellable_words, letters, starttime
    letters = list(chars)
    spellable_words = []

    starttime = time.time()  # starts timer

    pre_processing()

    # print(f'Total runtime: {time.time() - starttime}')

    format_words_for_printing()  # sorts list alphabetically and by length
    # display_words()  # prints words

    # reset()
    return spellable_words


hash_words_by_length()

if __name__ == '__main__':
    print(get_combos('oxyphenbutadsneosdzone'))
