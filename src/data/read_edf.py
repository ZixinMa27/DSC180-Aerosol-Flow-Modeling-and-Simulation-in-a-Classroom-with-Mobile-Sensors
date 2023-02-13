import glob

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly
#from plotly import tools as tls

sns.set_theme()

# plt.style.use('ggplot')

def plot_pm_data(dataframes, plot_type="mass_conc"):

    place_mapping = {'137f63':'door', '680415': 'fan corner', '6f7f19':'back of ac',
                    '110e60':'back of mannequin', '620512': 'source'}

    sensor_mapping = {'BC5F2E8BD0E9B21D':'680415', 'DA8590A0DD5EC12B':'6f7f19', 
                    '1837FE6A6AD70C29':'620512', '124BF175470BC117':'137f63', '033EBECC09FAA564':'110e60'}

    fig, ax = plt.subplots(nrows=5, ncols=1, sharex=True, sharey=True, figsize=(15, 13))  
    ax[-1].set_xlabel('Time')
    # ax.set_title('PM Sensor Reading')

    if plot_type == "mass_conc":
        data_cols = ['MassConc_1p0_SPS3x_', 'MassConc_2p5_SPS3x_',
                    'MassConc_4p0_SPS3x_', 'MassConc_10p_SPS3x_']
        labels = ['1.0', '2.5', '4.0', '10.0']
        # ax.set_ylabel('Mass Concentration')
    else:
        data_cols = ['NumbConc_0p5_SPS3x_', 'NumbConc_1p0_SPS3x_','NumbConc_2p5_SPS3x_', 
                    'NumbConc_4p0_SPS3x_', 'NumbConc_10p_SPS3x_']
        labels = ['0.5', '1.0', '2.5', '4.0', '10.0']
        # ax.set_ylabel('Count Concentration')
    

    for i, (loc, df) in enumerate(dataframes.items()):

        data_cols_sensor = [col_name+loc for col_name in data_cols]

        if plot_type == "mass_conc":
            df[data_cols_sensor] = df[data_cols_sensor].clip(lower=0, upper=500)

        print(i, loc)
        # df = df.iloc[:200, :]
        ax[i].plot(df['Local_Date_Time'], df[data_cols_sensor], label=labels)
        ax[i].set_title(place_mapping[sensor_mapping[loc]], loc='right', y=1.0)
        ax[i].set_ylabel("Concentration (μg/m3)", rotation=90)

    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left')
    plt.subplots_adjust(left=None, bottom=None, right=.9, top=None, wspace=None, hspace=0.9)
    plt.savefig("pm_data_visualization.png")
    plt.show()
    
    # plotly_fig = tls.mpl_to_plotly(fig)
    # plotly_fig.show()



file_paths = [f for f in glob.glob('../data/pm_data/*.edf')]
data_frames = {}

for _file in file_paths:
    print(_file)
    df = pd.read_csv(_file, sep="	", parse_dates=[1])

    sensor_id = _file.split("_")[-1].split(".")[0]
    data_frames[sensor_id] = df



plot_pm_data(data_frames)


