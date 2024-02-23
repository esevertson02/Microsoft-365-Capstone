from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary of Microsoft 365 tools and their features
tools = {
    "Microsoft 365 Business Basic": ["Email", "Web versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint"],
    "Microsoft 365 Business Standard": ["Email", "Web versions of Office apps", "Desktop versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint"],
    "Microsoft 365 Business Premium": ["Email", "Web versions of Office apps", "Desktop versions of Office apps", "1TB OneDrive storage", "Teams", "SharePoint", "Advanced Threat Protection", "Intune device management", "Azure Information Protection"],
    # Add more licensing plans and their features as needed
}

@app.route('/')
def index():
    return render_template('index.html', tools=tools)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_features = request.form.getlist('features')
    recommended_plan = None

    for plan, features in tools.items():
        if all(feature in features for feature in selected_features):
            recommended_plan = plan
            break

    return render_template('recommendation.html', recommended_plan=recommended_plan)

if __name__ == '__main__':
    app.run(debug=True)
