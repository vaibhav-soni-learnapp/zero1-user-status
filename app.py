import streamlit as st
import pandas as pd
import requests
from enum import Enum

class UserStatus(Enum):
    REJECTED = 'REJECTED'
    WAITLISTED = 'WAITLISTED'
    CLAIMED = 'CLAIMED'
    SELECTED = 'SELECTED'

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
            st.write(df)

            # Display total number of records fetched
            st.write(f"Total records fetched: {len(df)}")
                
           

            # Assuming df is your DataFrame

            # Calculate and display value counts for rsvpAccepted
            if 'rsvpAccepted' in df.columns:
                rsvp_accepted_counts = df['rsvpAccepted'].value_counts()
                st.write("Value counts for RSVP Accepted:")
                st.write(rsvp_accepted_counts)
            
            # Calculate and display value counts for isPlusOneSent
            if 'isPlusOneSent' in df.columns:
                plus_one_sent_counts = df['isPlusOneSent'].value_counts()
                st.write("Value counts for isPlusOneSent:")
                st.write(plus_one_sent_counts)
            
            
            
            # Calculate and display value counts for plusOne
            if 'plusOne' in df.columns:
                plus_one_counts = df['plusOne'].value_counts()
                st.write("Value counts for plusOne:")
                st.write(plus_one_counts)
            
            # Calculate and display value counts for isWaitlistCom
            if 'isWaitlistCom' in df.columns:
                waitlist_com_counts = df['isWaitlistCom'].value_counts()
                st.write("Value counts for isWaitlistCom:")
                st.write(waitlist_com_counts)

            
            # Calculate and display value counts for acceptanceReason
            if 'acceptanceReason' in df.columns:
                st.write("Value counts for each Acceptance Reason:")
                acceptance_counts = df['acceptanceReason'].value_counts()
                st.write(acceptance_counts)

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
