import sys
sys.path.append("../")
import os, shutil
import sys
import numpy as np
import random
import world
import model
import grammar
import speaker
from utils import read_dataset, printer

np.set_printoptions(suppress=True)

'''Create data directory if it does not exist.'''
if not os.path.exists("./data"):
    os.makedirs("./data")


'''Remove content of data/ directory.'''
folder = './data/'
for f in os.listdir(folder):
    file_path = os.path.join(folder, f)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)


'''Start of simulation. Create a world.'''
real_world = world.World("../animal-dataset.txt",50,30)



'''Let's share the vocab between speakers for now.'''
kinds, vocab = read_dataset("../animal-dataset.txt")

'''Make S1'''
print "Making speaker S1..."
m1 = model.Model()
m1.mk_speaker_model(real_world,30)
m1.print_me()
S1 = speaker.Speaker("Kim",vocab,m1)

'''Make S2'''
print "Making speaker S2..."
m2 = model.Model()
m2.mk_speaker_model(real_world,30)
m2.print_me()
S2 = speaker.Speaker("Sandy",vocab,m2)

print "\n\nSpeaker overlap (the instances that both speakers know about)...\n\n"
s1_e=[]
for e in S1.model.entities:
    s1_e.append(e.ID)
s2_e=[]
for e in S2.model.entities:
    s2_e.append(e.ID)
print set(S1.model.entities).intersection(set(S2.model.entities))

'''Refer: generate sentences about the actual entities of the domain.'''
for entity in S1.model.entities:
    words = []
    for p in entity.predicates:
        words.append(p.form)
    sentences = grammar.generate(words)
    for s in sentences:
        print "S1 says about",entity.ID,":",s

        '''S2 checks. Is it really true?'''
        truth, denotation = S2.model.true_interpretation(s)
        print "S2 thinks this sentence is",truth
        for e in denotation:
            print e.ID