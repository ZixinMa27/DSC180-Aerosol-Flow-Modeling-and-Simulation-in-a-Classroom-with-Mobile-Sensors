
import pandas as pd
import matplotlib.pyplot as plt


'''
Time v.s Audio Label
'''
def time_label(path):
    df = pd.read_csv(path)
    plt.figure(figsize=(15,6))
    plt.xticks(rotation=90)
    plt.scatter(df['time'], df['label'])
    plt.savefig("label.png")
    plt.show()
    
# DO: modify path    
path = "../../data/firestore/Feb8-1_audio_labels.csv"
time_label(path)