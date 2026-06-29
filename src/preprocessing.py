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

# calculate labour cost 
small_retail['labor_cost'] = (
    small_retail['hourly_wage'] * small_retail['scheduled_hours']
)

large_retail['labor_cost'] = (
    large_retail['hourly_wage'] * large_retail['scheduled_hours']
)

# save datasets 
small_retail.to_csv(config.DATA_SMALL_PATH, index=False)
large_retail.to_csv(config.DATA_LARGE_PATH, index=False)

# recehck datasets after splitting 
# print(small_retail.shape)
# print(large_retail.shape)

config.logger.info("small_retail Dataset loaded: %s rows, %s columns", small_retail.shape[0], small_retail.shape[1])
config.logger.info("large_retail Dataset loaded: %s rows, %s columns", large_retail.shape[0], large_retail.shape[1])

