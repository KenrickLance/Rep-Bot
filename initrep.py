import pickle

with open('polls.pk1', 'rb') as file:
	polls = pickle.load(file)

print(polls)