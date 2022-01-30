import main

with open('legal.txt') as f:
    words = f.readlines()
    words = [i.replace('\n', '') for i in words]

gray = 'gray'
yellow = 'yellow'
green = 'green'

total_loses = 0
total_turns = 0
total_words = len(words)

def test_word(answer, guess):
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

    return colors


def game_over(colors, turn):
    global total_loses, total_turns

    if all(i == green for i in colors):
        total_turns += turn
        print('passed in', turn)
        return True
    elif turn == 6:
        total_loses += 1
        print('failed')
        return True

    return False


def test():
    for word in words:
        main.invalid_letters.clear()
        main.greens = ['-' for i in range(main.length)]
        main.columns = [[] for i in range(main.length)]
        remaining_answers = main.words
        recommended_guesses = []

        for turn in range(1, 7):
            if turn == 1:
                guess = 'later'
                colors = test_word(answer=word, guess=guess)
            else:
                if not recommended_guesses:
                    print('fail', remaining_answers)
                    break
                guess = recommended_guesses[0]
                colors = test_word(answer=word, guess=guess)
            if game_over(colors, turn):
                break

            grays = ''.join(main.invalid_letters)
            yellows = ''
            greens = ''
            for index, char in enumerate(guess):
                if colors[index] == gray:
                    grays += char
                yellows += char if colors[index] == yellow else '-'
                greens += char if colors[index] == green else '-'

            main.get_user_input(grays, yellows, greens)
            recommended_guesses, remaining_answers = main.check(remaining_answers)



if __name__ == '__main__':
    test()
    print('Fail %:', round(total_loses / total_words, 2))
    print('Average turns:', total_turns / total_words)
