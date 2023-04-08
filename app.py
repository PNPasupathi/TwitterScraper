import base64
import datetime
import time
import json
import pandas as pd
import pymongo
import snscrape.modules.twitter as sntwitter
import streamlit as st
from streamlit_option_menu import option_menu
import zipfile
import os


                                            #FUNCTIONS
def profile(user):
        limit = 1
        ids = {}
        dname={}
        name = {}
        desc = {}
        follw = {}
        url = {}
        rep = {}
        ret = {}
        lan = {}
        like = {}
        source = {}
        for i, tweet in enumerate(sntwitter.TwitterProfileScraper(user).get_items()):
            if i < limit:
                ids['User_ID'] = tweet.id
                dname['Name']=tweet.user.displayname
                name['User_Name'] = tweet.username
                url['Url'] = tweet.url
                desc['Description'] = tweet.user.description
                follw['Followers'] = tweet.user.followersCount
                source['Source'] = tweet.source
                rep['Reply_Count'] = tweet.replyCount
                ret['Retweet_Count'] = tweet.retweetCount
                like['Like_Count'] = tweet.likeCount
                lan['Language'] = tweet.lang
                data = [{'User_ID': ids['User_ID'],'Url': url['Url'],'Name':dname['Name'], 'User_Name': name['User_Name'],
                         'Description': desc['Description'], 'Followers': follw['Followers'],
                         'Source': source['Source'], 'Reply_Count': rep['Reply_Count'],
                         'Retweet_Count': ret['Retweet_Count'], 'Like_Count': like['Like_Count'],
                         'Language': lan['Language']}]
                print(data)
                return data
            else:
                break

def trending(limit):
        tname = []
        tdomain = []
        tdesc = []
        for i, trend in enumerate(sntwitter.TwitterTrendsScraper().get_items()):
            if i < limit:
                tname.append(trend.name)
                tdomain.append(trend.domainContext)
                tdesc.append(trend.metaDescription)
            else:
                break
        i = 0
        lst = []
        while i < limit:
            dic = {'Trend Name': tname[i], 'Domain': tdomain[i], 'Description': tdesc[i]}
            i += 1
            # st.write(dic)
            lst.append(dic)
        return lst
def tweetsearch( keyword,start,end, limit):
    try:
        ids = []
        name = []
        contents = []
        date = []
        lst = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{end} until:{start}".format(keyword,end,start)).get_items()):
            if i < limit:
                ids.append(tweet.id)
                name.append(tweet.username)
                contents.append(tweet.content)
                date.append(tweet.date.ctime())
            else:
                break
        for i in range(limit):
            lst.append({'ID': ids[i], 'Name': name[i], 'Content': contents[i], 'Date': date[i]})

        return lst
    except:
        st.warning(str(limit)+' Tweet is not in a Particular Date Range')
def convertcsv(x):
    return x.to_csv(index=False).encode('utf-8')

                                        #MAIN PROGRAM


selected = option_menu(menu_title='TWITTER SCRAPER', options=['Profile', 'Trending', 'Search'], orientation='horizontal',
                       icons=['person-badge','graph-up-arrow','search'])


                                        #DATABASE
