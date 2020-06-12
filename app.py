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
cpu_selected = st.sidebar.selectbox("Cpu choices", list(screen_size_filtered_data['cpu'].unique()), 0)

cpu_filtered_data = screen_size_filtered_data.loc[year_filtered_data['cpu'] == cpu_selected]
ram_selected = st.sidebar.selectbox("Cpu choices", list(cpu_filtered_data['ram'].unique()), 0)

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
#             if item.listingInfo.listingType == 'StoreInventory':
#                 continue
            if int(item.sellerInfo.feedbackScore) > 10000:
                continue




            title = item.title.lower()
            price = float(item.sellingStatus.currentPrice.value)
            listingType = item.listingInfo.listingType.lower()


            listing = [title,price,listingType]
            df_realtime.loc[len(df_realtime),:] = listing
    return df_realtime.shape[0]


keywords = brand_selected+' '+str(screen_size_selected) +' '+ str(year_selected) +' '+ cpu_selected + ' '+ram_selected + ' '+ storage_selected +' -parts -repair -read'
numListing = check_current_listing(keywords)

st.write(f'The market value of your mac is ${int(value)}! The number of current listings of the selected laptop is {numListing}.')

if (year_selected == 2015) & (brand_selected =='macbook'):
    st.image('https://techcrunch.com/wp-content/uploads/2015/04/macbook-front.jpg?w=730&crop=1', width=400)

elif (year_selected == 2016) & (brand_selected =='macbook'):
    st.image('https://cnet3.cbsistatic.com/img/w1eCN8WZ-8dujQWgg57SABUrE9A=/1200x675/2016/04/19/9102f487-6b02-4987-bfd7-0268c91b53ea/apple-macbook-2016-22.jpg', width=400)

elif (year_selected == 2017) & (brand_selected =='macbook'):
    st.image('https://i.pcmag.com/imagery/reviews/005x4wlhEjDj4CRKQQuVVet-10.fit_scale.size_1028x578.v_1569472269.jpg', width=400)



elif (year_selected == 2010) & (brand_selected =='macbook air') & (screen_size_selected == 11):
    st.image('https://images.anandtech.com/reviews/mac/macbookair2011/DSC_4301.jpg', width=400)


elif (year_selected == 2015) & (brand_selected =='macbook air') & (screen_size_selected == 11):
    st.image('https://i.pcmag.com/imagery/reviews/025GQFzhMiBKUqeRWEheThp-6.fit_scale.size_1028x578.v_1569481443.jpg', width=400)


elif (year_selected == 2015) & (brand_selected =='macbook air') & (screen_size_selected == 13):
    st.image('https://cnet2.cbsistatic.com/img/ajvbHHC5YGYoPgpiTCMagICG9Ws=/868x488/2015/05/06/1503bb41-3bf4-412a-8e7a-a94c084b140d/apple-macbook-air-2015-02.jpg', width=400)
