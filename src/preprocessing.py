import pandas as pd
import config

retail_dataset = pd.read_excel(config.RAW_DATA_PATH)
# print(retail_dataset.head())
# print(retail_dataset.info())

# drop columns which are not required
columns_to_drop = ['employee_name', 'role', 'shift_date', 'shift_end_time',
                   'availability_date', 'shift_start_time', 'availability_end_time']
retail_dataset = retail_dataset.drop(columns=columns_to_drop)

availability_hour = pd.to_datetime(
    retail_dataset["availability_start_time"]
).dt.hour

retail_dataset["available_morning"] = (
    availability_hour <= 6
).astype(int)

retail_dataset["available_afternoon"] = (
    (availability_hour >= 6) &
    (availability_hour <= 16)
).astype(int)

retail_dataset["available_evening"] = (
    availability_hour >= 11
).astype(int)



retail_dataset.drop(columns=['availability_start_time'])

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