try:
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
            unsafe_allow_html=True
        )


    add_bg_from_local('Image/dbimg.jpg')
    st.subheader('Connect Your Database')
    choose=st.selectbox('Select Your Choice ',['Mongodb Localhost','Mongodb Atlas'])
    if choose=='Mongodb Atlas':
        try:
            st.write('')
            dblink=st.text_input('Enter Your Database Link')
            pwd=st.text_input('Enter Your Password',type="password")
            uid=dblink.replace('<password>',pwd)
            client = pymongo.MongoClient(uid)
            db = client['Database']

                                  #PROFILE
            if selected=='Profile':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                    <style>
                    .stApp {{
                        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                        background-size: cover
                    }}
                    </style>
                    """,
                        unsafe_allow_html=True
                    )
                add_bg_from_local('Image/Twipro.jpg')



                try:

                    if " 🚀 Search" not in st.session_state:
                        st.session_state[" 🚀 Search"] = False
                    if "📂 Insert MongoDB" not in st.session_state:
                        st.session_state["📂 Insert MongoDB"] = False
                    st.title('Twitter Profile Scraper ')
                    st.write('')
                    st.write('')
                    name = st.text_input('Enter Your Profile Name ',)
                    st.markdown(
                        """
                        <style>
                        textarea {
                            font-size: 3rem !important;
                        }
                        input {
                            font-size: 1.2rem !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(" 🚀 Search"):
                        st.session_state[" 🚀 Search"] = not st.session_state[" 🚀 Search"]
                    if st.session_state[" 🚀 Search"]:
                        st.write('')
                        st.write('')
                        if len(name)!=0:
                            with st.spinner('Please Wait for it...'):
                                time.sleep(0.5)
                                data = profile(name)
                                st.markdown (r'Profile of **{}**'.format(data[0]['Name']))
                                st.dataframe(data,width=800)
                            with st.sidebar:
                                radio=st.selectbox('Choose Your Choice     ',['CSV','JSON'],)
                                st.write('')
                                st.write('')
                                st.write('')
                                if radio=='CSV':
                                    df = pd.DataFrame(data)
                                    csv = convertcsv(df)
                                    st.write('')
                                    st.write('Click to Download CSV File')
                                    st.write('')
                                    csv=st.download_button('📥 Download', csv, 'Profile.csv', 'text/csv', key='download-csv')
                                    st.write('')
                                    st.write('')
                                    if csv:
                                        with st.spinner('Waiting for Confirmation...'):
                                            time.sleep(0.8)
                                            st.success('Download Successfully ')
                                if radio=='JSON':
                                    js = json.dumps(data[0])
                                    st.write('')
                                    st.write('Click to Download JSON File')
                                    st.write('')
                                    json=st.download_button('📥 Download ', js, 'ProfileJson.json')
                                    st.write('')
                                    st.write('')
                                    if json:
                                        with st.spinner('Waiting for Confirmation...'):
                                            time.sleep(0.8)
                                            st.success('Download Successfully ')
                            st.write('')
                            st.write('')
                            if st.button(' 📂 Insert MongoDB'):
                                st.write('')
                                st.write('')
                                prg = st.progress(0)
                                for i in range(100):
                                    time.sleep(0.01)
                                    prg.progress(i + 1)

                                st.session_state["📂 Insert MongoDB"] = not st.session_state["📂 Insert MongoDB"]

                                # drop collection
                                profilecollection = db.drop_collection('Profile')
                                # create colletion
                                profilecollection = db.create_collection('Profile')
                                profilecollection.insert_many(data)
                                st.write("")
                                st.subheader('Record Inserted Successfully !')

                    else:
                        quit()
                except :
                    st.write("")

                                                #TRENDING

            if selected=='Trending':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                    <style>
                    .stApp {{
                        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                        background-size: cover
                    }}
                    </style>
                    """,
                        unsafe_allow_html=True
                    )
                add_bg_from_local('Image/Twitrend1.jpg')

                try:
                        st.title('Twitter Trending Scraper')
                        st.write('')
                        radio=st.radio('Choose One Option ',['👁‍🗨 View Records','📥 Store Database & Download'])
                        if radio=='👁‍🗨 View Records':
                            st.markdown(
                                """
                                <style>
                                textarea {
                                    font-size: 3rem !important;
                                }
                                input {
                                    font-size: 1.2rem !important;
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
                            limit = st.text_input('Enter The Limit (1-20)')
                            st.write('')
                            st.write('')
                            if int(limit) <= 20 and int(limit) >= 1  :
                                with st.spinner('Please Wait for it...'):
                                    time.sleep(1)
                                    data=trending(int(limit))
                                    st.subheader('Trending')
                                    df=pd.DataFrame(data)
                                    st.dataframe(df,width=800)
                                    #st.success('No of Records   : ' + str(len(df)))
                                    st.latex('Records   : ' + str(len(df)))
                            else:
                                st.warning('Please Enter The Correct Limit !')
                        if radio=='📥 Store Database & Download':
                            st.markdown(
                                """
                                <style>
                                textarea {
                                    font-size: 3rem !important;
                                }
                                input {
                                    font-size: 1.2rem !important;
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,
                            )
                            limit1 = st.text_input('Enter The Limit (1-20)')
                            st.write('')
                            if int(limit1) <= 20 and int(limit1) >= 1  :
                                with st.spinner('Please Wait for it...'):
                                    time.sleep(1)
                                    ndata=trending(int(limit1))
                                    # ndata = trending(int(limit1))
                                dradio = st.radio(' ', ['Store Records in MongoDB', 'Download CSV & JSON File'])
                                if dradio == 'Store Records in MongoDB':
                                    st.write('')
                                    st.write('')
                                    mongodata = ndata
                                    if st.button('🍃 Insert into Mongodb'):
                                        st.write('')
                                        st.write('')
                                        prg = st.progress(0)
                                        for i in range(100):
                                            time.sleep(0.01)
                                            prg.progress(i + 1)
                                        # drop collection
                                        trendingcollection = db.drop_collection('Trending')
                                        # create collection
                                        trendingcollection = db.create_collection('Trending')
                                        for i in ndata:
                                            trendingcollection.insert_one(i)
                                        st.write("")
                                        st.subheader('Record Inserted Successfully !')
                                if dradio == 'Download CSV & JSON File':
                                    trend = []
                                    dom = []
                                    desc = []
                                    for i in range(len(ndata)):
                                        trend.append(ndata[i]['Trend Name'])
                                        dom.append(ndata[i]['Domain'])
                                        desc.append(ndata[i]['Description'])
                                    dic = {'Trend Name': trend, 'Domain': dom, 'Description': desc}
                                    js = json.dumps(dic)
                                    check=os.path.isfile('./Trendtest/my_test.zip')
                                    if check==True:
                                        os.remove('./Trendtest/my_test.zip')
                                    with zipfile.ZipFile('./Trendtest/my_test.zip', 'x') as zip_file:
                                        zip_file.writestr("data1.csv", pd.DataFrame(ndata).to_csv())
                                        zip_file.writestr("data2.json", pd.DataFrame(ndata).to_json())
                                    with open("./Trendtest/my_test.zip", "rb") as file:
                                        st.write('')
                                        st.write('')
                                        st.download_button(
                                            "📚 Download Zip",
                                            data=file,
                                            file_name="mydownload.zip",
                                            mime='application/zip'
                                        )

                            else:
                                st.warning('Please Enter The Correct Limit !')
                except:
                    st.write('')


                                                #SEARCH

            if selected=='Search':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                    <style>
                    .stApp {{
                        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                        background-size: cover
                    }}
                    </style>
                    """,
                        unsafe_allow_html=True
                    )
                add_bg_from_local('Image/Twisearch.jpg')

                try:
                    if "Enter ↵" not in st.session_state:
                        st.session_state["Enter ↵"] = False
                    if "Insert MongoDB" not in st.session_state:
                        st.session_state["Insert MongoDB"] = False
                    st.title('Twitter Tweet Scraper ')
                    st.write('')
                    name = st.text_input('Enter The Keyword or Hashtag  #️⃣')
                    s=st.date_input('Enter The Start Date   📅',value=datetime.date(2023, 4, 5))
                    e = st.date_input('Enter The End Date  📆',value=datetime.date(2023, 4, 2))
                    limit = st.text_input('Enter The limit 1-10000 🔢')
                    n=datetime.date(s.year,s.month,s.day+1)
                    start=n.strftime('%Y-%m-%d')
                    end=e.strftime('%Y-%m-%d')
                    st.write('')
                    if st.button("Enter ↵"):
                        st.session_state["Enter ↵"] = not st.session_state["Enter ↵"]
                    if st.session_state["Enter ↵"]:
                        st.write('')

                        with st.spinner('Please Wait for it...'):
                            time.sleep(0.5)
                            data = tweetsearch(name,start,end,int(limit))
                            st.write('')
                            st.write('')
                            upper=name.upper()
                            st.subheader(r'{} Tweets from ({} to {})'.format(upper,s,end))
                            st.write('')
                            df=pd.DataFrame(data)
                            st.dataframe(data=df,width=800,height=500)
                            st.latex('Records   : ' + str(len(df)))
                        with st.sidebar:
                            radio = st.selectbox('Choose Your Choice ', [ 'CSV', 'JSON'] )
                            st.write('')
                            st.write('')
                            st.write('')
                            if radio == 'CSV':
                                df = pd.DataFrame(data)
                                csv = convertcsv(df)
                                st.write('')
                                st.write('Click to Download CSV File')
                                st.write('')
                                csv=st.download_button('📥 Download', csv, 'Profile.csv', 'text/csv', key='download-csv')
                                st.write('')
                                st.write('')
                                if csv:
                                    with st.spinner('Waiting for Confirmation...'):
                                        time.sleep(0.8)
                                        st.success('Download Successfully ')
                            if radio == 'JSON':
                                js = json.dumps(data)
                                st.write('')
                                st.write('Click to Download JSON File')
                                st.write('')
                                json=st.download_button('📥 Download ', js, 'ProfileJson.json')
                                st.write('')
                                st.write('')
                                if json:
                                    with st.spinner('Waiting for Confirmation...'):
                                        time.sleep(0.8)
                                        st.success('Download Successfully ')
                        st.write('')
                        st.write('')
                        if st.button('📂 Insert MongoDB'):
                            st.write('')
                            st.write('')
                            prg = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                prg.progress(i + 1)
                            # drop collection
                            searchcollection = db.drop_collection('Tweetsearch')
                            # create search collection
                            searchcollection = db.create_collection('Tweetsearch')
                            searchcollection.insert_many(data)
                            st.write('')
                            st.subheader('Record Inserted Successfully !')
                    else:
                        quit()

                except:
                    st.write('')
        except:
            st.warning('Please Enter Your Database Link and Password')

    if choose=='Mongodb Localhost':
        try:
            st.write('')
            dblink = st.text_input('Enter Your Localhost Server')
            client = pymongo.MongoClient(dblink)
            db = client['Database']



            # PROFILE
            if selected == 'Profile':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                            <style>
                            .stApp {{
                                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                                background-size: cover
                            }}
                            </style>
                            """,
                        unsafe_allow_html=True
                    )


                add_bg_from_local('Image/Twipro.jpg')

                try:

                    if " 🚀 Search" not in st.session_state:
                        st.session_state[" 🚀 Search"] = False
                    if "📂 Insert MongoDB" not in st.session_state:
                        st.session_state["📂 Insert MongoDB"] = False
                    st.title('Twitter Profile Scraper ')
                    st.write('')
                    st.write('')
                    name = st.text_input('Enter Your Profile Name ', )
                    st.markdown(
                        """
                        <style>
                        textarea {
                            font-size: 3rem !important;
                        }
                        input {
                            font-size: 1.2rem !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(" 🚀 Search"):
                        st.session_state[" 🚀 Search"] = not st.session_state[" 🚀 Search"]
                    if st.session_state[" 🚀 Search"]:
                        st.write('')
                        st.write('')
                        if len(name) != 0:
                            with st.spinner('Please Wait for it...'):
                                time.sleep(0.5)
                                data = profile(name)
                                st.markdown(r'Profile of **{}**'.format(data[0]['Name']))
                                st.dataframe(data, width=800)
                            with st.sidebar:
                                radio = st.selectbox('Choose Your Choice     ', ['CSV', 'JSON'], )
                                st.write('')
                                st.write('')
                                st.write('')
                                if radio == 'CSV':
                                    df = pd.DataFrame(data)
                                    csv = convertcsv(df)
                                    st.write('')
                                    st.write('Click to Download CSV File')
                                    st.write('')
                                    csv = st.download_button('📥 Download', csv, 'Profile.csv', 'text/csv',
                                                             key='download-csv')
                                    st.write('')
                                    st.write('')
                                    if csv:
                                        with st.spinner('Waiting for Confirmation...'):
                                            time.sleep(0.8)
                                            st.success('Download Successfully ')
                                if radio == 'JSON':
                                    js = json.dumps(data[0])
                                    st.write('')
                                    st.write('Click to Download JSON File')
                                    st.write('')
                                    json = st.download_button('📥 Download ', js, 'ProfileJson.json')
                                    st.write('')
                                    st.write('')
                                    if json:
                                        with st.spinner('Waiting for Confirmation...'):
                                            time.sleep(0.8)
                                            st.success('Download Successfully ')
                            st.write('')
                            st.write('')
                            if st.button(' 📂 Insert MongoDB'):
                                st.write('')
                                st.write('')
                                prg = st.progress(0)
                                for i in range(100):
                                    time.sleep(0.01)
                                    prg.progress(i + 1)

                                st.session_state["📂 Insert MongoDB"] = not st.session_state["📂 Insert MongoDB"]

                                # drop collection
                                profilecollection = db.drop_collection('Profile')
                                # create colletion
                                profilecollection = db.create_collection('Profile')
                                profilecollection.insert_many(data)
                                st.write("")
                                st.subheader('Record Inserted Successfully !')

                    else:
                        quit()
                except:
                    st.write("")

                    # TRENDING

            if selected == 'Trending':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                            <style>
                            .stApp {{
                                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                                background-size: cover
                            }}
                            </style>
                            """,
                        unsafe_allow_html=True
                    )


                add_bg_from_local('Image/Twitrend1.jpg')

                try:
                    st.title('Twitter Trending Scraper')
                    st.write('')
                    radio = st.radio('Choose One Option ', ['👁‍🗨 View Records', '📥 Store Database & Download'])
                    if radio == '👁‍🗨 View Records':
                        st.markdown(
                            """
                            <style>
                            textarea {
                                font-size: 3rem !important;
                            }
                            input {
                                font-size: 1.2rem !important;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )
                        limit = st.text_input('Enter The Limit (1-20)')
                        st.write('')
                        st.write('')
                        if int(limit) <= 20 and int(limit) >= 1:
                            with st.spinner('Please Wait for it...'):
                                time.sleep(1)
                                data = trending(int(limit))
                                st.subheader('Trending')
                                df = pd.DataFrame(data)
                                st.dataframe(df, width=800)
                                # st.success('No of Records   : ' + str(len(df)))
                                st.latex('Records   : ' + str(len(df)))
                        else:
                            st.warning('Please Enter The Correct Limit !')
                    if radio == '📥 Store Database & Download':
                        st.markdown(
                            """
                            <style>
                            textarea {
                                font-size: 3rem !important;
                            }
                            input {
                                font-size: 1.2rem !important;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )
                        limit1 = st.text_input('Enter The Limit (1-20)')
                        st.write('')
                        if int(limit1) <= 20 and int(limit1) >= 1:
                            with st.spinner('Please Wait for it...'):
                                time.sleep(1)
                                ndata = trending(int(limit1))
                                # ndata = trending(int(limit1))
                            dradio = st.radio(' ', ['Store Records in MongoDB', 'Download CSV & JSON File'])
                            if dradio == 'Store Records in MongoDB':
                                st.write('')
                                st.write('')
                                mongodata = ndata
                                if st.button('🍃 Insert into Mongodb'):
                                    st.write('')
                                    st.write('')
                                    prg = st.progress(0)
                                    for i in range(100):
                                        time.sleep(0.01)
                                        prg.progress(i + 1)
                                    # drop collection
                                    trendingcollection = db.drop_collection('Trending')
                                    # create collection
                                    trendingcollection = db.create_collection('Trending')
                                    for i in ndata:
                                        trendingcollection.insert_one(i)
                                    st.write("")
                                    st.subheader('Record Inserted Successfully !')
                            if dradio == 'Download CSV & JSON File':
                                trend = []
                                dom = []
                                desc = []
                                for i in range(len(ndata)):
                                    trend.append(ndata[i]['Trend Name'])
                                    dom.append(ndata[i]['Domain'])
                                    desc.append(ndata[i]['Description'])
                                dic = {'Trend Name': trend, 'Domain': dom, 'Description': desc}
                                js = json.dumps(dic)
                                check = os.path.isfile('./Trendtest/my_test.zip')
                                if check == True:
                                    os.remove('./Trendtest/my_test.zip')
                                with zipfile.ZipFile('./Trendtest/my_test.zip', 'x') as zip_file:
                                    zip_file.writestr("data1.csv", pd.DataFrame(ndata).to_csv())
                                    zip_file.writestr("data2.json", pd.DataFrame(ndata).to_json())
                                with open("./Trendtest/my_test.zip", "rb") as file:
                                    st.write('')
                                    st.write('')
                                    st.download_button(
                                        "📚 Download Zip",
                                        data=file,
                                        file_name="mydownload.zip",
                                        mime='application/zip'
                                    )

                        else:
                            st.warning('Please Enter The Correct Limit !')
                except:
                    st.write('')

                    # SEARCH

            if selected == 'Search':
                def add_bg_from_local(image_file):
                    with open(image_file, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    st.markdown(
                        f"""
                            <style>
                            .stApp {{
                                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                                background-size: cover
                            }}
                            </style>
                            """,
                        unsafe_allow_html=True
                    )


                add_bg_from_local('Image/Twisearch.jpg')

                try:
                    if "Enter ↵" not in st.session_state:
                        st.session_state["Enter ↵"] = False
                    if "Insert MongoDB" not in st.session_state:
                        st.session_state["Insert MongoDB"] = False
                    st.title('Twitter Tweet Scraper ')
                    st.write('')
                    name = st.text_input('Enter The Keyword or Hashtag  #️⃣')
                    s = st.date_input('Enter The Start Date   📅', value=datetime.date(2023, 4, 5))
                    e = st.date_input('Enter The End Date  📆', value=datetime.date(2023, 4, 2))
                    limit = st.text_input('Enter The limit 1-10000 🔢')
                    n = datetime.date(s.year, s.month, s.day + 1)
                    start = n.strftime('%Y-%m-%d')
                    end = e.strftime('%Y-%m-%d')
                    st.write('')
                    if st.button("Enter ↵"):
                        st.session_state["Enter ↵"] = not st.session_state["Enter ↵"]
                    if st.session_state["Enter ↵"]:
                        st.write('')

                        with st.spinner('Please Wait for it...'):
                            time.sleep(0.5)
                            data = tweetsearch(name, start, end, int(limit))
                            st.write('')
                            st.write('')
                            upper = name.upper()
                            st.subheader(r'{} Tweets from ({} to {})'.format(upper, s, end))
                            st.write('')
                            df = pd.DataFrame(data)
                            st.dataframe(data=df, width=800, height=500)
                            st.latex('Records   : ' + str(len(df)))
                        with st.sidebar:
                            radio = st.selectbox('Choose Your Choice ', ['CSV', 'JSON'])
                            st.write('')
                            st.write('')
                            st.write('')
                            if radio == 'CSV':
                                df = pd.DataFrame(data)
                                csv = convertcsv(df)
                                st.write('')
                                st.write('Click to Download CSV File')
                                st.write('')
                                csv = st.download_button('📥 Download', csv, 'Profile.csv', 'text/csv', key='download-csv')
                                st.write('')
                                st.write('')
                                if csv:
                                    with st.spinner('Waiting for Confirmation...'):
                                        time.sleep(0.8)
                                        st.success('Download Successfully ')
                            if radio == 'JSON':
                                js = json.dumps(data)
                                st.write('')
                                st.write('Click to Download JSON File')
                                st.write('')
                                json = st.download_button('📥 Download ', js, 'ProfileJson.json')
                                st.write('')
                                st.write('')
                                if json:
                                    with st.spinner('Waiting for Confirmation...'):
                                        time.sleep(0.8)
                                        st.success('Download Successfully ')
                        st.write('')
                        st.write('')
                        if st.button('📂 Insert MongoDB'):
                            st.write('')
                            st.write('')
                            prg = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                prg.progress(i + 1)
                            # drop collection
                            searchcollection = db.drop_collection('Tweetsearch')
                            # create search collection
                            searchcollection = db.create_collection('Tweetsearch')
                            searchcollection.insert_many(data)
                            st.write('')
                            st.subheader('Record Inserted Successfully !')
                    else:
                        quit()

                except:
                    st.write('')
        except:
            st.warning('Please Enter Your Localhost')
except:
    st.warning('Please Enter Your Database Link')