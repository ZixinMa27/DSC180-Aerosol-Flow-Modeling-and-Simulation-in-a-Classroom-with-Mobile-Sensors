import numpy as np
from matplotlib import pyplot as plt 
import glob
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import plotly
import os


from src.data_preprocess import *

place_mapping, sensor_mapping, sensor_ids, loc_mapping = map()

x_mapping  = {k:v for k,v  in zip(sensor_ids, [.65, .9, .95, 0, 0, .9 ]) }
y_mapping  = {k:v for k,v in zip(sensor_ids, [.45, .45, 0, 0.1, .85, 1]) }
z_mapping  = {k:v for k,v in zip(sensor_ids, [.3, .5, 0.9, 0.8, .2, .6]) }

col_names =['Epoch_UTC', 'Local_Date_Time', 'MassConc_1p0',
       'MassConc_2p5',
       'MassConc_4p0',
       'MassConc_10p',
       'NumbConc_0p5',
       'NumbConc_1p0',
       'NumbConc_2p5',
       'NumbConc_4p0',
       'NumbConc_10p',
       'TypPartSize', 'id', 'x', 'y', 'z', 'loc']


def plot_3d(file_paths, plot_col = 'MassConc_2p5',start_ts = 250, end_ts =400, trial = "High-Fan-Speed"):
    data_frames = []
    for i, _file in enumerate(file_paths):
        #df = pd.read_csv(_file, sep="	 ", parse_dates=[1], error_bad_lines='skip')
        df = pd.read_csv(_file, sep="	", parse_dates=[1], comment = '#')
        df['Local_Date_Time'] = df['Local_Date_Time'].dt.floor('S').dt.tz_localize(None)
        sensor_id = _file.split("_")[-1].split(".")[0]
        df['id'] = sensor_id
        df['x'] = x_mapping[sensor_id]
        df['y'] = y_mapping[sensor_id]
        df['z'] = z_mapping[sensor_id]
        df['loc'] = loc_mapping[sensor_id]
        df.columns = col_names
        df = df.sort_values(by=['Epoch_UTC'])
        df = df.reset_index()
        df['time_elapsed'] = df.index
        df = df.dropna()
        data_frames.append(df.iloc[start_ts:end_ts, :])
    
    combined_df = pd.concat(data_frames, axis=0)
    combined_df['time_elapsed'] = combined_df['time_elapsed'] - start_ts
    min_conc_val = combined_df[plot_col].min()
    max_conc_val = combined_df[plot_col].max()
    fig = px.scatter_3d(combined_df,x='x', y='y', z='z', text='loc', color= plot_col, size= plot_col, animation_frame='time_elapsed', size_max=50, range_color=[min_conc_val, max_conc_val])
    fig.update_layout(title_text='Aerosol Concentration Changes Following a Cough  {}'.format(trial), title_x= 0.43, width= 750, height = 400)
    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=5, range=[0,1],),
                        yaxis = dict(nticks=5, range=[0,1],),
                        zaxis = dict(nticks=5, range=[0,1],),
                        aspectratio=dict(x=1, y=1, z=1),
                    ),
            )
    fig.show()
    pio.write_html(fig, file='Fig/pm_data_animation.html', auto_open=False)