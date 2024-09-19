def get_last_valid_letter(word):
    word = word.upper()
    if not word:
        return None

    invalid_letters = ('Ь', 'Ъ', 'Й', 'Ы')
    for letter in reversed(word):
        if letter not in invalid_letters:
            return letter

    return None
