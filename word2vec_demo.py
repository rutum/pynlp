import gensim.models

# setup logging
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# train the basic model with text8-rest, which is all the sentences
# without the word - queen
model = gensim.models.Word2Vec()
sentences = gensim.models.word2vec.Sentences("text8-rest")
model.build_vocab(sentences)
model.train(sentences)

# model.n_similarity("king", "duke")

sentences2 = gensim.models.word2vec.Sentences("text8-queen")
model.update_vocab(sentences2)
model.train(sentences2)

# model.n_similarity("king", "queen")
