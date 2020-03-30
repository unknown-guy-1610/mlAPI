import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

class processor:
    def process_data(self, data):
        return data

class predictor:
    def __init__(self, model):
        self.model = model
    def predict(self, data):
        predictions = self.model.predict(data)
        return predictions

Processor = processor()
processed_data = Processor.process_data(data)
model = DecisionTreeClassifier()

X_train, y_train = processed_data.iloc[:, 1].values.reshape(-1, 1), processed_data.iloc[:, 2].values


model.fit(X_train, y_train)

Predictor = predictor(model)

X_test = test_data.iloc[:, 1].values.reshape(-1, 1)
print(Predictor.predict(X_test))

with open('processor.pickle', 'wb') as f:
    pickle.dump(Processor, f)

with open('predictor.pickle', 'wb') as f:
    pickle.dump(Predictor, f)