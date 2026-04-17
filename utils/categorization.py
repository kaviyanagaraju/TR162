import re

CATEGORY_RULES = {
    'Food': ['uber eats', 'mcdonalds', 'kfc', 'restaurant', 'grocery', 'walmart', 'food', 'coffee', 'starbucks', 'cafe'],
    'Rent': ['rent', 'lease', 'apartment', 'housing', 'mortgage'],
    'Travel': ['uber', 'lyft', 'gas', 'petrol', 'subway', 'transit', 'flight', 'ticket', 'shell', ' Chevron'],
    'Bills': ['electric', 'water', 'internet', 'phone', 'utility', 'at&t', 'verizon', 't-mobile', 'comcast', 'insurance'],
    'Entertainment': ['netflix', 'spotify', 'movie', 'cinema', 'game', 'steam', 'hulu'],
}

def categorize_expense(description):
    """
    Categorizes an expense based on keywords in the description.
    Returns 'Misc' if no clear category is found.
    """
    desc_lower = str(description).lower()
    
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            # Using basic substring/regex search
            if re.search(rf'\b{re.escape(keyword)}\b', desc_lower):
                return category
                
    return 'Fuel'

def apply_categorization(df):
    """Apply categorization to the entire dataframe"""
    if 'Category' not in df.columns:
        df['Category'] = 'Fuel'
        
    if 'Description' in df.columns:
        # Only override categories if they are 'Fuel', empty strings, or nulls
        mask = df['Category'].isin(['Fuel', '', None]) | df['Category'].isna()
        df.loc[mask, 'Category'] = df.loc[mask, 'Description'].apply(categorize_expense)
    return df
