import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
# --- CONFIG ---
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://gnews.io/api/v4/search"

st.title("Redazione Palestina")

query = "palestine"
language = "en"
start_date = datetime.today() - timedelta(days=1)
end_date = datetime.today()

if st.button("Fetch News"):
    from_iso = start_date.isoformat()
    to_iso = end_date.isoformat()

    params = {
        "q": query,
        "token": API_KEY,
        "lang": language,
        "from": from_iso,
        "to": to_iso,
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if articles:
            df = pd.DataFrame(articles)
            df = df[["title", "description", "publishedAt", "source", "url"]]
            df["publishedAt"] = pd.to_datetime(df["publishedAt"])
            st.dataframe(df)
            st.success(f"Found {len(df)} articles.")
        else:
            st.warning("No articles found for your filters.")
    else:
        st.error("Failed to fetch articles. Check your API key or query.")