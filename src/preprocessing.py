'''
preprocessing.py
use for data preporcessing 
'''

import pandas as pd
import config

retail_dataset = pd.read_excel(config.RAW_DATA_PATH)
# print(retail_dataset.head())
# print(retail_dataset.info())

# drop columns which are not required
columns_to_drop = ['employee_name', 'role']
retail_dataset = retail_dataset.drop(columns=columns_to_drop)

# adding shift type 
retail_dataset['shift_type'] = pd.to_datetime(retail_dataset['shift_start_time']).dt.hour.apply(
    lambda h: "Morning" if 6 <= h < 14
    else "Afternoon" if 14 <= h < 22
    else "Evening"
)

# calculate labour cost 
retail_dataset['labor_cost'] = (
    retail_dataset['hourly_wage'] * retail_dataset['scheduled_hours']
)

# split by store 
# print(retail_dataset['store_state'].value_counts())

small_retail = retail_dataset[retail_dataset['store_state']=='WA']
large_retail = retail_dataset[retail_dataset['store_state']=='OR']

# verify dataset 
# print(small_retail.employee_id.nunique()) # 24
# print(large_retail.employee_id.nunique()) # 65

# remove store_state
small_retail = small_retail.drop(columns=['store_state'])
large_retail = large_retail.drop(columns=['store_state'])

# save datasets 
small_retail.to_csv(config.DATA_SMALL_PATH, index=False)
large_retail.to_csv(config.DATA_LARGE_PATH, index=False)

# recehck datasets after splitting 
# print(small_retail.shape)
# print(large_retail.shape)

config.logger.info("small_retail Dataset loaded: %s rows, %s columns", small_retail.shape[0], small_retail.shape[1])
config.logger.info("large_retail Dataset loaded: %s rows, %s columns", large_retail.shape[0], large_retail.shape[1])

