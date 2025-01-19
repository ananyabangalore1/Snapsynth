import pandas as pd
import PyPDF2
import pandas as pd

def process_excel(uploaded_excel):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_excel)
        
        # Ensure the necessary columns are present
        required_columns = ['account_holder_name', 'email', 'Password', 'location', 'favorite_color']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Excel file must contain the column: {col}")
        
        return df  

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return None  # Return None if there is any error during file processing

def process_pdf(uploaded_pdf):
    """
    Extract text from the uploaded PDF file.
    This function reads the PDF file and extracts all text from its pages.
    """
    try:
        # Open the PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
        
        # Extract text from all pages in the PDF
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
        
        return pdf_text
    except Exception as e:
        print(f"Error processing PDF file: {e}")
        return None
