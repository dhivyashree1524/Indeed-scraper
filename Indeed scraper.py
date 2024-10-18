from apify_client import ApifyClient
import pandas as pd
import json
import os

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_vkgJp6cArO4xkka9dMfCMjy0xuH8Zq1kQusF")

# Prepare the Actor input
run_input = {
    "position": "web developer",
    "country": "US",
    "location": "San Francisco",
    "maxItems": 50,
    "parseCompanyDetails": False,
    "saveOnlyUniqueItems": True,
    "followApplyRedirects": False,
}

# Run the Actor and wait for it to finish
run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)

# Fetch and collect Actor results from the run's dataset
data = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    data.append(item)

# Ensure we have data
if data:
    # 1. Save data as JSON
    json_filename = "scraped_data.json"
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file created: {json_filename}")

    # 2. Convert the data to a Pandas DataFrame for CSV/Excel
    df = pd.DataFrame(data)

    # 3. Save data as CSV
    csv_filename = "scraped_data.csv"
    df.to_csv(csv_filename, index=False)
    print(f"CSV file created: {csv_filename}")

    # 4. Save data as Excel
    excel_filename = "scraped_data.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Excel file created: {excel_filename}")

    # Automatically open the files (Windows-specific)
    try:
        os.startfile(json_filename)  # Open JSON file
        os.startfile(csv_filename)   # Open CSV file
        os.startfile(excel_filename) # Open Excel file
    except Exception as e:
        print(f"Error opening files: {e}")
else:
    print("No data was scraped, so no files were created.")
