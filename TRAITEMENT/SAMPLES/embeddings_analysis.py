from gensim.test.utils import common_texts
from gensim.models import Word2Vec

def main():
    model_name = sys.argv[1]
    model = Word2Vec.load(model_name)

if __name__ == '__main__':
    main()
