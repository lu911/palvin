# -*- coding:utf-8 -*-


def camel_case_to_lower_case_underscore(string):
    """
    Split string by upper case letters.

    F.e. useful to convert camel case strings to underscore separated ones.

    @return words (list)
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(string):
        if char.isupper() and from_char_position < current_char_position:
            words.append(
                string[from_char_position:current_char_position].lower()
            )
            from_char_position = current_char_position
    words.append(string[from_char_position:].lower())
    return '_'.join(words)
