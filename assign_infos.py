"""
DOCUMENTATION DE SPACY:
https://spacy.io/usage/linguistic-features

SETUP:
1. pip3 install spacy
2. python -m spacy download fr_core_news_sm
3. import spacy
4. nlp = spacy.load("fr_core_news_sm")

"""
import spacy
nlp = spacy.load("fr_core_news_sm")  # loader un corpus (small) de textes et nouvelles en francais

# pour output dans le fichier texte
from contextlib import redirect_stdout

INPUT_PATH = "paires-Lareau.txt"
OUTPUT_PATH = "words_assigned.txt"

class WordsClassified:
    class Word:
        def __init__(self, mot_masc, mot_fem):
            self.word_masc = mot_masc
            self.word_fem = mot_fem

        def set_info(self, pos, lemma, tag, dep):
            """
            Add further classifications for word from spacy
            :param pos: .pos_
            :param lemma: .lemma_
            :param tag: .tag_
            :param dep: .dep_
            """
            self.pos = pos
            self.lemma = lemma
            self.tag = tag
            self.dep = dep
            # TODO: check if there aren't more important ones to add

        def __str__(self):
            return self.word_masc + ", " + self.word_fem

        def print(self):
            print(self.__str__() + "\t" + " " * (40 - len(self.__str__())) +
                  self.pos + "\t" + " " * (10 - len(self.pos)) +
                  self.lemma + "\t" + " " * (25 - len(self.lemma)) +
                  self.tag + "\t" + " " * (10 - len(self.tag)) +
                  self.dep)

    def __init__(self, words_raw: [[str]]):
        """
        Takes in input a list of male/female pairs.
        :param words_raw:
        """
        self.words = [self.Word(word[0], word[1]) for word in words_raw]
        self.classified_words = self.classify()

    def classify(self):
        """
        Use spaCy to give different info about a specific word
        :return:
        """
        return [nlp(word.word_masc)[0] for word in self.words]

    def output(self):
        def print_header():
            names = ["Word (M/F)", "POS", "LEMMA", "TAG", "DEPENDENCY"]
            cell_widths = [43, 15, 25, 10, 10]
            header = ""
            for word_idx in range(len(names)):
                header += names[word_idx] + " " * (cell_widths[word_idx] - len(names[word_idx]))
            print(header)

        print_header()
        for idx in range(len(self.classified_words)):
            classified_word = self.classified_words[idx]
            self.words[idx].set_info(
                classified_word.pos_,
                classified_word.lemma_,
                classified_word.tag_,
                classified_word.dep_)
            self.words[idx].print()

    def print(self, is_external_print=False):
        """
        Prints to file OR to IDE
        :param is_external_print: if True, then will output to the file specified under OUTPUT_PATH
        """
        if is_external_print:
            with open(OUTPUT_PATH, 'w') as f:
                with redirect_stdout(f):
                    self.output()

        else:
            self.output()


def main():
    lines = open(INPUT_PATH, "r", encoding="utf-8").read().splitlines()
    words = WordsClassified([line.split("\t") for line in lines])

    # Mettre ceci a True si on veut output le tableau dans un fichier txt
    is_external_print = True

    words.print(is_external_print)




if __name__ == '__main__':
    main()
