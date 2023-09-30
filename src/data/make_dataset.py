import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string

class makeData:
    movie_name = []
    movie_plot = []
    director_list = []
    stars_list = []
    rating_list = []
    storyline = []
    movie_counter = 0
    
    # defining the function that scrapes the data from imdb
    def get_imdb_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_list = soup.find_all('div', class_='lister-item-content')
        for movie in movie_list:
            try:
                self.movie_counter += 1
                self.movie_name.append(movie.find('a').get_text())
                movie_ref_id = movie.find('a')['href'].split('/')[2]
                self.movie_plot.append(movie.find_all('p', class_= 'text-muted')[1].get_text())
                d_start = movie.find_all('p', class_= '')[0].get_text().find('Director:')
                s_start = movie.find_all('p', class_= '')[0].get_text().find('Stars:')
                self.director_list.append(movie.find_all('p', class_= '')[0].get_text()[15:d_start])
                self.stars_list.append(movie.find_all('p', class_= '')[0].get_text()[47:s_start])
                self.rating_list.append(movie.find('strong').get_text())


                url_story = 'https://www.imdb.com/title/{}/plotsummary/?ref_=tt_stry_pl'.format(movie_ref_id)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                }
                response = requests.get(url_story, headers=headers)
                soup_story = BeautifulSoup(response.text, "html.parser") 
                summary_object = soup_story.find_all('span', {'style': 'display:block'})
                if summary_object != []:
                    self.storyline.append(summary_object[0].find_parent('div').get_text())
                else:
                    self.storyline.append('')
                print('Done with movie:', self.movie_counter)
                
            except Exception as e:
                print(e)
                print('Skipping movie:', self.movie_name[-1])
                continue

    # Only gather the data if file is not present
    def getTop500(self, genre_list):
        for genre in genre_list:
            self.movie_counter = 0
            for page in range(1, 11, 1):
                if self.movie_counter <= 50:
                    url = 'https://www.imdb.com/search/title/?title_type=movie&genres={}&sort=num_votes,desc&explore=genres'.format(genre)
                    self.get_imdb_data(self, url)
                    print('Number of {} movies scraped:'.format(genre), self.movie_counter)
                else:
                    url = 'https://www.imdb.com/search/title/?title_type=movie&genres={}&sort=num_votes,desc&start={}&explore=genres&ref_=adv_nxt'.format(genre, self.movie_counter + 1)
                    self.get_imdb_data(self, url)
                    print('Number of {} movies scraped:'.format(genre), self.movie_counter)
        # creating a dictionary with all the lists and creating a df
        data_dic = {
            'name': self.movie_name,
            'rating': self.rating_list,
            'director': self.director_list,
            'stars': self.stars_list,
            'plot': self.movie_plot,
            'storyline': self.storyline
        }
        
        final_movie_df = pd.DataFrame(data_dic)
        final_movie_df.to_csv('final_data')

class cleanData:
    movies_df = None
    spacy_nlp = None
    df_to_clean = None
    stop_words = None
    punctuations = None

    def cleanRawDF(self, file_name):
        df_movies = pd.read_csv(file_name)
        df_movies['storyline'] = df_movies['storyline'].apply(lambda x: str(x).split('—')[0])
        df_movies['summary'] = df_movies['plot'] + ' ' + df_movies['storyline']
        df_movies['all_text'] = df_movies['director'] + df_movies['stars'] + df_movies['summary'] 
        self.setDF(self, df_movies)

    def setDF(self, file_name) -> None:
        self.movies_df = pd.read_csv(file_name)[['name', 'rating', 'director', 'stars', 'summary', 'all_text']]
        self.movies_df = self.movies_df.drop_duplicates(['name', 'summary'])
        # We are just considering 'name' and 'all_text' as it is combination of all the necessary information from the text data
        self.df_to_clean = self.movies_df.reset_index()[['name', 'all_text']]
        self.spacy_nlp = spacy.load("en_core_web_sm")
        self.punctuations = string.punctuation
        self.stop_words = STOP_WORDS
        self.df_to_clean['all_text_tokenized'] = self.df_to_clean['all_text'].map(lambda x: self.spacy_tokenizer(self, str(x)))


    
    def spacy_tokenizer(self, sentence):
        #remove distracting single quotes
        sentence = re.sub('\'','',sentence)
        #remove digits adnd words containing digits
        sentence = re.sub('\w*\d\w*','',sentence)
        #replace extra spaces with single space
        sentence = re.sub(' +',' ',sentence)
        #remove unwanted lines starting from special charcters
        sentence = re.sub(r'\n: \'\'.*','',sentence)
        sentence = re.sub(r'\n!.*','',sentence)
        sentence = re.sub(r'^:\'\'.*','',sentence)
        #remove non-breaking new line characters
        sentence = re.sub(r'\n',' ',sentence)
        #remove punctunations
        sentence = re.sub(r'[^\w\s]',' ',sentence)
        #creating token object
        tokens = self.spacy_nlp(sentence)
        #lower, strip and lemmatize
        tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
        #remove stopwords, and exclude words less than two charecters
        tokens = [word for word in tokens if word not in self.stop_words and word not in self.punctuations and len(word) > 2]
        #return tokens
        return tokens
    
    def getDF(self):
        return self.df_to_clean
    

