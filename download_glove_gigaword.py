import gensim.downloader as api

vectors = api.load('glove-wiki-gigaword-300')
vectors.save('glove-wiki-gigaword-300')