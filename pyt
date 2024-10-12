-- Data Cleaning

1. -- Data importation
import pandas as pd
df = pd.read_csv(r'C:\Users\TOSHIBA\Desktop\Pipeline Dataset.csv')

2. -- Duplicate removal
df = df.drop_duplicates()
df

3. -- Null values
df = df.fillna('')
df

-- Filling Null values of the liquid type and liquid subtype
df['Liquid Subtype'] = df['Liquid Subtype'].replace('', 'CRUDE OIL')
df1 = df[['Liquid Type', 'Liquid Subtype']]
df1

4. 
# Dropping unnecessary and unuseful columns in the dataset to focus mainly on cleaning the important columns 

df = df.drop(['Liquid Name',
              'Accident Latitude', 
              'Accident Longitude', 
              'Unintentional Release (Barrels)',
              'Intentional Release (Barrels)',
              'Liquid Recovery (Barrels)',
              'Shutdown Date/Time',
              'Restart Date/Time',
              'Operator Employee Injuries', 
              'Operator Contractor Injuries',
              'Emergency Responder Injuries',
              'Other Injuries',
              'Public Injuries',
              'All Injuries',
              'Operator Employee Fatalities',
              'Operator Contractor Fatalities',
              'Emergency Responder Fatalities', 
              'Other Fatalities',
              'Public Fatalities',
              'All Fatalities',
              'Property Damage Costs', 
              'Lost Commodity Costs',
              'Public/Private Property Damage Costs',
              'Emergency Response Costs',
              'Environmental Remediation Costs',
              'Other Costs'], axis=1 )
df

5
# Date standardisation
df['Accident Date/Time'] = pd.to_datetime(df['Accident Date/Time'])
df

-- Data Transformation
# Dictionary mapping state abbreviations to full names
us_state_abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts',
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Replace the abbreviations with full names
df['Accident State'] = df['Accident State'].map(us_state_abbrev)

df

# convert the date column and time column to their respective datatype
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
df['time'] = pd.to_datetime(df['time'], format = '%H:%M:%S').dt.time
df

# Create a new column from the time table to label which period of the day the pipeline accident occured

bins = [0, 6, 12, 16, 20, 24]
labels = ['Midnight', 'Morning', 'Afternoon', 'Evening', 'Night']

df['time_period'] = pd.cut(df['Accident Date/Time'].dt.hour,
                          bins = bins,
                          labels = labels,
                          include_lowest = True)
df

# Data visualisation

import seaborn as sns
import matplotlib.pyplot as plt

# TOP 15 ACCIDENT OCCURENCE PER STATE
location_counts = df['Accident State'].value_counts().nlargest(15)

plt.figure(figsize = (10,6))
location_counts.plot(kind = 'bar')
plt.title('Pipeline Accidents by State')
plt.xlabel('Accident State')
plt.ylabel('Reported Cases')

plt.show()

# TOP 10 ACCIDENT CAUSES

cause_counts = df['Cause Category'].value_counts()
top_10_causes = cause_counts.nlargest(10)

plt.figure(figsize=(10,6))
top_10_causes.plot(kind='bar')
plt.title('Top causes of pipeline accident')
plt.xlabel('Cause')
plt.ylabel('Count')

plt.show()

# ACCIDENT OCCURENCE BY YEAR

year_counts = df['Accident Year'].value_counts()

plt.figure(figsize = (10,6))
year_counts.plot(kind = 'line')
plt.title('Accidents Over Time')
plt.xlabel('Year')
plt.ylabel('Accident Reported')

plt.show()
