# 📊 AutomatedSpreadsheets Dashboard

> A suite of Python projects that, by changing variables, allows you to export spreadsheets and charts almost automatically. Furthermore, there's a Streamlit dashboard that updates almost instantly!

🔗 **[Access the Live Dashboard](https://luiusu-dashboard-universidades.streamlit.app/?embed_options=dark_theme)**

## 📋 About

This project automates the processing of public procurement data from federal universities, generating consolidated spreadsheets, summaries, and charts almost automatically. The processed data is displayed on an interactive dashboard built with Streamlit.
The full pipeline goes from reading raw CSV files all the way to dynamic month/year visualization in the browser.

## ⚙️ Features

### 🤖 Automation (`automatedSpreadsheets/`)
- Reads public procurement CSV files (Windows-1252 encoding)
- Filters records from universities by agency name
- Calculates **Total Cost** (Quantity × Unit Price) per item
- Removes zero-cost entries and sorts from highest to lowest cost
- Exports two spreadsheets per month:
  - `universidades_{month}_{year}.xlsx` — detailed item data
  - `resumo_universidades_{month}_{year}.xlsx` — grouped by university
- Generates a bar chart of annual cost by month (in billions of BRL)
- Exports the chart as a `.png` image

### 📈 Dashboard (`Dashboard.py` + `pages/Resumo.py`)
- Dynamic **year** and **month** selection
- Table displaying costs for the selected month
- Interactive bar chart with **cumulative annual cost** (in billions of BRL)
- **Summary page** with a donut chart showing cost distribution per university (filtered to those exceeding R$ 11.6 million)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AutomatedSpreadsheets_Dashboard.git
cd AutomatedSpreadsheets_Dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the example file and fill in your paths:

```bash
cp .env.example .env
```

```env
PLANILHA_BASE2024_mar_ItemCompra.csv=C:\path\to\your\file.csv
CAMINHO=C:\path\to\export\folder
```

### 4. Run the processing script

Open `automatedSpreadsheets/main.py`, adjust the `ano` (year) and `mes` (month) variables at the top of the file, then run:

```bash
python automatedSpreadsheets/main.py
```

Spreadsheets and the chart will be automatically exported to the `{year}/{month}/` folder structure.

### 5. Launch the Dashboard

```bash
streamlit run Dashboard.py
```

## 📁 Expected Data Format

The input CSV must contain at least the following columns:

| Column | Description |
|---|---|
| `Nome Órgão` | Name of the purchasing agency |
| `Quantidade Item` | Quantity purchased |
| `Valor Item` | Unit price of the item |

> The columns `Código UG`, `Nome UG`, and `Descrição Complementar Item Compra` are automatically dropped during processing.


## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.


## 📄 License

This project is licensed under the **MIT License.** See the `LICENSE` file for details.
