# app.py
import csv
from flask import Flask, jsonify, render_template_string # Added jsonify and render_template_string

# --- Configuration ---
CSV_FILE_PATH = 'data.csv'

# --- Helper Function to Load Data ---
def load_csv_data(filepath):
    """Reads data from a CSV file into a list of dictionaries."""
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            # DictReader uses the first row as headers/keys for the dicts
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        print(f"Successfully loaded {len(data)} rows from {filepath}")
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred while reading {filepath}: {e}")
    return data

# --- Load Data on Application Start ---
# Reads the CSV once when the app starts, making it efficient for requests.
# Assumes the CSV doesn't change while the app is running.
# If the CSV changes frequently, you might need to reload it periodically or on request.
csv_data = load_csv_data(CSV_FILE_PATH)

# --- Create Flask App Instance ---
app = Flask(__name__)

# --- Routes ---
@app.route('/')
def hello_world():
    """Homepage route."""
    return 'Hello from Flask! Go to /data for CSV content or /api/data for JSON.'

@app.route('/data')
def show_data_table():
    """Displays the CSV data in a simple HTML table."""
    if not csv_data:
        return "Error: No data loaded from CSV or file not found.", 404

    # Basic HTML table generation (for more complex HTML, use Jinja2 templates)
    # Get headers from the keys of the first dictionary (assumes all rows have same keys)
    headers = csv_data[0].keys()
    html = "<h1>CSV Data</h1>"
    html += "<table border='1'>"

    # Table Header Row
    html += "<thead><tr>"
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr></thead>"

    # Table Body Rows
    html += "<tbody>"
    for row_dict in csv_data:
        html += "<tr>"
        for header in headers: # Iterate in header order for consistency
            html += f"<td>{row_dict.get(header, '')}</td>" # Use .get for safety
        html += "</tr>"
    html += "</tbody>"

    html += "</table>"
    # Using render_template_string is slightly safer than just returning raw HTML
    # but for production apps, use proper Jinja2 template files.
    return render_template_string(html)

@app.route('/api/data')
def get_data_json():
    """Serves the CSV data as JSON."""
    if not csv_data:
         # Return an empty list or an error message in JSON format
        return jsonify({"error": "No data loaded from CSV or file not found."}), 404
    return jsonify(csv_data) # Flask's jsonify converts the list of dicts to JSON

# --- Run Development Server ---
if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible from other devices on the network
    # debug=True enables auto-reloading and detailed error pages (NEVER use in production)
    app.run(debug=True, host='0.0.0.0', port=5000)