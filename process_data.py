
import pandas as pd
import re

def clean_empresa_pais_tipo(text):
    """
    This function cleans and parses the EMPRESA_PAIS_TIPO column.
    It extracts the company name, country, and type of relationship.
    """
    if not isinstance(text, str):
        return [], [], []

    # Split by ' + '
    entries = text.split(' + ')
    
    companies = []
    countries = []
    types = []

    for entry in entries:
        # Remove parentheses and strip whitespace
        entry = entry.strip().strip('()')
        
        # Extract type
        type_match = re.search(r'<([A-ZÃÇÕÁÉÍÚÂÊÔ, ]+)>([A-Z]+)', entry)
        if type_match:
            country = type_match.group(1).strip()
            type_ = type_match.group(2).strip()
            
            # Extract company name
            company_match = re.search(r'(.*?)<[A-ZÃÇÕÁÉÍÚÂÊÔ, ]+>[A-Z]+', entry)
            if company_match:
                company = company_match.group(1).strip()
            else:
                company = 'N/A'
        else:
            # Handle cases where the format is different
            parts = entry.split(' - ')
            if len(parts) > 1:
                company = ' - '.join(parts[:-1])
                location_type = parts[-1]
                
                # Extract country and type from location_type
                location_match = re.search(r'(.*)<([A-ZÃÇÕÁÉÍÚÂÊÔ, ]+)>(.*)', location_type)
                if location_match:
                    country = location_match.group(2).strip()
                    type_ = location_match.group(3).strip()
                else:
                    country = 'N/A'
                    type_ = 'N/A'
            else:
                company = entry
                country = 'N/A'
                type_ = 'N/A'

        companies.append(company)
        countries.append(country)
        types.append(type_)

    return companies, countries, types

def main():
    """
    Main function to process the Agrofit data.
    """
    # Load the dataset
    try:
        df = pd.read_csv('agrofitprodutosformulados.csv', sep=';', encoding='utf-8')
    except FileNotFoundError:
        print("Error: agrofitprodutosformulados.csv not found.")
        return

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Clean string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Process the 'empresa_pais_tipo' column
    df['empresas'], df['paises'], df['tipos'] = zip(*df['empresa_pais_tipo'].apply(clean_empresa_pais_tipo))

    # Save the cleaned data
    df.to_csv('agrofit_cleaned.csv', index=False)
    print("Data processed and saved to agrofit_cleaned.csv")

if __name__ == "__main__":
    main()
