# Reusable Data Cleaning Project

A no-code, step-by-step CSV data cleaning tool built with Streamlit and Pandas. Upload your CSV, clean it column by column, and download the result — no Python knowledge required.

---

## 🚀 Features

- **Upload & Inspect** — view shape, data types, missing values, duplicates, and statistical summary before touching anything
- **Rename Columns** — rename any column header or keep it as is
- **Fix Data Types** — cast columns to integer, string, datetime, or boolean
- **Handle Missing Values** — drop rows or fill with zero, mean, median, or mode per column
- **Clean Text** — strip whitespace, remove all spaces, or standardize casing (uppercase, lowercase, capitalize)
- **Download** — export your cleaned data as CSV or Excel (.xlsx)

---

## 📸 App Flow

| Step | Page |
|------|------|
| 1 | Upload CSV |
| 2 | Inspect Data |
| 3 | Rename Columns _(optional)_ |
| 4 | Fix Data Types |
| 5 | Handle Missing Values |
| 6 | Clean Text Data |
| 7 | Download Cleaned File |

### Upload CSV
<img width="1920" height="1080" alt="upload" src="https://github.com/user-attachments/assets/437aa76b-2d75-45d9-9b47-9cdf2191e4f0" />


### Inspect Data
<img width="1920" height="1080" alt="overview1" src="https://github.com/user-attachments/assets/1ebc75c5-c651-47f0-a588-ee0c915f7ea3" />
<img width="1920" height="1080" alt="overview2" src="https://github.com/user-attachments/assets/1132d006-3852-4ae8-be1b-3e79532f0bf2" />
<img width="1920" height="1080" alt="overview3" src="https://github.com/user-attachments/assets/c517e4ef-3eec-49f3-b7d9-44bbdb701413" />
<img width="1920" height="1080" alt="overview4" src="https://github.com/user-attachments/assets/7c68acd4-f5e5-4c7d-93eb-3353ca8cf565" />



### Rename Columns

<img width="1920" height="1080" alt="colum" src="https://github.com/user-attachments/assets/7c520c2f-af40-4b89-a7c3-338cb482cf70" />


### Fix Data Types

<img width="1920" height="1080" alt="datacleandatatype" src="https://github.com/user-attachments/assets/102aba2c-6445-4c1d-a7e4-2c25848710e5" />


### Handle Missing Values
<img width="1920" height="1080" alt="missing" src="https://github.com/user-attachments/assets/fbc53b4c-980e-4e43-bc68-655bf1a0aec4" />

### Download Cleaned File

<img width="1920" height="1080" alt="download" src="https://github.com/user-attachments/assets/19cbabb8-4e38-441c-b670-beb4c2d15a11" />


---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Pandas](https://pandas.pydata.org/) — data manipulation
- [NumPy](https://numpy.org/) — missing value replacement
- [OpenPyXL](https://openpyxl.readthedocs.io/) — Excel export

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/streamlit-data-cleaner.git
cd streamlit-data-cleaner

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```text
streamlit-data-cleaner/
├── app.py              # Main application — all pages and logic
└── README.md
```

---

## 🙌 Author

Built by **Biniyam** — feel free to fork, use, or contribute.
