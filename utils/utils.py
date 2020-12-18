def get_meaning_text(result: dict):
    meaning_string = [
        f'*{result["word"][0].upper()}{result["word"][1:]}*\n',
        f'Pronunciation: _{result["phonetics"]}_\n',
    ]

    # Adding the synonyms to the list
    synonyms = result["synonyms"]
    if len(synonyms) != 0:
        meaning_string.append(
            f'Synonyms: _{", ".join(synonyms)}_\n'
        )

    # Adding the meanings to the list
    meanings_list = result["meanings"]
    for meaning in meanings_list:
        for key, value in meaning.items():
            # Adding meanings
            meanings = value['meanings']
            meanings = [
                str(meanings.index(meaning) + 1) +
                '\. ' +
                replace_special_characters(meaning) + '\n'
                for meaning in meanings
            ]
            meaning_string.append(
                f'*{key}*\n\n{"".join(meanings)}\n'
            )

            # Adding Example
            example = replace_special_characters(value['example'])
            if example != 'None':
                meaning_string.append(
                    f'Example: _{example}_\n'
                )

    return meaning_string


def replace_special_characters(meaning: str):
    special_characters = [
        '+',
        '-',
        '.',
        '(',
        ')',
        '*',
    ]
    for char in special_characters:
        meaning = meaning.replace(char, f'\{char}')
    return meaning
