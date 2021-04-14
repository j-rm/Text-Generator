import string, os, json
from typing import TextIO

def get_texts(book: TextIO) -> list:
    """Returns a list of all 970 characters long texts from the given book file."""
    content = book.read()
    chars_limit = 970
    texts = [content[i:i + chars_limit] for i in range(0, len(content), chars_limit)]
    return ["..." + t + "..." if t != texts[0] else t + "..." for t in texts]

def remove_punctuation(word: str) -> str:
    "Removes any leading spaces or punctuation from the given word."
    return word.strip().strip(string.punctuation)

def word_frequencies(word_list: TextIO) -> dict:
    """Returns a dictionary where each key-value pair is a word and its frequency in frequency list of words.  """
    words = word_list.read().split(' ')
    amount_of_words = len(set(words))
    frequencies = {}
    for index, word in enumerate(words):
        clean_word = remove_punctuation(word)
        if clean_word not in frequencies:
            frequencies[clean_word] = (index + 1) / amount_of_words
    del frequencies[""]
    return frequencies

def frequency(w: str) -> float:
    """Returns the frequency of the given word by looking it up in the dictionary of words and their frequencies, frequency_list"""
    return frequency_list.get(remove_punctuation(w), 0)

def complexity(text:str) -> float:
    """Returns the complexity of the given text by adding up the frequencies of all its words."""
    words = text.split(' ')
    freqs = [frequency(w) for w in words]
    return sum(freqs) / (len(frequency_list) - freqs.count(0))  #sum of the frequencies / all the words that were in the list

def difficulty(score: float) -> str:
    """Returns the difficulty category of score. It can be one of: Easy, Medium or Hard."""
    if score <= 0.000055:
        return "Easy"
    elif score <= 0.000099:
        return "Medium"
    else:
        return "Hard"

def keywords(text:str) -> list:
    """Returns a list of 5 keywords from the given text."""
    return sorted(set(text.split(' ')), key=frequency, reverse=True)[0:5]

def coverage(text: str) -> float:
    """Returns the percentage of (unique) words from the given text that are in the frequency list."""
    words = set(text.split(' '))
    return len([w for w in words if frequency(w) != 0]) / len(words) * 100

def categorize(book: TextIO) -> list:
    """Returns a list with all the 100 words long texts from the given book along with their difficulties and keywords."""
    chunks = get_texts(book)
    texts = []
    for t in chunks:
        level = difficulty(complexity(t))
        texts.append((t, level, keywords(t)))
    return texts

def save_frequencies(freqs: dict) -> None:
    """Stores the given frequency list in a file ('freq_list')."""
    with open("freq_list", 'w') as stored_freq_list:
        json.dump(freqs, stored_freq_list)

def load_frequencies() -> dict:
    """Loads the frequency list stored in a file ('freq_list') and returns it."""
    with open("freq_list", 'r') as stored_freq_list:
        return json.load(stored_freq_list)

with open("final_version_words.txt", 'r') as word_list, open("book.txt", 'r', encoding='utf-8') as book:
    if os.path.exists("freq_list"):
        frequency_list = load_frequencies()
    else:
        frequency_list = word_frequencies(word_list)
        save_frequencies(frequency_list)
    texts = categorize(book)

with open("final_texts.txt", 'w', encoding='utf-8') as final_texts:
    for t in texts:
        text, level, kwords = t[0], t[1], ", ".join([remove_punctuation(w) for w in t[2]])
        final_texts.write("%s level.\nKeywords: %s\n%s\n" % (level, kwords, text))
        final_texts.write("--------------------------------------------------------------------------\n")