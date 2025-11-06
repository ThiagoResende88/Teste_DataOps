
import pandas as pd

def analyze_data():
    """
    Analyzes the cleaned Agrofit data and provides insights.
    """
    try:
        df = pd.read_csv('agrofit_cleaned.csv')
    except FileNotFoundError:
        print("Error: agrofit_cleaned.csv not found. Please run process_data.py first.")
        return

    print("--- Data Analysis and Insights ---")

    # Number of products per company
    company_counts = df['titular_de_registro'].value_counts().head(10)
    print("\nTop 10 Companies by Number of Products:")
    print(company_counts)

    # Number of products per class
    class_counts = df['classe'].value_counts()
    print("\nNumber of Products by Class:")
    print(class_counts)

    # Number of products per environmental class
    environmental_class_counts = df['classe_ambiental'].value_counts()
    print("\nNumber of Products by Environmental Class:")
    print(environmental_class_counts)

    # Number of organic products
    organic_counts = df['organicos'].value_counts()
    print("\nNumber of Organic vs. Non-Organic Products:")
    print(organic_counts)
    
    # --- Proposed Visualizations ---
    print("\n--- Proposed Visualizations for Power BI Dashboard ---")
    print("1. Bar Chart: Top 10 Companies by Number of Registered Products.")
    print("2. Pie Chart: Distribution of Products by Toxicological Class.")
    print("3. Donut Chart: Distribution of Products by Environmental Class.")
    print("4. Map: Geographical Distribution of Companies (requires extracting location from 'titular_de_registro').")
    print("5. Treemap: Hierarchical view of Product Classes and their respective Formulations.")
    print("6. Word Cloud: Most Common Active Ingredients ('ingrediente_ativo').")

if __name__ == "__main__":
    analyze_data()
