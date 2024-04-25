import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from enum import Enum

class UserStatus(Enum):
    REJECTED = 'REJECTED'
    WAITLISTED = 'WAITLISTED'
    CLAIMED = 'CLAIMED'
    SELECTED = 'SELECTED'
    REJECTED_WITH_MERCH = 'REJECTED_WITH_MERCH'

def fetch_data(url, status=None):
    """Fetch data from the API and return a DataFrame."""
    headers = {
        'authorization': 'Bearer d011a53f5413423fceaf0bf8e9db78dde18dff63'
    }
    # Add query parameter if status is selected
    if status:
        url += f"?status={status}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return pd.json_normalize(data, 'users')

def main():
    st.title('⚡ User Data')

    # URL without status parameter
    url = "https://crates.zero1byzerodha.com/users/list"

    # Dropdown to select status or no filter
    status = st.selectbox('Select User Status or Choose None to fetch all:', [None] + list(UserStatus))

    if st.button('Fetch Data'):
        with st.spinner('Fetching data...'):
            # Convert status to the string value if not None
            status_value = status.value if status else None
            df = fetch_data(url, status=status_value)
            # Display total number of records fetched
            

          # st.balloons()
                
           

            
            
            # Creating two columns for side by side display
            col1, col2, col3 = st.columns(3)
            
            # Display value counts for rsvpAccepted in the first column
            if 'rsvpAccepted' in df.columns:
                rsvp_accepted_counts = df['rsvpAccepted'].value_counts()
                with col1:
                    st.write("Value counts for RSVP Accepted:")
                    st.write(rsvp_accepted_counts)
            
            # Display value counts for plusOne in the second column
            if 'plusOne' in df.columns:
                plus_one_counts = df['plusOne'].value_counts()
                with col2:
                    st.write("Value counts for plusOne:")
                    st.write(plus_one_counts)

                # Get count of 'True' from rsvp_accepted_counts and 'Y' from plus_one_counts
                true_count = rsvp_accepted_counts.get(True, 0)  # Defaults to 0 if 'True' not present
                y_count = plus_one_counts.get('Y', 0)          # Defaults to 0 if 'Y' not present
            
                # Calculate the sum of these specific values
                total_count = true_count + y_count
                with col3:
                    # Display the result
                    st.write("Total Fest Participants 🧑‍🤝‍🧑")
                    st.title(total_count) 
                
            
            # Calculate and display value counts for isWaitlistCom
         #   if 'isWaitlistCom' in df.columns:
              #  waitlist_com_counts = df['isWaitlistCom'].value_counts()
              #  st.write("Value counts for isWaitlistCom:")
               #  st.write(waitlist_com_counts)

            # Calculate and display value counts for isPlusOneSent
         #   if 'isPlusOneSent' in df.columns:
             #   plus_one_sent_counts = df['isPlusOneSent'].value_counts()
             #   st.write("Value counts for isPlusOneSent:")
             #   st.write(plus_one_sent_counts)
            
            st.write(f"Total records fetched: {len(df)}")
            st.write(df)

            # Creating a histogram for the "age" column
            fig, ax = plt.subplots()
            ax.hist(df['age'], bins=20, color='skyblue', edgecolor='black')
            ax.set_title('Age Distribution')
            ax.set_xlabel('Age')
            ax.set_ylabel('Frequency')
            ax.grid(True)
            
            # Display the plot in Streamlit
            st.pyplot(fig)
            
            # Calculate and display value counts for acceptanceReason
            if 'acceptanceReason' in df.columns:
                st.write("Value counts for each Acceptance Reason:")
                acceptance_counts = df['acceptanceReason'].value_counts()
                st.write(acceptance_counts)

        #    st.snow()
            # Generate download link for the DataFrame
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="user_data.csv",
                mime="text/csv",
                key='download-csv'
            )
    else:
                st.write("No data found for the selected status.")

if __name__ == "__main__":
    main()
