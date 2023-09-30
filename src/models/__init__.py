import data
from .train_model import trainModel

print("starting with model")
df_to_clean = data.getCleanDF()
trainModel.removeWords(trainModel, df_to_clean)
print("ending with model")
