import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Streamlit UI
st.title("🔥 Meme Coin Tweet Scraper 🪙🚀")

st.markdown("Find the latest trending tweets about meme coins!")

# User input fields
keyword = st.text_input("Enter keywords (default: meme coin, dogecoin, shiba inu)", "meme coin OR dogecoin OR shiba inu")
min_likes = st.number_input("Minimum Likes", min_value=0, value=50)
min_retweets = st.number_input("Minimum Retweets", min_value=0, value=20)
num_tweets = st.slider("Number of Tweets", 10, 500, 100)

if st.button("Fetch Tweets"):
    query = f"{keyword} min_faves:{min_likes} min_retweets:{min_retweets} since:2024-01-01"

    # Fetch tweets
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= num_tweets:
            break
        tweets.append([tweet.date, tweet.user.username, tweet.content, tweet.likeCount, tweet.retweetCount, tweet.url])

    # Convert to DataFrame
    df = pd.DataFrame(tweets, columns=["Date", "Username", "Tweet", "Likes", "Retweets", "Link"])

    if not df.empty:
        st.success(f"✅ Found {len(df)} tweets!")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "meme_coin_tweets.csv", "text/csv")
    else:
        st.warning("⚠️ No tweets found. Try adjusting the filters!")
