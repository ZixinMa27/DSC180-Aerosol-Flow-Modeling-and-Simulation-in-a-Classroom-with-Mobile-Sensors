import numpy as np
import glob
import pandas as pd
from functools import reduce

"""
Data integration
Consolidating data from six sensors into a single dataset
"""
def combine_dataset(file_paths):    
    data_frames = []
    for _file in file_paths:
        pm_df = pd.read_csv(_file, sep="	", parse_dates=[1], comment='#')
        pm_df['Local_Date_Time'] = pm_df['Local_Date_Time'].dt.floor('S').dt.tz_localize(None)
        pm_df['Time'] = pm_df['Local_Date_Time'].dt.time.astype(str)
        data_frames.append(pm_df)

    combined_df = reduce(lambda left,right: pd.merge(left,right,on='Time'), data_frames)
    return combined_df


"""
Data ingestion
"""
def read_pm(path):
    file_paths = [f for f in glob.glob(path)]
    df = combine_dataset(file_paths)
    return df

"""
sensor place mapping
"""
def map():
    place_mapping = {'137f63':'door', 
                    '680415': 'front corner', 
                    '6f7f19':'back corner/exhaust',
                    '110e60':'back', 
                    '620512': 'front-desk', 
                    '6e0d1e': 'front-tripod'}

    sensor_mapping = {'1837FE6A6AD70C29':'620512', 
                    'DA8590A0DD5EC12B':'6f7f19',
                    '033EBECC09FAA564':'110e60',
                    '38869427C2B44E7E':'6e0d1e',       
                    'BC5F2E8BD0E9B21D':'680415',  
                    '124BF175470BC117':'137f63'}

    sensor_ids = ['1837FE6A6AD70C29', '38869427C2B44E7E', '124BF175470BC117', '033EBECC09FAA564', 'DA8590A0DD5EC12B', 'BC5F2E8BD0E9B21D']
    loc_mapping = {sid:place_mapping[sensor_mapping[sid]] for sid in sensor_ids}
    return (place_mapping, sensor_mapping, sensor_ids, loc_mapping)