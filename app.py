import streamlit as st
import requests
import pandas as pd

def fetch_users(status):
    """Fetches users based on status from the API and returns a DataFrame with specific headers."""
    url = f"https://crates.zero1byzerodha.com/users/list?status={status}"
    headers = {
        'Authorization': 'Bearer CIkam6eUXoOmeSYHrZTJ6kKdpH1y4ZdkdzO9XyusJpNNqYxOxq'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Convert data to DataFrame with predefined columns
        if isinstance(data, dict):
            data = [data]  # Ensure data is in list format

        df = pd.DataFrame(data)
        # Define columns even if they are missing in the response
        columns = ['age', 'email', 'phoneNumber', 'status', 'userLocation']
        # Reindex DataFrame to include all required columns, fill missing with None or appropriate defaults
        df = df.reindex(columns=columns, fill_value=pd.NA)
        return df
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
