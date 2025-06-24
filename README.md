# 📈 Price Tracker Scraper

A Python-based web scraper and dashboard to track product prices from [Books to Scrape](https://books.toscrape.com/), log them over time, analyze trends, and visualize the data with a beautiful Streamlit UI.

---

## 🚀 Features

- **Scrape product prices and titles** from any Books to Scrape page (main, category, or product).
- **Multi-page scraping**: Specify how many pages to scrape.
- **Dynamic dashboard**: Enter URLs and page limits directly in the UI.
- **Data logging**: All results are saved to `data/price_log.csv` with timestamps.
- **Automated testing**: Uses `pytest` to ensure scraping logic is robust.
- **Advanced analytics**: Command-line and dashboard analysis (stats, price changes, anomalies, duplicates, and more).
- **Interactive visualizations**: Line charts, bar charts, histograms, and pie charts.
- **CI/CD ready**: GitHub Actions workflow for daily scraping, testing, and artifact upload.

---

## 🗂️ Project Structure

```
price-tracker-scraper/
│
├── scrape.py            # Main scraper (Selenium, Pandas)
├── test_scrape.py       # Pytest-based tests for scraping logic
├── analyze.py           # Command-line analytics and stats
├── dashboard.py         # Streamlit dashboard (UI & analytics)
├── requirements.txt     # All dependencies
├── instruction.txt      # Step-by-step usage instructions
├── data/
│   └── price_log.csv    # Price log (auto-created)
└── .github/
    └── workflows/
        └── scrape.yml   # GitHub Actions workflow
```

---

## ⚡ Quickstart

### 1. **Set Up Your Environment**

```bash
python -m venv venv
# Activate:
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. **Run the Scraper**

```bash
python scrape.py
```
Or use the dashboard for dynamic scraping.

### 3. **Launch the Dashboard**

```bash
streamlit run dashboard.py
```
- Enter any Books to Scrape URL and page limit in the sidebar.
- Explore the Dashboard and Analysis tabs.

### 4. **Analyze Data via CLI (Optional)**

```bash
python analyze.py
# Or with filters:
python analyze.py title=love pricemin=10 pricemax=20
```

### 5. **Run Tests**

```bash
pytest test_scrape.py
```

---

## 🧪 Technologies Used

- **Python 3.8+**
- **Selenium** (web scraping)
- **Pandas** (data handling)
- **Streamlit** (dashboard UI)
- **Pytest** (testing)
- **Matplotlib** (visualizations)
- **GitHub Actions** (CI/CD)

---

## 🛠️ Configuration

Edit the top of `scrape.py` to set:
- `URL` (default: main site, or set to a category/product)
- `PRICE_ALERT_THRESHOLD`
- `PRICE_FILTER_MAX`
- `TITLE_KEYWORD_FILTER`

Or use the dashboard sidebar for dynamic scraping.

---

## 📊 Dashboard Features

- **Dashboard Tab**: Price trends, latest prices, top deals, filters.
- **Analysis Tab**: Advanced stats, price changes, anomalies, duplicates, and multiple chart types.

---

## 🤖 CI/CD

- `.github/workflows/scrape.yml` automates:
  - Dependency install
  - Testing
  - Scraping
  - Artifact upload
  - Daily schedule (customizable)

---

## 📄 License

[MIT License](./LICENSE)

---

## 🙌 Credits

- [Books to Scrape](https://books.toscrape.com/) for the demo data.

---

## 💡 Tips

- For best results, use a fresh virtual environment.
- You can reset your data by deleting `data/price_log.csv`.
- The dashboard is fully interactive—try all the filters and analytics!

---

Happy scraping and analyzing! 🚀 