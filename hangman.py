#################################################################
# FILE : hangman.py
# WRITER : Noor Khamaisy , noor.khamaisy , 212809925
# EXERCISE : intro2cs2 ex2 2022
# DESCRIPTION: The hangman game

#################################################################


from hangman_helper import *


# part A :
def update_word_pattern(word, pattern, letter):
    ## function that returns an updated pattern
    l = []
    p = []
    for j in word:
        l.append(j)
    for i in pattern:
        p.append(i)
    for s in range(len(l)):
        if l[s] == letter:
            p[s] = letter
    x = ''
    for m in range(len(p)):
        x = x + p[m]
    return x


def run_single_game(words_list, score):
    # function that runs a single game and returns the player's score
    word = get_random_word(words_list)
    pattern = '_' * len(word)
    wrong_guesses = []
    msg = "Starting the game."
    while True:
        display_state(pattern, wrong_guesses, score, msg)
        msg = ''
        choice, guess_value = get_input()
        if choice == LETTER:
            if len(guess_value) > 1 or not (guess_value.islower() and guess_value.isalpha()):
                msg = 'The value is not valid'
                continue
            if guess_value in wrong_guesses or guess_value in pattern:
                msg = 'The letter is already taken'
                continue
            score = score - 1
            occour = word.count(guess_value)
            if occour > 0:
                pattern = update_word_pattern(word, pattern, guess_value)
                score = score + (occour * (occour + 1)) // 2
            else:
                wrong_guesses.append(guess_value)
        elif choice == WORD:
            score = score - 1
            if guess_value == word:
                chars = pattern.count('_')
                score = score + ((chars) * (chars + 1)) // 2
                pattern = word
        elif choice == HINT:
            score = score - 1
            new_filtered = filter_words_list(words_list, pattern, wrong_guesses)
            filtered_length = len(new_filtered)
            if filtered_length > HINT_LENGTH:
                new_filtered = [new_filtered[(i * filtered_length) // HINT_LENGTH] for i in range(HINT_LENGTH)]
            show_suggestions(new_filtered)

        if word == pattern:
            msg = 'congratulations , you guessed it'
            break
        if score == 0:
            msg = 'Game over,you lost.The word is:' + word
            break
    display_state(pattern, wrong_guesses, score, msg)
    return score


def main():
    # function that lets the player play full game and enable him to play again
    rounds = 1
    words_list = load_words()
    points = run_single_game(words_list, POINTS_INITIAL)
    while True:
        if points > 0:
            message = 'Rounds played: {} | your current score: {}\n'.format(rounds, points)
            playingagain = play_again(message + 'Wanna play more ?')
            if playingagain:
                points = run_single_game(words_list, points)
                rounds = rounds + 1
            else:
                break
        else:
            message = 'Survived Rounds : {} | your current score: {}\n'.format(rounds, points)
            playingagain = play_again(message + 'Do you want to start a new game?')
            if playingagain:
                points = run_single_game(words_list, POINTS_INITIAL)
                rounds = 1
            else:
                break


# part b
def filter_words_list(words, pattern, wrong_guess_lst):
    # function that builds a new words list that contains the correct word
    new_words = []
    for word in words:
        if len(word) != len(pattern):
            continue
        good_word = True
        for char in range(len(word)):
            if pattern[char] != '_' and pattern[char] != word[char]:
                good_word = False
            if word[char] in wrong_guess_lst:
                good_word = False
            if pattern[char] == '_' and word[char] in pattern:
                good_word = False
        if good_word:
            new_words.append(word)

    return new_words


if __name__ == "__main__":
    main()
