import streamlit as st
import folium
import webbrowser
import joblib
import pickle
import time
import streamlit.components.v1 as components
import pandas as pd
import help

from streamlit_folium import folium_static

df = pd.read_csv('hospitals.csv', encoding='windows-1252')
ndf = pd.read_csv('ndf.csv')
gdf = pd.read_csv('GovernmentSchemes.csv', encoding='windows-1252')

titlee = '''<h4 style="font-family:timesnewroman;color:#009999;text-align:center;font-size:20px;">MEDIGUIDE 🩺<h4>'''
st.sidebar.write(titlee,unsafe_allow_html=True)

select_boxs = st.sidebar.selectbox('Main Menu',('Home','About','Contact'))

if select_boxs == 'Home':
    user_menu = st.sidebar.radio('Search for',
    ('Main Page','Hospitals in state', 'Hospitals in city', 'Pincode','Take Test','Recommend Medicine','Hospital Location','All government schemes','Government schemes in State')
    )

    if user_menu == 'Main Page':
        st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://cdn.geckoandfly.com/wp-content/uploads/2017/07/health-quotes-08.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True)
     
    if user_menu == 'Hospitals in state':
        st.sidebar.header('State')
        state = help.search_state(df)

        selected_state = st.sidebar.selectbox("Select state", state)

        statewise_hospitals = help.fetch_state_hospital(df, selected_state)
        st.title("Hospitals in " + selected_state)
        st.table(statewise_hospitals[['Hospital','City','LocalAddress']])

    if user_menu == 'Hospitals in city':
        st.sidebar.header('City')
        city = help.search_city(df)

        selected_city = st.sidebar.selectbox("Select state", city)

        citywise_hospitals = help.fetch_city_hospital(df, selected_city)
        st.title("Hospitals in " + selected_city)
        st.table(citywise_hospitals[['Hospital','State','LocalAddress']])

    if user_menu == 'Pincode':
        st.sidebar.header('Pincode')
        pin = help.search_pincode(df)

        selected_pincode = st.sidebar.selectbox("Select Pincode", pin)

        pin_hospitals = help.fetch_pin_hospital(df, selected_pincode)
        st.title("Hospitals with area pincode " + str(int(selected_pincode)))
        st.table(pin_hospitals[['State','City','Hospital','LocalAddress']])

    if user_menu == 'Take Test':
        # loading model and list of symptoms
        model = joblib.load("saved_model/random_f.joblib")
        symptoms_list = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
        st.title("Please enter your symptoms")
        symptoms = st.multiselect('Enter your symptoms so that we can get you a primary diagnosis:',[*symptoms_list],key='symptoms')
        
        # creating dataframe for accepting testing values
        prediction_value = [0 for i in range(132)]
        for sym in symptoms:
            index = symptoms_list.index(sym)
            # assigning encoded value to testing frame
            prediction_value[index] = 1

        # convert list to Pandas dataframe and transpose it for model evaluation
        query = pd.DataFrame(prediction_value).T
        prediction = model.predict(query)
        # evaluation and confirmation
        if st.button("Evaluate"):
            with st.spinner('Predicting output...'):
                time.sleep(1)
            if symptoms:
                st.success("Prediction complete!")
                st.write("The diagnosis we have reached is: ")
                st.info(*prediction)
               
    if user_menu == 'Recommend Medicine':
        medicines = " "
        def recommend(condition):
            drug_index = drugs[drugs['condition'] == condition].index[0]
            distances = similarity[drug_index]
            drug_list = sorted((list(enumerate(distances))), reverse=True, key=lambda x:x[1])[0:5]
            recommended_drugs = []
            for i in drug_list:
                recommended_drugs.append(drugs.iloc[i[0]].drugName)
            return recommended_drugs

        drugs_list = pickle.load(open('drugs_dict.pkl','rb'))
        drugs = pd.DataFrame(drugs_list)

        similarity = pickle.load(open('similarity.pkl','rb'))

        st.title("Drug Recommender ")

        selected_drug_name = st.selectbox(
        "Please select health condition and get medicine recommendation",
        drugs['condition'].values)

        if st.button('Recommend'):
            recommendation = recommend(selected_drug_name)
            for i in recommendation:
                medicines = medicines+"\n"+i
                st.info(i)
            st.download_button('Download Medicines List',medicines)

    
    if user_menu == 'Hospital Location':
        st.sidebar.header('Hospital')
        hospital = help.search_hospital(df)

        selected_hospital = st.sidebar.selectbox("Select Hosptial", hospital)
        hospitals = help.fetch_hospital(df, selected_hospital)
        st.title(selected_hospital+', '+hospitals['City']+', '+hospitals['State'])
        lat = hospitals['latutude'].astype(float, errors = 'raise')
        lon = hospitals['longitude'].astype(float, errors = 'raise')
        radius = 3
        m = folium.Map(location=[lat, lon], zoom_start=20, tiles='OpenStreetMap')
        folium.Marker([lat, lon]).add_to(m)
        folium.Circle([lat, lon], radius=radius).add_to(m)  # radius is in meters
        folium_static(m)
    # st.title("Hospitals with area pincode " + str(int(selected_pincode)))
    # st.table(pin_hospitals[['State', 'City', 'Hospital']])


    if user_menu == 'All government schemes':
        st.sidebar.header('All government schemes in India')
        allGS = help.search_allgs(gdf)

        allGovschemes = help.fetch_all_govschemes(gdf)
        st.title("All the government schemes in India")
        st.table(allGovschemes[['State','Scheme','Details','Eligibility','Website/Apply at']])

    if user_menu == 'Government schemes in State':
        st.sidebar.header('Government schemes')
        sgs = help.search_stategs(gdf)

        selected_stategs = st.sidebar.selectbox("Select state", sgs)

        statewise_gs = help.fetch_state_gs(gdf, selected_stategs)
        st.title("Government schemes in " + selected_stategs)
        st.table(statewise_gs[['Scheme','Details','Eligibility','Website/Apply at']])

