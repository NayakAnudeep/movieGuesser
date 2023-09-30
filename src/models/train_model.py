from gensim import corpora
from collections import defaultdict
import visualization
from gensim.similarities import MatrixSimilarity
import gensim

class trainModel:
    df_to_clean = None

    def removeWords(self, df_to_clean):
        # Count word frequencies within each document and across all document
        texts = df_to_clean['all_text_tokenized'].tolist()
        dictionary = corpora.Dictionary(texts)

        # Initialize dictionaries to store word frequencies
        word_frequency_across_all_documents = defaultdict(int)
        word_frequency_within_document = {}
        key = 0

        # Iterate through each document's words
        for text in texts:
            # Count word frequencies within each document
            word_frequency_doc = defaultdict(int)
            for word in text:
                word_frequency_doc[word] += 1
            word_frequency_within_document[key] = word_frequency_doc
            key += 1
            
            # building the total word frequency across all documents 
            for word, freq in word_frequency_doc.items():
                word_frequency_across_all_documents[word] += freq
        visualization.freqCounterPlot(texts)
        # filtering for all words that exceed a threshold within and across all documents for a better representative corpus
        for doc in df_to_clean['all_text_tokenized']:
            for word in doc:
                current_count = doc.count(word)
                if(len(word) <= 2):
                    doc.remove(word)
                    pass
                if (current_count >= 1 and word_frequency_across_all_documents[word] <= 70):
                    pass
                else:
                    doc.remove(word)
        self.df_to_clean = df_to_clean

    def getTrainedModel(self):
        df_to_clean = self.df_to_clean
        dictionary = corpora.Dictionary(df_to_clean['all_text_tokenized'])
        corpus = [dictionary.doc2bow(desc) for desc in df_to_clean['all_text_tokenized']]

        # developing the tf-idf and lsi model using the corpus data
        movie_tfidf_model = gensim.models.TfidfModel(corpus, id2word = dictionary)
        movie_lsi_model = gensim.models.LsiModel(
            movie_tfidf_model[corpus], id2word = dictionary, num_topics = 300)
        
        # serializing and storing the corpus data for easy retrieval
        gensim.corpora.MmCorpus.serialize('movie_tfidf_model_mm', movie_tfidf_model[corpus])
        gensim.corpora.MmCorpus.serialize('movie_lsi_model_mm',movie_lsi_model[movie_tfidf_model[corpus]])

        movie_tfidf_corpus = gensim.corpora.MmCorpus('movie_tfidf_model_mm')
        movie_lsi_corpus = gensim.corpora.MmCorpus('movie_lsi_model_mm')
        movie_index = MatrixSimilarity(movie_lsi_corpus, num_features = movie_lsi_corpus.num_terms)

        return (movie_tfidf_model, movie_lsi_model, movie_index, dictionary)

    def getDF(self):
        return self.df_to_clean
    