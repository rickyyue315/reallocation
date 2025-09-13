# Smart Transfer Optimization System

A Python-based intelligent transfer optimization system designed for retail inventory management. The system automatically analyzes Excel inventory data and generates optimal cross-store transfer suggestions.

## 🚀 Key Features

### 1. Data Preprocessing & Validation
- ✅ Article field 12-digit text formatting
- ✅ Automatic numeric field correction and outlier handling
- ✅ Intelligent missing value filling
- ✅ Sales data range validation (0-100,000)

### 2. Core Business Logic
- 🔄 **ND Type Transfer**: Priority processing for ND type inventory transfers
- 🔄 **RF Type Transfer**: Smart identification of RF type excess inventory
- 🚨 **Emergency Stockout Receiving**: Priority replenishment for zero-stock stores with sales records
- 📈 **Potential Stockout Receiving**: Inventory optimization for high-sales stores

### 3. Intelligent Matching Algorithm
- 🤖 Article+OM combination grouping
- ⚡ Priority-driven matching logic
- 📊 Optimal transfer quantity calculation
- 🔄 Real-time status updates

### 4. Quality Assurance System
- ✅ 5 automated quality checks
- 📋 Complete processing logs
- 🎯 Data accuracy validation

### 5. Multi-format Output
- 📊 Excel format output (transfer suggestions + statistical summary)
- 📝 CSV format export
- 📈 Visual statistical reports

## 🛠️ Technology Stack

- **Python 3.8+**
- **Pandas** - Data processing and analysis
- **Streamlit** - Web user interface
- **Openpyxl** - Excel file handling
- **Logging** - System logging

## 📦 Installation & Running

### Method 1: Using batch file (Recommended)
1. Double-click `run_app.bat`
2. System automatically installs dependencies and starts web interface

### Method 2: Manual installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start web interface
streamlit run web_interface.py

# Or process Excel file directly
python transfer_system.py
```

## 📁 File Structure

```
Smart Transfer System/
├── transfer_system.py    # Core transfer logic
├── web_interface.py     # Web user interface
├── run_app.bat         # Windows startup script
├── requirements.txt    # Python dependencies
├── README.md          # English documentation
├── README_CN.md       # Chinese documentation
└── sample_data.py     # Sample data generation
```

## 📊 Input File Requirements

### Required Fields
| Field Name | Description | Format |
|------------|-------------|--------|
| Article | Product code | Text |
| RP Type | Type identifier | ND/RF |
| Site | Store location | Text |
| OM | Organizational unit | Text |
| SaSa Net Stock | Current inventory | Integer |
| Safety Stock | Safety stock | Integer |

### Optional Fields
| Field Name | Description |
|------------|-------------|
| Last Month Sold Qty | Last month sales quantity |
| MTD Sold Qty | Month-to-date sales quantity |
| Pending Received | In-transit inventory |

## 🎯 Output Results

### Transfer Suggestions Table
- Article (12-digit text)
- OM (Organizational unit)
- Transfer Site (Transfer-out store)
- Receive Site (Receive store)
- Transfer Qty (Transfer quantity)
- Transfer Type (Transfer type)
- Receive Priority (Receive priority)

### Statistical Summary
- 📈 KPI key metrics
- 📊 Statistics by Article
- 📊 Statistics by OM
- 📊 Transfer type analysis
- 📊 Receive priority analysis

## 🔧 Custom Configuration

System supports the following parameter adjustments:
- Safety stock coefficient adjustment
- Sales outlier threshold settings
- Output file format selection
- Processing log level configuration

## 📞 Technical Support

If encountering issues, please check:
1. Python version is 3.8+
2. All dependencies installed successfully
3. Input file format meets requirements
4. Error messages in system logs

## 📄 License

This project is open source under MIT license, free to use and modify.