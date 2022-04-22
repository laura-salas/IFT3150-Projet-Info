from translate import Translator
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')

translator = Translator(from_lang='fr', to_lang='en')
nlp.add_pipe('spacytextblob')


def translate(sentence: str) -> str:
    return translator.translate(sentence)


def translate_and_get_sentiment(sentence) -> tuple:
    """
    Translates the sentence to English and gets the sentiment analysis of it
    :param sentence: the sentence to analyze
    :return: a tuple with:
         1. polarity  a float within the range [-1.0, 1.0].
         2. subjectivity a float within the range [0.0, 1.0]
    where 0.0 is very objective and 1.0 is very subjective.
         3. sentiment analysis assessment a list of polarity
         and subjectivity scores for the assessed tokens.
         4. ngrams
    """
    translated = translate(sentence)
    doc = nlp(translated)

    return doc._.blob.polarity, \
           doc._.blob.subjectivity, \
           doc._.blob.sentiment_assessments.assessments, \
           doc._.blob.ngrams()


def get_polarity(sentence):
    return translate_and_get_sentiment(sentence)[0]


def get_subjectivity(sentence):
    return translate_and_get_sentiment(sentence)[1]
