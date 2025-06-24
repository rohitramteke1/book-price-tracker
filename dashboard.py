import streamlit as st
import pandas as pd
import os
from datetime import datetime
import subprocess
import sys
import matplotlib.pyplot as plt

CSV_PATH = os.path.join("data", "price_log.csv")

def load_data():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        return df
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def main():
    st.set_page_config(page_title="Book Price Tracker Dashboard", layout="wide")
    st.title("📚 Book Price Tracker Dashboard")

    df = load_data()

    st.sidebar.header("Filters")
    min_price, max_price = (float(df['price'].min()), float(df['price'].max())) if not df.empty else (0, 100)
    price_range = st.sidebar.slider("Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))
    title_search = st.sidebar.text_input("Search Title")
    if not df.empty:
        date_min, date_max = df['timestamp'].min(), df['timestamp'].max()
    else:
        date_min, date_max = datetime.now(), datetime.now()
    date_range = st.sidebar.date_input("Date Range", [date_min, date_max])

    st.sidebar.header("Scraper Controls")
    def_url = "https://books.toscrape.com/"
    user_url = st.sidebar.text_input(
        "Enter a Books to Scrape URL",
        value=def_url
    )
    page_limit = st.sidebar.number_input("Max pages to scrape", min_value=1, value=1, step=1)
    if st.sidebar.button("Scrape Now"):
        subprocess.run([sys.executable, "scrape.py", user_url, str(page_limit)])
        st.success(f"Scraping complete for up to {page_limit} page(s)! Refresh to see new data.")

    tab1, tab2 = st.tabs(["📊 Dashboard", "🧮 Analysis"])

    # --- Dashboard Tab ---
    with tab1:
        if df.empty:
            st.warning("No data in price log.")
        else:
            filtered = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
            if title_search:
                filtered = filtered[filtered['title'].str.contains(title_search, case=False)]
            filtered = filtered[(filtered['timestamp'].dt.date >= date_range[0]) & (filtered['timestamp'].dt.date <= date_range[1])]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Books Logged", len(filtered))
            col2.metric("Avg Price", f"£{filtered['price'].mean():.2f}" if not filtered.empty else "-")
            col3.metric("Lowest Price", f"£{filtered['price'].min():.2f}" if not filtered.empty else "-")
            col4.metric("Highest Price", f"£{filtered['price'].max():.2f}" if not filtered.empty else "-")

            st.markdown("---")
            st.subheader("📈 Price Over Time")
            st.line_chart(filtered.set_index('timestamp')['price'])

            st.subheader("🔍 Latest 10 Prices")
            st.dataframe(filtered.sort_values('timestamp', ascending=False).head(10), use_container_width=True)

            st.markdown("---")
            st.subheader("💸 Top Deals (Under £20)")
            deals = filtered[filtered['price'] < 20]
            if not deals.empty:
                st.table(deals.sort_values('price').head(10)[['timestamp', 'title', 'price']])
            else:
                st.info("No top deals found under £20.")

    # --- Analysis Tab ---
    with tab2:
        if df.empty:
            st.warning("No data in price log.")
        else:
            st.header("Advanced Analytics")
            st.markdown("---")
            st.subheader("Summary Statistics")
            st.write(f"**Mean price:** £{df['price'].mean():.2f}")
            st.write(f"**Median price:** £{df['price'].median():.2f}")
            st.write(f"**Std deviation:** £{df['price'].std():.2f}")
            st.write(f"**Unique titles:** {df['title'].nunique()}")
            st.write(f"**Total entries:** {len(df)}")

            st.markdown("---")
            st.subheader("Top 5 Cheapest Books")
            st.dataframe(df.nsmallest(5, 'price')[['title', 'price', 'timestamp']])
            st.subheader("Top 5 Most Expensive Books")
            st.dataframe(df.nlargest(5, 'price')[['title', 'price', 'timestamp']])

            st.markdown("---")
            st.subheader("Books with Price Changes (since previous log)")
            df_sorted = df.sort_values(['title', 'timestamp'])
            df_sorted['prev_price'] = df_sorted.groupby('title')['price'].shift(1)
            df_sorted['price_change'] = df_sorted['price'] - df_sorted['prev_price']
            changed = df_sorted[df_sorted['price_change'].notnull() & (df_sorted['price_change'] != 0)]
            if not changed.empty:
                st.dataframe(changed[['title', 'timestamp', 'prev_price', 'price', 'price_change']])
            else:
                st.info("No price changes detected.")

            st.markdown("---")
            st.subheader("Biggest Price Drop")
            if not changed.empty:
                drop = changed.nsmallest(1, 'price_change')
                st.dataframe(drop[['title', 'timestamp', 'prev_price', 'price', 'price_change']])
            else:
                st.info("No price drops detected.")

            st.subheader("Biggest Price Increase")
            if not changed.empty:
                inc = changed.nlargest(1, 'price_change')
                st.dataframe(inc[['title', 'timestamp', 'prev_price', 'price', 'price_change']])
            else:
                st.info("No price increases detected.")

            st.markdown("---")
            st.subheader("Daily Price Trends (min, max, mean)")
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            daily = df.groupby('date')['price'].agg(['min', 'max', 'mean', 'count'])
            st.dataframe(daily)

            st.markdown("---")
            st.subheader("Price Anomaly Detection (prices outside 2 std dev)")
            mean_price = df['price'].mean()
            std_price = df['price'].std()
            lower_bound = mean_price - (2 * std_price)
            upper_bound = mean_price + (2 * std_price)
            anomalies = df[(df['price'] < lower_bound) | (df['price'] > upper_bound)]
            if not anomalies.empty:
                st.dataframe(anomalies[['title', 'price', 'timestamp']])
            else:
                st.info("No price anomalies detected.")

            st.markdown("---")
            st.subheader("Duplicate Entry Detection")
            duplicates = df[df.duplicated(subset=['timestamp', 'title', 'price'], keep=False)]
            if not duplicates.empty:
                st.dataframe(duplicates)
            else:
                st.info("No duplicate entries found.")

            st.markdown("---")
            st.subheader("Price Distribution Histogram")
            st.bar_chart(df['price'])

            st.subheader("Price by Book (Top 20)")
            top20 = df.groupby('title')['price'].mean().nlargest(20)
            st.bar_chart(top20)

            st.subheader("Price Distribution Pie Chart (by Price Range)")
            bins = [0, 20, 40, 60, 100]
            labels = ['<£20', '£20-£40', '£40-£60', '£60+']
            df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)
            pie_data = df['price_range'].value_counts().sort_index()

            # Remove zero-count bins
            pie_data_nonzero = pie_data[pie_data > 0]
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.pie(pie_data_nonzero, labels=pie_data_nonzero.index, autopct='%1.1f%%', textprops={'fontsize': 10})
            ax.set_ylabel('')
            ax.axis('equal')
            st.pyplot(fig)

if __name__ == "__main__":
    main() 