import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Inventory Transfer Optimization System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data validation and transformation functions
def validate_and_transform_data(df):
    """Data validation and transformation"""
    # Article field forced to 12-digit text format
    if 'Article' in df.columns:
        df['Article'] = df['Article'].astype(str).str.zfill(12)
    
    # Numeric field processing
    numeric_columns = ['Inventory', 'Sales', 'Safety Stock', 'Pending Received']
    for col in numeric_columns:
        if col in df.columns:
            # Convert non-numeric to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill missing values
            df[col] = df[col].fillna(0)
            # Correct outliers (negative values to 0)
            df[col] = df[col].clip(lower=0)
    
    return df

# Transfer logic engine
class TransferOptimizer:
    def __init__(self, safety_stock_threshold=1.2):
        self.safety_stock_threshold = safety_stock_threshold
    
    def calculate_transfer_needs(self, df):
        """Calculate transfer needs"""
        results = []
        
        # Group by Article+OM
        grouped = df.groupby(['Article', 'OM'])
        
        for (article, om), group in grouped:
            total_stock = group['Inventory'].sum()
            total_sales = group['Sales'].sum()
            safety_stock = total_sales * self.safety_stock_threshold
            
            # Identify suppliers (sufficient inventory) and receivers (insufficient inventory)
            suppliers = []
            receivers = []
            
            for _, row in group.iterrows():
                available_stock = row['Inventory'] - (row['Sales'] * self.safety_stock_threshold)
                
                if available_stock > 0:
                    suppliers.append({
                        'location': row.get('Location', 'Unknown'),
                        'available_stock': available_stock,
                        'current_stock': row['Inventory']
                    })
                elif available_stock < 0:
                    receivers.append({
                        'location': row.get('Location', 'Unknown'),
                        'needed_stock': -available_stock,
                        'current_stock': row['Inventory']
                    })
            
            # Match transfers
            transfer_suggestions = self.match_transfers(suppliers, receivers, article, om)
            results.extend(transfer_suggestions)
        
        return pd.DataFrame(results)
    
    def match_transfers(self, suppliers, receivers, article, om):
        """Match suppliers and receivers"""
        suggestions = []
        
        for receiver in receivers:
            needed = receiver['needed_stock']
            remaining_need = needed
            
            for supplier in suppliers:
                if supplier['available_stock'] > 0 and remaining_need > 0:
                    transfer_amount = min(supplier['available_stock'], remaining_need)
                    
                    suggestion = {
                        'Article': article,
                        'OM': om,
                        'Transfer Location': supplier['location'],
                        'Receive Location': receiver['location'],
                        'Suggested Transfer Quantity': transfer_amount,
                        'Transfer Current Stock': supplier['current_stock'],
                        'Receive Current Stock': receiver['current_stock'],
                        'Receive Needed Qty': receiver['needed_stock'],
                        'Priority': 'Emergency' if receiver['needed_stock'] > receiver['current_stock'] else 'Potential'
                    }
                    
                    suggestions.append(suggestion)
                    remaining_need -= transfer_amount
                    supplier['available_stock'] -= transfer_amount
                    
                    if remaining_need <= 0:
                        break
        
        return suggestions

# Main Application
def main():
    st.title("📊 Inventory Transfer Optimization System")
    
    # Sidebar - Parameter Settings
    with st.sidebar:
        st.header("Parameter Settings")
        safety_threshold = st.slider(
            "Safety Stock Coefficient", 
            min_value=1.0, 
            max_value=2.0, 
            value=1.2, 
            step=0.1,
            help="Safety Stock = Sales × Coefficient"
        )
        
        uploaded_file = st.file_uploader(
            "Upload Excel File", 
            type=['xlsx'],
            help="Supports .xlsx format Excel files"
        )
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Data validation and transformation
            df = validate_and_transform_data(df)
            
            # Display data preview
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Initialize transfer optimizer
            optimizer = TransferOptimizer(safety_threshold)
            
            # Calculate transfer suggestions
            with st.spinner("Calculating transfer suggestions..."):
                transfer_results = optimizer.calculate_transfer_needs(df)
            
            if not transfer_results.empty:
                # Display transfer suggestions
                st.subheader("Transfer Suggestions")
                st.dataframe(transfer_results, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Transfer Suggestions", len(transfer_results))
                with col2:
                    st.metric("Urgent Transfers", 
                             len(transfer_results[transfer_results['Priority'] == 'Emergency']))
                with col3:
                    total_transfer = transfer_results['Suggested Transfer Quantity'].sum()
                    st.metric("Total Transfer Quantity", f"{total_transfer:,.0f}")
                
                # Visualization analysis
                st.subheader("Analysis Charts")
                
                tab1, tab2, tab3 = st.tabs(["Priority Distribution", "Transfer Quantity Distribution", "Location Analysis"])
                
                with tab1:
                    priority_counts = transfer_results['Priority'].value_counts()
                    fig1 = px.pie(
                        values=priority_counts.values,
                        names=priority_counts.index,
                        title="Transfer Priority Distribution"
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with tab2:
                    fig2 = px.histogram(
                        transfer_results, 
                        x='Suggested Transfer Quantity',
                        title="Transfer Quantity Distribution",
                        nbins=20
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                with tab3:
                    location_stats = transfer_results.groupby('Transfer Location')['Suggested Transfer Quantity'].sum().reset_index()
                    fig3 = px.bar(
                        location_stats,
                        x='Transfer Location',
                        y='Suggested Transfer Quantity',
                        title="Transfer Out Quantity by Location"
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Export function
                st.subheader("Export Results")
                csv = transfer_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Transfer Suggestions CSV",
                    data=csv,
                    file_name=f"transfer_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            else:
                st.info("No transfer suggestions needed for current data")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        st.info("Please upload an Excel file to start analysis")
        
        # Display example file format requirements
        with st.expander("File Format Requirements"):
            st.markdown("""
            ### Required Columns:
            - **Article**: Product number (numeric or text)
            - **OM**: Organizational unit number
            - **Inventory**: Current inventory quantity
            - **Sales**: Recent sales data
            
            ### Optional Columns:
            - **Location**: Inventory location identifier
            - **Safety Stock**: Safety stock threshold
            - **Pending Received**: In-transit inventory quantity
            
            ### Example Data Structure:
            | Article | OM | Inventory | Sales | Location |
            |---------|-----|-----------|-------|----------|
            | 123456789012 | 1001 | 150 | 50 | Warehouse A |
            | 123456789012 | 1002 | 80 | 60 | Warehouse B |
            """)

if __name__ == "__main__":
    main()