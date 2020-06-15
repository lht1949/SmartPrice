import streamlit as st
import pandas as pd
import pickle
import numpy as np
from ebaysdk.finding import Connection as finding

# year = st.slider('year of purchase', min_value=2015, max_value=2019, value=2015)
# st.markdown(f"your laptop was purchase in {year}")

# Draw a title and some text to the app:
'''
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
years = brand_filtered_data['year'].unique()


#year_selected = st.sidebar.slider('year of manufacture', min_value=int(years.min()), max_value=int(years.max()), value=int(years.min()))

year_selected = st.sidebar.selectbox("Year choices", list(brand_filtered_data['year'].unique()), 0)

year_filtered_data = brand_filtered_data.loc[brand_filtered_data['year'] == year_selected]
screen_size_selected = st.sidebar.selectbox("Screen size choices", list(year_filtered_data['screen_size'].unique()), 0)

screen_size_filtered_data = year_filtered_data.loc[year_filtered_data['screen_size'] == screen_size_selected]
cpu_selected = st.sidebar.selectbox("CPU choices", list(screen_size_filtered_data['cpu'].unique()), 0)

cpu_filtered_data = screen_size_filtered_data.loc[year_filtered_data['cpu'] == cpu_selected]
ram_selected = st.sidebar.selectbox("RAM choices", list(cpu_filtered_data['ram'].unique()), 0)

storage_filtered_data = cpu_filtered_data.loc[cpu_filtered_data['ram'] == ram_selected]
storage_selected = st.sidebar.selectbox("Hard drive choices", list(storage_filtered_data['storage'].unique()), 0)


storage_type_filtered_data = storage_filtered_data.loc[storage_filtered_data['storage'] == storage_selected]
storage_type_selected = st.sidebar.selectbox("Hard drive type choices", list(storage_filtered_data['storage_type'].unique()), 0)


cpu_rank = list(computer_cat[computer_cat['cpu'] ==  cpu_selected]['cpu_rank'].unique())

ram_rank = list(computer_cat[computer_cat['ram'] ==  ram_selected]['ram_rank'].unique())

storage_rank = list(computer_cat[computer_cat['storage'] ==  storage_selected]['storage_rank'].unique())


# if brand_selected == 'macbook':
#     temp = [1, 0, 0]
# elif brand_selected == 'macbook pro':
#     temp = [0, 1, 0]
# elif brand_selected == 'macbook air':
#     temp = [0, 0, 1]


#st.write(temp)

predictors = [int(screen_size_selected), int(year_selected), int(cpu_rank[0]), int(ram_rank[0]), int(storage_rank[0])]

loaded_model = pickle.load(open('./data/rf_regrssor.pkl', 'rb'))
#value = round(loaded_model.predict([predictors+temp])[0])
value = round(loaded_model.predict([predictors])[0])



# check current listing

def check_current_listing(keywords):

    df_realtime = pd.DataFrame(columns=['title','price','listingType'])

    myappid = 'StevenLi-insight-PRD-a2eb84eea-78672287'
    api = finding(appid=myappid, config_file=None)

    api_request = {
            'keywords': keywords,
            'categoryId': 111422,
            'itemFilter': [{'name': 'Condition', 'value': 'Used'},
                       {'name': 'ListingType', 'value': 'FixedPrice'},
                {'name': 'LocatedIn', 'value': 'US'}],
            }
    response = api.execute('findItemsAdvanced', api_request)
    num_pages = int(response.reply.paginationOutput.totalPages)

    for page_number in range(1,num_pages+1):
        api_request = {
            'keywords': keywords,
            'categoryId': 111422,
            'itemFilter': [{'name': 'Condition', 'value': 'Used'},
                           #{'name': 'ListingType', 'value': 'FixedPrice'},
                {'name': 'LocatedIn', 'value': 'US'}],
            'paginationInput': {'pageNumber': page_number},
            'outputSelector': ['SellerInfo']
            }
        response = api.execute('findItemsAdvanced', api_request)
        items = response.reply.searchResult.item
        for item in items:
            # select true "Used" (instead of refurbished or for parts listings)
            # conditionId for used is '3000'
            if item.condition.conditionId != '3000':
                continue
#             # not interested in store data
            if item.listingInfo.listingType == 'StoreInventory':
                continue
            if int(item.sellerInfo.feedbackScore) > 10000:
                continue




            title = item.title.lower()
            price = float(item.sellingStatus.currentPrice.value)
            listingType = item.listingInfo.listingType.lower()


            listing = [title,price,listingType]
            df_realtime.loc[len(df_realtime),:] = listing
    return df_realtime


keywords = brand_selected+' '+str(screen_size_selected) +' '+ str(year_selected) +' '+ cpu_selected + ' '+ram_selected + ' '+ storage_selected +' -parts -repair -read'
df_realtime = check_current_listing(keywords)
numListing = df_realtime.shape[0]


st.write(f'The market value of your mac is ${int(value)}! The number of current listings of the selected laptop is {numListing}.')

# if numListing >0:
#     price_listing_mean = df_realtime['price'].mean()
#     st.write(f'The everage of prices of the current listings of the selected laptop is ${int(price_listing_mean)}.')

@st.cache
def load_imag():
    data = pd.read_csv('./data/everymac_imag.csv')
    return data

def show_imag():
    img_url = load_imag()
    url = img_url[(img_url['screen_size'] == screen_size_selected) & (img_url['product'] == brand_selected) & (img_url['year'] == year_selected)]['url']
    st.image(list(url)[0], width=400)

show_imag()
