import pandas as pd
import matplotlib.pyplot as plt
import os

'''
Time v.s Audio Label
'''
FIGURE_PATH = 'fig'

def time_label(path):
    df = pd.read_csv(path)
    plt.figure(figsize=(15,6))
    plt.xticks(rotation=90)
    plt.scatter(df['time'], df['label'])
    plt.savefig(os.path.join(FIGURE_PATH, "audio_label.png"), dpi = 300)
     
#path = "../../data/firestore/Feb8-1_audio_labels.csv"
#time_label(path)