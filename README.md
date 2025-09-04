---

# 📊 Zomato Review Trends Analysis

This project analyzes **Zomato app reviews from Google Play Store**, extracts **topics using an LLM (OpenAI GPT models)**, **clusters similar topics using embeddings**, and finally generates a **trend table** showing how topics evolve over time.

The code is modularized into separate Python files for **readability**, **maintainability**, and **ease of contribution**.

---

## ⚙️ How It Works — Data Flow Overview

Here’s how data flows across the files:

```
fetch_reviews.py ──► topic_extraction.py ──► clustering.py ──► trend_analysis.py ──► CSV output
```

Step-by-step explanation:

1. **Fetch Reviews (`fetch_reviews.py`)**

   * Uses `google-play-scraper` to download reviews of the Zomato app.
   * Filters them by a given **date range** (configured in `config.py`).
   * Groups reviews **by date** so that we can later analyze daily trends.
   * **Output:**

     ```python
     {
       "2025-05-25": ["Food delivery was late", "Great app!"],
       "2025-05-26": ["Payment issues", "UI is confusing"]
     }
     ```
   * This dictionary (`daily_reviews`) is passed to `topic_extraction.py`.

---

2. **Extract Topics (`topic_extraction.py`)**

   * Takes `daily_reviews` from the previous step.
   * Sends each review text to **OpenAI GPT-3.5-turbo**.
   * The model summarizes each review into a **short topic label** (e.g., `"Late delivery"`, `"Payment issue"`, `"UI/UX problem"`).
   * Groups extracted topics **per date**.
   * **Output:**

     ```python
     {
       "2025-05-25": ["Late delivery", "Positive feedback"],
       "2025-05-26": ["Payment issue", "UI/UX problem"]
     }
     ```
   * This dictionary (`daily_topics`) is passed to `clustering.py`.

---

3. **Cluster Topics (`clustering.py`)**

   * Takes `daily_topics` and collects all **unique topics** across dates.
   * Calls OpenAI’s **embedding model** (`text-embedding-3-small`) to generate vectors for each topic.
   * Uses **cosine similarity** to group topics that are **semantically similar** (e.g., `"Late delivery"` and `"Delivery delay"` are clustered into the same group).
   * Creates a `cluster_map` that maps each original topic → its cluster representative.
   * **Output:**

     ```python
     {
       "Late delivery": "Delivery issue",
       "Delivery delay": "Delivery issue",
       "Payment issue": "Payment issue",
       "UI/UX problem": "UI/UX problem"
     }
     ```
   * This `cluster_map` is passed along with `daily_topics` to `trend_analysis.py`.

---

4. **Trend Analysis (`trend_analysis.py`)**

   * Replaces all topics in `daily_topics` with their **cluster representative** (using `cluster_map`).
   * Counts how many times each cluster-topic occurs **per day**.
   * Builds a **trend matrix (Pandas DataFrame)** with rows = topics, columns = dates, values = frequency counts.
   * Saves the trend matrix as a **CSV file** (`zomato_review_trends.csv`).
   * **Output Example (CSV):**

     | Topic          | 2025-05-24 | 2025-05-25 | 2025-05-26 | 2025-05-27 | ... |
     | -------------- | ---------- | ---------- | ---------- | ---------- | --- |
     | Delivery issue | 0          | 2          | 1          | 0          | ... |
     | Payment issue  | 0          | 0          | 3          | 1          | ... |
     | UI/UX problem  | 0          | 1          | 1          | 2          | ... |

---

5. **Main Orchestrator (`main.py`)**

   * Connects all the steps together.
   * Execution flow:

     * Calls `fetch_reviews()` → returns raw reviews.
     * Calls `get_daily_topics()` → returns extracted topic labels.
     * Calls `cluster_topics()` → returns cluster mapping.
     * Calls `consolidate_topics()` + `generate_trend_table()` → outputs final CSV.
   * Prints the **first few rows of the DataFrame** so you can quickly inspect results.

---

## 📂 File Structure

```
zomato-review-trends/
│── README.md              # Full explanation of the project
│── requirements.txt       # Dependencies
│── main.py                # Orchestrator script
│
├── config.py              # Configurations (dates, app_id, models, thresholds)
├── fetch_reviews.py       # Fetch and group reviews
├── topic_extraction.py    # Extract topics using GPT
├── clustering.py          # Cluster similar topics using embeddings
├── trend_analysis.py      # Generate trend CSV
└── utils.py               # Helper functions (optional, currently not used)
```

---

## 🔑 Configuration

You can configure the project in `config.py`:

* **App ID:** Which Play Store app to fetch reviews for.
* **Date Range:** Start and end date for fetching reviews.
* **Trend Window:** How many days to generate trend tables for.
* **Models:** Which GPT and embedding models to use.
* **Similarity Threshold:** How strict clustering should be.

---

## 🚀 Running the Project

1. **Clone the repo and install dependencies:**

   ```bash
   git clone https://github.com/yourusername/zomato-review-trends.git
   cd zomato-review-trends
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

   *(On Windows PowerShell use `setx OPENAI_API_KEY "your_api_key_here"`)*

3. **Run the pipeline:**

   ```bash
   python main.py
   ```

4. **Check the output:**

   * Console will show first 5 rows of the trend DataFrame.
   * CSV file `zomato_review_trends.csv` will be saved in the repo folder.

---

## 📊 Example Workflow

* Review: `"Delivery guy was rude"` → Extracted Topic: `"Delivery issue"`
* Review: `"Order arrived late"` → Extracted Topic: `"Delivery delay"`
* Clustering groups both into `"Delivery issue"`.
* Trend table shows how **Delivery issues** trend over multiple days.

---

## 🧩 Why Modularized?

Instead of one big notebook/script, we split the logic into **separate files**:

* Easier to **test/debug** each step independently.
* Easier to **extend** (e.g., switch LLM, change clustering method).
* Cleaner for **open-source collaboration**.

---

## 📈 Output at Each Stage

* **fetch\_reviews.py** → Raw reviews grouped by date.
* **topic\_extraction.py** → Topics per review.
* **clustering.py** → Cluster mapping.
* **trend\_analysis.py** → Final trend DataFrame + CSV.

Each file transforms the data **one step forward**, so by the end we get a **clean time-series dataset of review trends**.

---

⚡ In short:
This repo takes **raw app reviews → summarizes into topics → clusters similar topics → builds daily trend tables → exports CSV.**

---