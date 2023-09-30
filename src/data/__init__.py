from .make_dataset import makeData
import os
from .make_dataset import cleanData

# creating a list of all genres to loop over
genre_list = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 'family',
              'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical', 'mystery', 'romance', 'sci-fi',
              'short', 'sport', 'thriller', 'war', 'western']
file_name = "data.csv"

current_directory = os.getcwd() + '\data'
print(current_directory)
print(current_directory)
full_file_path = os.path.join(current_directory, file_name)
print(full_file_path)

if(os.path.isfile(full_file_path) == False):
    makeData.getTop500(makeData, genre_list)
else:
    print('File:',file_name,'Already exists')

cleanData.setDF(cleanData, file_name)
print("Finished with setDF")
def getCleanDF():
    return cleanData.getDF(cleanData)