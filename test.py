import pickle

model = pickle.load(open("/home/rekarenan/Desktop/modelos/model.pkl", "rb"))
model.predict([1,2,4,5])
print(model)
