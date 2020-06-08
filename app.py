import streamlit as st
import pandas as pd
import numpy as np
import pickle

# year = st.slider('year of purchase', min_value=2015, max_value=2019, value=2015)
# st.markdown(f"your laptop was purchase in {year}")

# Draw a title and some text to the app:
''''
# Smart Price

Optimum price for your used laptop!
'''


@st.cache
def load_data():
    data = pd.read_csv('./data/everymac.csv')
    return data

computer_cat = load_data()
brand_selected = st.sidebar.selectbox("Brand choices", list(computer_cat['product'].unique()), 0)

brand_filtered_data = computer_cat.loc[computer_cat['product'] == brand_selected]
year_selected = st.selectbox("Year choices", list(brand_filtered_data['year'].unique()), 0)

year_filtered_data = brand_filtered_data.loc[brand_filtered_data['year'] == year_selected]
screen_size_selected = st.selectbox("Screen size choices", list(year_filtered_data['screen_size'].unique()), 0)

screen_size_filtered_data = year_filtered_data.loc[year_filtered_data['screen_size'] == screen_size_selected]
cpu_selected = st.selectbox("Cpu choices", list(screen_size_filtered_data['cpu'].unique()), 0)

cpu_filtered_data = screen_size_filtered_data.loc[year_filtered_data['cpu'] == cpu_selected]
ram_selected = st.selectbox("Cpu choices", list(cpu_filtered_data['ram'].unique()), 0)

storage_filtered_data = cpu_filtered_data.loc[cpu_filtered_data['ram'] == ram_selected]
storage_selected = st.selectbox("Hard drive choices", list(storage_filtered_data['storage'].unique()), 0)


cpu_dict={'m 1.1': 1, 'm 1.2': 1, 'm 1.3': 1, 'm3 1.1': 2, 'm3 1.2': 2, 'm5 1.2':3,
         'm7 1.3': 4, 'i5 1.3':5, 'i5 1.6':5, 'i5 1.8':5, 'i7 2.2':5, 'i5 1.1':5, 'i5 2.7':5,
       'i5 2.9':5, 'i7 3.1':6, 'i7 2.5':6, 'i7 2.8':6, 'i5 2.0':6, 'i7 2.4':6,
       'i5 3.1':6, 'i7 3.3':6, 'i7 2.6':6, 'i7 2.7':6, 'i7 2.9':6, 'i5 2.3':5,
       'i5 3.3':5, 'i7 3.5':6, 'i9 2.9':7, 'i5 2.4':7, 'i9 2.3':7, 'i9 2.4':7,
       'i5 1.4':5}

ram_dict={'4 gb': 1, '8 gb': 2, '16 gb': 3}
storage_dict={'128 gb': 1, '256 gb': 2, '512 gb': 3, '1 tb': 4}

if brand_selected == 'macbook':
    temp = [1, 0, 0]
elif brand_selected == 'macbook pro':
    temp = [0, 1, 0]
elif brand_selected == 'macbook air':
    temp = [0, 0, 1]

#st.write(temp)

predictors = [int(screen_size_selected), int(year_selected), cpu_dict.get(cpu_selected), ram_dict.get(ram_selected), storage_dict.get(storage_selected)]

loaded_model = pickle.load(open('./data/rf_fixedprice_regrssor.pkl', 'rb'))
value = round(loaded_model.predict([predictors+temp])[0])
st.write(f'The market value of your mac is ${int(value)}!')
