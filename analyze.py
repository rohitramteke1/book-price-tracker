import pandas as pd
import os
import sys

CSV_PATH = os.path.join("data", "price_log.csv")

def main():
    # Command-line filters
    title_filter = None
    price_min = None
    price_max = None
    date_start = None
    date_end = None
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('title='):
                title_filter = arg.split('=', 1)[1].strip().lower()
            elif arg.startswith('pricemin='):
                price_min = float(arg.split('=', 1)[1])
            elif arg.startswith('pricemax='):
                price_max = float(arg.split('=', 1)[1])
            elif arg.startswith('datestart='):
                date_start = arg.split('=', 1)[1]
            elif arg.startswith('dateend='):
                date_end = arg.split('=', 1)[1]

    if not os.path.exists(CSV_PATH):
        print("No price log found.")
        return
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        print("No data in price log.")
        return
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Apply filters
    if title_filter:
        df = df[df['title'].str.lower().str.contains(title_filter)]
    if price_min is not None:
        df = df[df['price'] >= price_min]
    if price_max is not None:
        df = df[df['price'] <= price_max]
    if date_start:
        df = df[df['timestamp'] >= pd.to_datetime(date_start)]
    if date_end:
        df = df[df['timestamp'] <= pd.to_datetime(date_end)]

    print("--- Price Statistics ---")
    print(f"Mean price: {df['price'].mean():.2f}")
    print(f"Min price: {df['price'].min():.2f}")
    print(f"Max price: {df['price'].max():.2f}")
    print(f"Median price: {df['price'].median():.2f}")
    print(f"Std deviation: {df['price'].std():.2f}")
    print(f"Unique titles: {df['title'].nunique()}")
    print(f"Total entries: {len(df)}")
    print("\n--- Latest 5 Logs ---")
    df_sorted = df.sort_values('timestamp', ascending=False)
    print(df_sorted.head(5).to_string(index=False))

    print("\n--- Top 5 Cheapest Books ---")
    print(df.nsmallest(5, 'price')[['title', 'price', 'timestamp']].to_string(index=False))

    print("\n--- Top 5 Most Expensive Books ---")
    print(df.nlargest(5, 'price')[['title', 'price', 'timestamp']].to_string(index=False))

    # Price change detection
    print("\n--- Books with Price Changes (since previous log) ---")
    df_sorted = df.sort_values(['title', 'timestamp'])
    df_sorted['prev_price'] = df_sorted.groupby('title')['price'].shift(1)
    df_sorted['price_change'] = df_sorted['price'] - df_sorted['prev_price']
    changed = df_sorted[df_sorted['price_change'].notnull() & (df_sorted['price_change'] != 0)]
    if not changed.empty:
        print(changed[['title', 'timestamp', 'prev_price', 'price', 'price_change']].to_string(index=False))
    else:
        print("No price changes detected.")

    # Biggest price drop/increase
    print("\n--- Biggest Price Drop ---")
    if not changed.empty:
        drop = changed.nsmallest(1, 'price_change')
        print(drop[['title', 'timestamp', 'prev_price', 'price', 'price_change']].to_string(index=False))
    else:
        print("No price drops detected.")

    print("\n--- Biggest Price Increase ---")
    if not changed.empty:
        inc = changed.nlargest(1, 'price_change')
        print(inc[['title', 'timestamp', 'prev_price', 'price', 'price_change']].to_string(index=False))
    else:
        print("No price increases detected.")

    # Time series trends: min, max, mean price per day
    print("\n--- Daily Price Trends (min, max, mean) ---")
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily = df.groupby('date')['price'].agg(['min', 'max', 'mean', 'count'])
    print(daily.to_string())

    # Anomaly Detection: prices outside 2 standard deviations
    print("\n--- Price Anomaly Detection (prices outside 2 std dev) ---")
    mean_price = df['price'].mean()
    std_price = df['price'].std()
    lower_bound = mean_price - (2 * std_price)
    upper_bound = mean_price + (2 * std_price)
    anomalies = df[(df['price'] < lower_bound) | (df['price'] > upper_bound)]
    if not anomalies.empty:
        print(anomalies[['title', 'price', 'timestamp']].to_string(index=False))
    else:
        print("No price anomalies detected.")

    # Duplicate Detection
    print("\n--- Duplicate Entry Detection ---")
    duplicates = df[df.duplicated(subset=['timestamp', 'title', 'price'], keep=False)]
    if not duplicates.empty:
        print(duplicates.to_string(index=False))
    else:
        print("No duplicate entries found.")

if __name__ == "__main__":
    main() 