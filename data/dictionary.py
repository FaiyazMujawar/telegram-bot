import requests
from bs4 import BeautifulSoup
from requests.models import HTTPError


def search_meaninig(word: str):
    """ Searches the given word from Lexico Dictionary """

    URL = f'https://www.lexico.com/definition/{word}'

    response = None
    try:
        # Getting the HTML page for the word
        response = requests.get(URL, allow_redirects=True)
    except HTTPError:
        # If any error occurs getting the page, throw an error
        raise Exception('Sorry! A fatal error occured with the server.')

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        try:
            # Get the headword
            soup.find('span', class_='hw').text
        except AttributeError:
            del soup
            raise ValueError('No word found')

        # Get phonetic pronunciation
        pronunciation = soup.find('span', class_='phoneticspelling').text

        # Get pronunciation audio
        pronunciation_audio = soup.find('a', class_='speaker').audio['src']

        # Get synonyms
        synonyms = soup.find(class_='synonyms')
        if synonyms is not None:
            synonyms = synonyms.find(class_='exg').div.text.split(', ')[:3]
        else:
            synonyms = []

        result = {
            "word": word,
            "phonetics": pronunciation,
            "synonyms": synonyms,
            "audio": pronunciation_audio
        }

        # List of meanings
        meanings_list = []

        sections = soup.find_all('section', class_='gramb')
        for section in sections:

            # Get the part of speech
            part_of_speech = section.find('span', class_='pos').text

            # Get the meaning
            meanings = [
                meaning.text for meaning in section.find_all(
                    'span', class_='ind'
                )][:3]

            # Get an example
            example = None
            try:
                example = section.find('div', class_='ex').em.text
            except:
                example = "None"

            meanings_list.append({
                part_of_speech: {
                    "meanings": meanings,
                    "example": example
                }
            })

        result["meanings"] = meanings_list

        del soup

        return result

    else:
        raise Exception('An error occured!')
