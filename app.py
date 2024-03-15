import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the NCE Pricelist data
nce_pricelist = pd.read_csv('NCE_Pricelist.csv')

# Dictionary of Microsoft 365 tools and their features
tools = {
    "Microsoft 365 Business Basic": ["Email", "Web versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint", "Yammer"],
    "Microsoft 365 Business Standard": ["Email", "Web versions of Office apps", "Desktop versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint", "Yammer"],
    "Microsoft 365 Business Premium": ["Email", "Web versions of Office apps", "Desktop versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint", "Yammer", "Advanced Threat Protection", "Intune device management", "Azure Information Protection"],
}

@app.route('/')
def index():
    return render_template('index.html', tools=tools)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_features = request.form.getlist('features')
    recommended_plan = None

    # Load the offer matrix file
    offer_matrix = pd.read_csv('Offer_Matrix.csv')

    # Assuming the column names for Product ID and Provisioning ID in offer_matrix
    product_id_column = 'ProductId'
    provisioning_id_column = 'ProvisioningId'

    # Assuming the column name for Product ID in NCE Pricelist
    pricelist_product_id_column = 'ProductId'

    # Map selected features to product IDs
    product_ids = map_features_to_product_ids(selected_features, offer_matrix)

    # Filter the pricelist based on the mapped product IDs
    filtered_pricelist = nce_pricelist[nce_pricelist[pricelist_product_id_column].isin(product_ids)]

    # Recommend the best licensing plan based on the filtered pricelist
    recommended_plan = recommend_licensing_plan(filtered_pricelist)

    return render_template('recommendation.html', recommended_plan=recommended_plan)

def map_features_to_product_ids(selected_features, offer_matrix):
    product_ids = []
    for feature in selected_features:
        # Filter the DataFrame based on the feature
        filtered_rows = offer_matrix[offer_matrix['ProductId'] == feature]
        
        # Check if the filtered DataFrame is empty
        if not filtered_rows.empty:
            # If not empty, get the first 'ProductId' value
            product_id = filtered_rows['ProductId'].values[0]
            product_ids.append(product_id)
        else:
            # Handle the case where no matching product ID is found
            # This could involve logging a message, skipping the feature, or taking other actions
            print(f"No product ID found for feature: {feature}")
    
    return product_ids

def recommend_licensing_plan(filtered_pricelist):
    if filtered_pricelist.empty:
        return "No matching plan found."
    
    # Assuming there's a 'Price' column in the pricelist
    lowest_price_plan = filtered_pricelist.loc[filtered_pricelist['Price'].idxmin()]
    recommended_plan = lowest_price_plan['ProductId']
    return recommended_plan

if __name__ == '__main__':
    app.run(debug=True)