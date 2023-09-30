import data
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

df_to_clean = data.getCleanDF()
# visualizing frequency of words to describe the movies based on storyline and plot
series = pd.Series(np.concatenate(df_to_clean['all_text_tokenized'])).value_counts()[:100]
wordcloud = WordCloud(background_color='white').generate_from_frequencies(series)

print("plotting here")
plt.figure(figsize=(15,15), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('wordcloud_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("ending here")
def freqCounterPlot(x):
    # Plotting frequency of word to approximate the threshhold in the next step
    plt.hist(x, bins=1)
    plt.xticks([])
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Count of Words')
    plt.savefig('thresholdPlot.png', dpi=300, bbox_inches='tight')
    plt.show()