if select_boxs == 'About':
    st.markdown(f"""
         <style>
         .stApp {{
             background: url("https://cdn.wallpapersafari.com/13/96/XkD4cw.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True)
    st.markdown(f'<h4 style="color:lightseagreen;font-size:42px;text-align:center"><br><b>MediGuide<b><h4>',unsafe_allow_html=True)
    st.markdown(f'<p style="color:#0080FF;font-size:20px;">MediGuide is a web application that helps you in searching for a hospital in a state, city, and using pincode. <br>Have any health problem? Does not know what disease you are suffering with? Here we are! Enter your symptoms we will predict your health condition and recommend you a medicine!<br> <p>',unsafe_allow_html=True)
    st.markdown(f'<h2 style="text-align:center;font-family:papyrus;color:#FF3333;font-size:50px;"><i>Health is Wealth!<i><h2>',unsafe_allow_html=True)

if select_boxs == 'Contact':
    st.markdown(f"""
         <style>
         .stApp {{
             background: url("https://www.idfreshfood.com/wp-content/uploads/2017/09/contact_us_2.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True)
    pname = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> <br>
    <i class="fa fa-user" style="font-size:30px;color:lightseagreen">    <b>Gayathri Reddy<b></i><br><br>'''
    st.write(pname,unsafe_allow_html=True)
    gmail = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> 
    <i class="fa fa-envelope" style="font-size:25px;color:lightseagreen">     <b>gayathrireddykalthireddy@gmail.com<b></i><br><br>'''
    st.write(gmail,unsafe_allow_html=True)
    phno = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> 
    <i class="fa fa-mobile" style="font-size:40px;color:lightseagreen">     7898108163</i><br>'''
    st.write(phno,unsafe_allow_html=True)