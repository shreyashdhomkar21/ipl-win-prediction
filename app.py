import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals', 'Gujarat Titans',
         'Lucknow Super Giants']

cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
        'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
        'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore',
        'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
        'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
        'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    Batting_team = st.selectbox('Select the Batting team', teams)

with col2:
    Bowling_team = st.selectbox('Select the Bowling team', teams)

selected_city = st.selectbox('Select host city', sorted(cities))

target = int(st.number_input('Target', step=1))

col3, col4, col5 = st.columns(3)

with col3:
    score = int(st.number_input('Score', step=1))


with col4:
    overs = st.number_input('Overs completed', format="%.1f", step=0.1)
    if overs:
        overs_int = int(overs)
        overs_decimal = round(overs % 1, 1)
        if overs_decimal < 0.91:
            a = round(overs_decimal / 0.18)
            b = round(a * 0.1, 1)
            c = overs_int + b
        else:
            c = overs_int + 1
        overs_modified = f"{c}"
        overs = st.number_input('Overs completed', format="%.1f", value=float(overs_modified))

with col5:
    wickets = st.number_input('Wickets out', step=1)
if st.button('Predict Probability'):
    if score >= 0 and target >= 0 and score < target:
        if overs >= 0 and overs < 20:
            if wickets >= 0 and wickets < 10:
                if Batting_team != Bowling_team:
                    runs_left = target - score
                    balls_left = 120 - (overs * 6)
                    wickets_left = 10 - wickets
                    crr = score / overs
                    rrr = (runs_left * 6) / balls_left

                    input_df = pd.DataFrame({
                        'BattingTeam': [Batting_team],
                        'Bowling Team_x': [Bowling_team],
                        'City': [selected_city],
                        'runs_left': [runs_left],
                        'balls_left': [balls_left],
                        'wickets_left': [wickets_left],
                        'total_run_x': [target],
                        'crr': [crr],
                        'rrr': [rrr]
                    })

                    result = pipe.predict_proba(input_df)
                    loss = result[0][0]
                    win = result[0][1]
                    st.header(Batting_team + "- " + str(round(win*100)) + "%")
                    st.header(Bowling_team + "- " + str(round(loss*100)) + "%")
                else:
                    st.warning("Batting team and Bowling team should be different.")
            else:
                st.warning("The number of wickets should be less than 10 and not less than 0.")
        else:
            st.warning("Overs should not less than 0 and not be greater than 20.")
    else:
        st.warning("Please ensure that the score is not less than 0 and not equal to and greater than the target. target is not less than 0.")
