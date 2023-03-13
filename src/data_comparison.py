import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 
import glob
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import plotly
from functools import reduce
plt.style.use('ggplot')
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns


from src.data_preprocess import *

place_mapping, sensor_mapping, sensor_ids, loc_mapping = map()

def plot_event(df,plot_type = "MassConc", PM_size = "2p5", timestamp= 0, interval = 1000, event = 5,  trial = 'Feb8-1'):
    size = {"0p5": '0.5', "1p0": '1.0', "2p5":'2.5', "4p0":'4.0', "10p": '10.0'}
    concentration = {"MassConc": 'Mass Concentration', "NumbConc": 'Count Concentration'}

    df = df[timestamp:timestamp+interval]
    df['elapsed_time']  = range(interval)
    
    # Plot figure
    fig, ax = plt.subplots(figsize=(10,5))
    # Plot
    for i, j in enumerate([f'{plot_type}_{PM_size}_SPS3x_{sensor_id}' for sensor_id in sensor_mapping.keys()]):
        _ = ax.plot(df['elapsed_time'], df[j], 
                    label=[ place_mapping[sensor_mapping[sensor_id]] for sensor_id in sensor_mapping.keys()][i])
        _ = ax.legend() 
        
    # add description
    ax.set_title('PM {} Sensors at Different Location - {}'.format(size[PM_size], trial))
    ax.set_ylabel('{} (µg/m3)'.format(concentration[plot_type]))
    ax.set_xlabel('Elapsed time (second)')
    # ax.set_yscale('log')
    # plt.savefig("PM{}_{}_{}.png".format(size[PM_size], plot_type, trial), bbox_inches="tight",facecolor="white", dpi=300)
    plt.show()
    
def plot_events_subplot(data_list, plot_type = "MassConc", PM_size = "2p5", y_logscale=True, plot_backend ="mpl"):
    size = {"0p5": '0.5', "1p0": '1.0', "2p5":'2.5', "4p0":'4.0', "10p": '10.0'}
    concentration = {"MassConc": 'Mass Concentration', "NumbConc": 'Count Concentration'}

    fig, ax = plt.subplots(nrows=len(data_list), ncols=1, sharex=True, sharey=True, figsize=(8, 5))
    label_name = []

    for k, data_dict in enumerate(data_list):
        timestamp = data_dict['timestamp']
        interval = data_dict['interval']
        df = data_dict['df'].iloc[timestamp:timestamp+interval]
        df['elapsed_time']  = range(interval)
        col_list = [f'{plot_type}_{PM_size}_SPS3x_{sensor_id}' for sensor_id in sensor_mapping.keys()]
        print(col_list)
        label_name = [place_mapping[sensor_mapping[sensor_id]] for sensor_id in sensor_mapping.keys()]
        print([place_mapping[sensor_mapping[sensor_id]] for sensor_id in sensor_mapping.keys()])
        ax[k].plot(df['elapsed_time'], pd.DataFrame(df[col_list]))#, 
                        #label= label_name)
        # _ = ax[k].legend()
        
        ax[k].title.set_text(data_dict['label'])
        if y_logscale:
            ax[k].set_yscale('log')
    #fig.suptitle(f'PM {PM_size} Sensors at Different Position with Different Fan Speed')
    handles, labels = ax[0].get_legend_handles_labels()
    
    #fig.legend(handles, labels, loc='upper left')
    fig.legend(label_name, loc='upper right')
    plt.subplots_adjust(left=None, bottom=None, right=.9, top=None, wspace=None, hspace=.4)
    ax[1].set_ylabel('log {} (µg/m3)'.format(concentration[plot_type]))
    ax[-1].set_xlabel('Elapsed Time (sec)')
    if plot_backend == "mpl":
        plt.show()
        fig.savefig("PM{}_Diff_Loc.png".format(size[PM_size]), bbox_inches="tight",facecolor="white", dpi=300)
    else:
        plotly_fig = plotly.tools.mpl_to_plotly(fig)
        plotly_fig.update_layout(width= 700, height = 500, showlegend= True)
        plotly_fig.show()
        pio.write_html(plotly_fig, file='Fig/pm_data_diff_setting.html', auto_open=False)

def ploty_event(df,plot_type = "MassConc", PM_size = "2p5", timestamp= 0, interval = 1000, event = 5,  trial = 'Feb8-1'):
    size = {"0p5": '0.5', "1p0": '1.0', "2p5":'2.5', "4p0":'4.0', "10p": '10.0'}
    concentration = {"MassConc": 'Mass Concentration', "NumbConc": 'Count Concentration'}

    df = df[timestamp:timestamp+interval]
    df['elapsed_time']  = range(interval)
    columns = [f'{plot_type}_{PM_size}_SPS3x_{sensor_id}' for sensor_id in sensor_mapping.keys()]  
    label_name = [place_mapping[sensor_mapping[sensor_id]] for sensor_id in sensor_mapping.keys()]
    fig = go.Figure()
    for i, d in enumerate(columns):
        fig.add_trace(go.Scatter(x = df['elapsed_time'],
                                y = df[d],
                                name = label_name[i],
                                fill=None))   #tozeroy 
    fig.update_layout(
        title='PM{} Sensors Aerosol Concentration at Different Location - {}'.format(size[PM_size], trial),
        xaxis_title="Elapsed Time (sec)",
        yaxis_title='{} (µg/m3)'.format(concentration[plot_type]),
        legend_title="Sensor Location",
        width= 500, 
        height = 300,
        showlegend = True,
        font = dict(size = 8)
    )
    
    fig.show()
    pio.write_html(fig, file='Fig/pm{}_data_{}.html'.format(PM_size,trial), auto_open=False)

