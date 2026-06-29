import pandas as pd
import config

retail_dataset = pd.read_excel(config.RAW_DATA_PATH)
# print(retail_dataset.head())
# print(retail_dataset.info())

# drop columns which are not required
columns_to_drop = ['employee_name', 'role', 'shift_date', 'shift_end_time',
                   'availability_date', 'availability_start_time', 'availability_end_time']
retail_dataset = retail_dataset.drop(columns=columns_to_drop)

# adding shift type 
retail_dataset['shift_type'] = pd.to_datetime(retail_dataset['shift_start_time']).dt.hour.apply(
    lambda h: 'Morning' if 6 <= h < 14
    else 'Afternoon' if 14 <= h < 22
    else 'Evening'
)

# creating columns for each shift availability 
retail_dataset['available_morning'] = (
    retail_dataset['shift_type'] == 'Morning'
).astype(int)

retail_dataset['available_afternoon'] = (
    retail_dataset['shift_type'] == 'Afternoon'
).astype(int)

retail_dataset['available_evening'] = (
    retail_dataset['shift_type'] == 'Evening'
).astype(int)

# drop shift_type after creating avialiability columns
retail_dataset = retail_dataset.drop(columns=['shift_type', 'shift_start_time'])

# creating shift demand - fixed demand throughout the week 
SHIFT_DEMAND = {
    'Morning': 6,
    'Afternoon': 5,
    'Evening': 4
}

# split by store 
print(retail_dataset['store_state'].value_counts())

small_retail = retail_dataset[retail_dataset['store_state']=='WA']
large_retail = retail_dataset[retail_dataset['store_state']=='OR']

# verify dataset 
print(small_retail.employee_id.nunique()) # 24
print(large_retail.employee_id.nunique()) # 65

# remove store_state
small_retail = small_retail.drop(columns=['store_state'])
large_retail = large_retail.drop(columns=['store_state'])

# save datasets 
small_retail.to_csv(config.DATA_SMALL_PATH, index=False)
large_retail.to_csv(config.DATA_LARGE_PATH, index=False)

# recehck datasets after splitting 
print(small_retail.shape)
print(large_retail.shape)

config.logger.info('small_retail Dataset loaded: %s rows, %s columns', small_retail.shape[0], small_retail.shape[1])
config.logger.info('large_retail Dataset loaded: %s rows, %s columns', large_retail.shape[0], large_retail.shape[1])

