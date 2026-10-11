# 💰 MoneyMate — AI-Powered Personal Finance Management

MoneyMate is an AI-powered personal finance application that turns receipt images into structured expense data and helps users understand their spending habits. By combining multimodal AI, structured data extraction, financial analytics, and interactive visualizations, MoneyMate makes personal expense tracking easier and more insightful.



https://github.com/user-attachments/assets/ad8103ec-0f7c-4595-b1de-cb5229bb15c2



## ✨ Features

- **AI Receipt Scanning:** Upload receipt images and use an OpenAI-powered vision model to extract merchant names, purchase dates, item names, prices, and expense categories.
- **Structured Data Extraction:** Use LangChain and structured model output to convert unstructured receipt images into validated, structured receipt data.
- **Expense History:** Review previously scanned receipts and inspect individual purchases.
- **Spending Analytics:** Visualize spending by category, merchant, and date.
- **Flexible Date Filtering:** Analyze daily, weekly, monthly, yearly, or custom date ranges.
- **AI Financial Insights:** Generate concise observations about spending patterns and receive practical suggestions based on aggregated expense data.
- **Persistent Local Data:** Save receipt records to a JSON file so existing records can be loaded when the application starts again.

## 🧠 How It Works

1. **Upload a receipt** through the Streamlit interface.
2. **Extract information with AI:** Send the receipt image to an OpenAI vision-capable model through LangChain.
3. **Structure the result:** Convert the model output into a structured receipt containing merchant, date, and item-level expense information.
4. **Store the receipt:** Save the extracted data in a local JSON file.
5. **Analyze spending:** Aggregate expenses by category, merchant, and date, then visualize the results.
6. **Generate insights:** Send spending summaries to an OpenAI language model to produce observations and practical suggestions.

## 🏗️ Architecture

```text
Receipt Image
     |
     v
Streamlit User Interface
     |
     v
LangChain + OpenAI Vision Model
     |
     v
Structured Receipt Data
     |
     v
Receipt Handler
     |
     v
JSON Storage
     |
     v
Expense Aggregation and Analytics
     |
     +----------------------+
     |                      |
     v                      v
Interactive Visualizations  AI Financial Insights
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive multi-page web application |
| OpenAI API | Receipt image understanding and financial insights |
| LangChain | Model integration and structured output |
| Pydantic | Structured receipt data validation |
| Pandas | Tabular expense data and aggregation |
| Matplotlib and Seaborn | Spending visualizations |
| Altair | Interactive spending-over-time charts |
| JSON | Local receipt data persistence |
| Pytest | Testing support |

## 📊 Financial Analytics

MoneyMate provides several ways to explore personal spending:

- **Spending by category:** Compare expenses across food, household, transportation, entertainment, shopping, and other categories.
- **Spending by merchant:** Identify which companies account for the largest share of purchases.
- **Spending over time:** Explore how total spending changes across dates.
- **Quick statistics:** Review total spending, transaction count, and average transaction value.
- **AI-generated insights:** Get a concise summary of notable spending patterns and a practical suggestion.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or newer
- An OpenAI API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/18alba1/Personal-AI-Financial-management.git
cd Personal-AI-Financial-management
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

Install the project and its declared dependencies:

```bash
python -m pip install -e .
```

### 4. Configure Streamlit secrets

Copy the example secrets file to create your local configuration:

```bash
mkdir -p .streamlit
cp .streamlit/example_secrets.toml .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
openai_model = "gpt-4o"
openai_key = "YOUR_OPENAI_API_KEY"
working_dir = "/path/to/your/data-directory"
```

Replace the API key with your own key and set `working_dir` to a directory where the application can store receipt data.

**Security:** Never commit your real API key or private financial data to GitHub.

### 5. Run the application

```bash
streamlit run money_mate/home_page.py
```

Streamlit will provide a local URL where you can open MoneyMate in your browser.

## 📁 Project Structure

```text
Personal-AI-Financial-management/
├── .streamlit/
│   └── example_secrets.toml
├── money_mate/
│   ├── agents/
│   │   └── receipt_extraction_agent.py
│   ├── handler/
│   │   └── receipt_handler.py
│   ├── pages/
│   │   └── 2_analyze_page.py
│   └── home_page.py
├── pyproject.toml
└── README.md
```

The structure above highlights the main components; additional application files and pages are present in the repository.

## 🧩 Engineering Highlights

- **Multimodal AI integration:** Process receipt images with a vision-capable language model rather than relying solely on manual expense entry.
- **Structured LLM outputs:** Use a defined receipt schema to represent merchants, dates, and individual purchases consistently.
- **Separation of responsibilities:** Keep AI extraction, receipt persistence, and financial aggregation in separate components.
- **Data-driven insights:** Calculate spending summaries in Python before using an LLM to interpret the results.
- **Time-based analysis:** Support date filtering and aggregate spending across multiple dimensions.
- **Interactive analytics:** Combine Streamlit with charting libraries to make spending patterns easier to explore.

## 🔮 Potential Improvements

- Add automated tests for receipt extraction, data validation, and financial calculations.
- Introduce a database such as PostgreSQL for more robust storage and querying.
- Improve handling of duplicate receipts, currencies, taxes, and refunds.
- Add spending budgets, category limits, and alerts.
- Add deployment configuration and automated CI/CD checks.

## 📄 License

Check the repository for license information before reusing or distributing the project.
