from collections import defaultdict
from models.train_model import trainModel
from operator import itemgetter
from data import cleanData
import pandas as pd



def search_similar_movies(search_term):
    movie_tfidf_model, movie_lsi_model, movie_index, dictionary = trainModel.getTrainedModel(trainModel)
    df_to_clean = trainModel.getDF(trainModel)
    query_bow = dictionary.doc2bow(cleanData.spacy_tokenizer(cleanData,search_term))
    query_tfidf = movie_tfidf_model[query_bow]
    query_lsi = movie_lsi_model[query_tfidf]
    movie_index.num_best = 5
    movies_list = movie_index[query_lsi]
    movies_list.sort(key=itemgetter(1), reverse=True)    
    movie_names = []
    
    for j, movie in enumerate(movies_list):
        movie_names.append (
            {
                'Relevance': round((movie[1] * 100),2),
                'Movie Title': df_to_clean['name'][movie[0]],
                'Movie Plot': df_to_clean['all_text'][movie[0]]
            }

        )
        if j == (movie_index.num_best-1):
            break

    return pd.DataFrame(movie_names, columns=['Relevance','Movie Title','Movie Plot'])