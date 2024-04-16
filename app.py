import pandas as pd
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load the NCE Pricelist data
nce_pricelist = pd.read_csv('NCE_Pricelist.csv')

# Dictionary of Microsoft 365 tools and their features
tools = {
    "Microsoft 365 Features": ["Desktop versions of Microsoft Word, Excel, PowerPoint, Outlook, and OneDrive","Identity, Access and User Management","Host and Administer 50GB Mailboxes", "Custom Business Emails","Web and Mobile version of Outlook", "Microsoft Teams (Collaboration and Communication Platform)", "Microsoft SharePoint (Web-based Collaboration Platform)","Microsoft Stream (Video Sharing)","Microsoft Bookings (Appointment Scheduling Service)","Microsoft Planner (Project Management Tool)", "Microsoft Forms (Online Surveys and Quizzes)", "Microsoft Lists (Task and Information Management)","Desktop Version of Microsoft Teams", "Microsoft Access (Database Management System)", "Microsoft Publisher (Desktop Publishing Software)", "Microsoft Loop (Webinar Hosting and Functionality)","Microsoft Clipchamp (Video Editing)", "Advanced Threat Protection (Necessary for Compliance in Some Cases)", "Microsoft EntraID (Protect Employee Identities)","Microsoft Intune (Cloud-based Mobile Device and Application Management)", "Azure Information Protection (Data Security and Encryption Service)"],
}

featurelist = [
 ['Advanced Threat Protection (ATP)', 'Data Loss Prevention (DLP)', 'Mobile Device Management (MDM)', 'Multi-Factor Authentication (MFA)'],
 ['Microsoft Teams', 'Exchange Online', 'SharePoint Online'],
 ['Office Applications', 'OneDrive for Business', 'Outlook Customer Manager'],
 ['Information Protection', 'eDiscovery', 'Audit Logs'],
 ['Admin Console', 'Intune', 'Windows Autopilot'],
 ['Exchange Online Protection', 'Skype for Business', 'Yammer'],
 ['MyAnalytics', 'Power BI Pro']
]

microFeatures = [[['x','f','z'],['d'],['a','python'],['d']],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[]]]


groupList = ["Security","Collaboration","Productivity","Compliance and Legal","Administration and IT","Communication","Analytics"
]

@app.route('/index')
def index():
    return render_template('index.html', tools=tools)

@app.route('/finalRecommend')
def finalRecommend():
    return render_template('finalRecommend.html')

@app.route('/features')
def features():
    groups = groupList
    return render_template('features.html', groups = groups,features=featurelist, size = len(groups), microFeatures = microFeatures)

@app.route('/')
def welcome():
    return render_template('welcome.html')

'''@app.route('/proofofconcept', methods = ['POST'])
def proofofconcept():
    plan = 'Microsoft 365 Apps for Business ' #So this is the default state, added space so I can differentiate between when it is changed ot it rather than default
    selected_features = request.form.getlist('features[]')
    sizeOfCompany = request.form['size']
    features_selected = [False] * len(featurelist)
    for feature in selected_features:
        index = featurelist.index(feature)
        features_selected[index] = True
    if sizeOfCompany == "Yes":
        plan = 'Some Enterprise Level Plan'
    else:
        if features_selected[0]:
            plan = 'Microsoft 365 Apps for Business'
        if True in features_selected[1:13]:
            if plan == 'Microsoft 365 Apps for Business':
                plan = 'Microsoft 365 Business Standard'
            else:
                plan = 'Microsoft 365 Business Basic'
        if True in features_selected[13:17]:
            plan = 'Microsoft 365 Business Standard'
        if True in features_selected[17:21]:
            plan = 'Microsoft 365 Business Premium'
    
    plan = plan.rstrip()
    return render_template('concept.html', plan = plan)
'''
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
