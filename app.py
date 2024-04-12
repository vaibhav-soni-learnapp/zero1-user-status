import streamlit as st
import requests
import pandas as pd

def fetch_users(status):
    """Fetches users based on status from the API and returns a DataFrame."""
    url = f"https://crates.dev.zero1byzerodha.com/users/list?status={status}"
    headers = {
        'Authorization': 'Bearer CIkam6eUXoOmeSYHrZTJ6kKdpH1y4ZdkdzO9XyusJpNNqYxOxq'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Check if data is a list or a single dict
        if isinstance(data, dict):
            # Convert single dict to DataFrame
            data = [data]  # Convert dict to list of dicts
        # Convert list of dicts to DataFrame
        return pd.DataFrame(data)
    else:
        return pd.DataFrame({'Error': ['Failed to fetch data'], 'Status Code': [response.status_code]})

def main():
    """Main function for the Streamlit app."""
    st.title('User Status Dashboard')

    user_status = st.selectbox(
        "Select User Status",
        options=["ACCEPTED", "REJECTED", "WAITLISTED", "CLAIMED", "SELECTED"],
        index=3  # Default to CLAIMED as an example
    )

    if st.button('Fetch Users'):
        with st.spinner('Fetching data...'):
            data = fetch_users(user_status)
            if 'Error' in data.columns:
                st.error(f"Error: {data.iloc[0]['Error']} (Status code: {data.iloc[0]['Status Code']})")
            else:
                # Displaying the DataFrame in Streamlit with all headers
                st.dataframe(data)

if __name__ == "__main__":
    main()
