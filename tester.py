gray = 'gray'
yellow = 'yellow'
green = 'green'

def test_word(answer, guess):
    turn = 1
    if turn > 6:
        print('fail')

    colors = [gray for i in range(5)]
    letters = list(answer)
    for index, char in enumerate(guess):
        if char not in letters:
            colors[index] = gray

        elif char in letters and answer[index] != char:
            colors[index] = yellow
            letters.remove(char)

        elif char in letters and answer[index] == char:
            colors[index] = green
            letters.remove(char)

    print('guess', guess)
    print(list(answer))
    print(colors)


def main():
    with open('legal.txt') as f:
        words = f.readlines()
        words = [i.replace('\n', '') for i in words]

    total_turns = 0
    total_words = len(words)

    test_word(answer='smith', guess='house')

if __name__ == '__main__':
    main()
