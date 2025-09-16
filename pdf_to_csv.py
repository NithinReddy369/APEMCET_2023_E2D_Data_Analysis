import pdfplumber
import pandas as pd
import os

def extract_tables_from_pdf(pdf_path, csv_path):
    """
    Extract tables from PDF and save them to a CSV file.
    
    Args:
        pdf_path (str): Path to the input PDF file
        csv_path (str): Path where the CSV file will be saved
    """
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # List to store all tables
    all_tables = []
    
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_path) as pdf:
            # Iterate through all pages
            for page_number, page in enumerate(pdf.pages, 1):
                print(f"Processing page {page_number} of {len(pdf.pages)}")
                
                # Extract tables from the current page
                tables = page.extract_tables()
                
                # Process each table in the page
                for table_number, table in enumerate(tables, 1):
                    print(f"Found table {table_number} on page {page_number}")
                    
                    # Convert table to pandas DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])
                    
                    # Clean the DataFrame
                    # Remove any empty rows
                    df = df.dropna(how='all')
                    # Remove any empty columns
                    df = df.dropna(axis=1, how='all')
                    
                    all_tables.append(df)
    
        if not all_tables:
            print("No tables found in the PDF")
            return
        
        # Combine all tables
        final_df = pd.concat(all_tables, ignore_index=True)
        
        # Save to CSV
        final_df.to_csv(csv_path, index=False)
        print(f"Successfully saved data to {csv_path}")
        
        # Display first few rows of the extracted data
        print("\nFirst few rows of the extracted data:")
        print(final_df.head())
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Define input and output paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "APEAPCET_2022_Cutoff.pdf")
    csv_path = os.path.join(current_dir, "csv_file.csv")
    
    # Extract tables and save to CSV
    extract_tables_from_pdf(pdf_path, csv_path)