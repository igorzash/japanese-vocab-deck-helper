import requests


with open('data.txt') as datafile:
    data = datafile.readlines()
    data = map(lambda x: x.split(), data)
    data = map(lambda x: (x[0], int(x[1])), data)
    data = {x[0]: x[1] for x in data}


with open('words.txt') as wordsfile:
    words = map(lambda x: x.strip(), wordsfile.readlines())
    words = list(words)
    words.sort(key=lambda x: -data[x] if x in data else 0)


del data


def build_http_string(kw):
    return 'https://jisho.org/api/v1/search/words?keyword=' + kw


with open('output.tsv', 'w') as outputfile:
    for i, word in enumerate(words):
        r = requests.get(build_http_string(word))
        
        word_data = r.json()['data'][0]

        reading = word_data['japanese'][0]['reading']
        meanings = '; '.join(word_data['senses'][0]['english_definitions'])

        kana_alone = 'Usually written using kana alone' in word_data['senses'][0]['tags']

        exp = reading if kana_alone else word

        outputfile.write(f"{exp}\t{reading}\t{meanings}\n")
        print(i + 1)

