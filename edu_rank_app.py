import streamlit as st
import pandas as pd
import numpy as np

# Function to perform MOORA ranking
def moora(data, weights):
    # Normalize the data (min-max normalization)
    normalized_data = data.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    # Multiply by weights
    weighted_data = normalized_data * weights
    
    # Calculate the MOORA Ratio (sum of weighted normalized values)
    moora_score = weighted_data.sum(axis=1)
    
    # Ranking based on the highest MOORA score
    data['MOORA Score'] = moora_score
    data['Rank'] = data['MOORA Score'].rank(ascending=False)
    
    return data

# Streamlit app UI
st.title("EduRank: A MOORA-based Big Data System for Evaluating Educational Technologies")

st.write("""
This application allows you to evaluate and rank different educational technologies using the MOORA method.
You will input the data for various educational tools and their criteria, then the system will calculate the ranks based on a multi-criteria decision-making process.
""")

# Input for the number of technologies
num_technologies = st.number_input("Number of Educational Technologies", min_value=1, step=1, value=3)

# Define the criteria
criteria = ['Cost', 'Ease of Use', 'Effectiveness', 'Accessibility', 'Innovation']

# Initialize a list to hold the technology data
technology_data = []

# Collect input for each technology
with st.form(key='technology_form'):
    for i in range(num_technologies):
        technology_name = st.text_input(f"Technology Name {i+1}", key=f"tech_name_{i}")
        cost = st.number_input(f"Cost for {technology_name}", min_value=0.0, step=0.1, key=f"cost_{i}")
        ease_of_use = st.number_input(f"Ease of Use for {technology_name}", min_value=0.0, step=0.1, key=f"ease_{i}")
        effectiveness = st.number_input(f"Effectiveness for {technology_name}", min_value=0.0, step=0.1, key=f"effectiveness_{i}")
        accessibility = st.number_input(f"Accessibility for {technology_name}", min_value=0.0, step=0.1, key=f"accessibility_{i}")
        innovation = st.number_input(f"Innovation for {technology_name}", min_value=0.0, step=0.1, key=f"innovation_{i}")

        # Add input data to the list
        technology_data.append({
            'Technology': technology_name,
            'Cost': cost,
            'Ease of Use': ease_of_use,
            'Effectiveness': effectiveness,
            'Accessibility': accessibility,
            'Innovation': innovation
        })

    # Submit button for the form
    submitted = st.form_submit_button("Submit")

# Once the form is submitted, process the data
if submitted and technology_data:
    # Create DataFrame from input data
    technologies = pd.DataFrame(technology_data)

    st.write("### Input Data for Technologies")
    st.write(technologies)

    # Weighting for each criteria (can be adjusted by the user)
    weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  # Sum of weights should equal 1

    # Apply MOORA method to rank the technologies
    ranked_data = moora(technologies[criteria], weights)

    st.write("### Ranking Based on MOORA Method")
    st.write(ranked_data[['Technology', 'MOORA Score', 'Rank']])
