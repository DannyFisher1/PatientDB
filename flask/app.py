# Import necessary libraries
from flask import Flask, flash, jsonify, redirect, request, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_session import Session
from werkzeug.utils import secure_filename
import functions.cases_func as cf
from functions.convert_patient_data import get_data
from functions.sort_patients import match_patients, set_traffic_speed, update_facility_lists
import os
import pandas as pd
import functions.load_balance as lb

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'verysecretkeychangethis'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'flask_session_files'
app.config['SESSION_PERMANENT'] = False
# app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'json'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# Initialize Flask-Session
Session(app)
# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Set session to non-permanent before each request
@app.before_request
def make_session_not_permanent():
    session.permanent = False

# Route for home page
@app.route('/', methods=['GET'])
def base():
    session.clear()
    return render_template('landing.html')

# Route for uploading files
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
   
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('base'))
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_file(filepath)
            return redirect(url_for('display_results'))
        
    confirmed = session.get('confirm', [])
    
    return render_template('upload.html')

# Function to process uploaded file
def process_file(filepath):
    data_df = get_data(filepath)
    results = cf.get_info(data_df)
    traffic_speed = set_traffic_speed()
    session['results'] = results if not isinstance(results, pd.DataFrame) else results.to_dict('records')
    session['traffic_speed'] = traffic_speed if not isinstance(traffic_speed, pd.DataFrame) else traffic_speed.to_dict('records')


# Route to process confirmed selections
@app.route('/process_value', methods=['POST'])
def process_value():
    data = request.get_json()
    confirmed_placement = {
        'facility': data['facility'],
        'bedType': data['bedType'],
        'mode': data['mode'],
        'time': data['time'],
        'case_id': data['caseId']
    }
    if 'confirm' not in session:
        session['confirm'] = []
    if all(confirmed_placement['case_id'] != conf['case_id'] for conf in session['confirm']):
        session['confirm'].append(confirmed_placement)
        session.modified = True
    if 'bd' not in session:
        session['bd'] = lb.data
    lb.update_beds(confirmed_placement)
    return jsonify({"message": "Confirmation data stored successfully."})

# Move case to end of severity
@app.route('/skip_case')
def skip_case():
    skip_case_id = int(request.args.get('skip_case_id'))
    if 'results' not in session or skip_case_id is None:
        return jsonify({"success": False, "message": "No case ID provided or no results in session."})

    results = session['results']
    skipped_case = None
    for case in results:
        if case['Case ID'] == skip_case_id: 
            skipped_case = case

    if skipped_case is None:
        return jsonify({"success": False, "message": f"No case found with ID {skip_case_id}."})

    skipped_case_severity = skipped_case['Severity'].upper()

    # Reorganize cases based on severity and skip case
    organized_cases = { 'CRITICAL': [], 'SERIOUS': [], 'MODERATE': [], 'MILD': [] }
    for case in results:
        organized_cases[case['Severity'].upper()].append(case)
    
    # Remove the skipped case from its current list and append it to the end
    organized_cases[skipped_case_severity].remove(skipped_case)
    organized_cases[skipped_case_severity].append(skipped_case)

    # Flatten the dictionary back into the session's results
    session['results'] = [case for cases in organized_cases.values() for case in cases]
    session.modified = True

    return jsonify({"success": True, "message": f"Case ID {skip_case_id} moved to the end of the {skipped_case_severity} list."})

@app.route('/results', methods=['GET'])
def display_results():
    skip_case_id = request.args.get('skip_case_id', None)
    results = session.get('results', [])
    traffic_speed = session.get('traffic_speed', [])
    recs = match_patients(results, traffic_speed)

    # Initialize lists to hold cases based on severity
    critical_cases = []
    serious_cases = []
    moderate_cases = []
    mild_cases = []  # New list for mild cases

    # Iterate through the cases to categorize them and identify the skipped case
    skipped_case = None
    for case in recs:
        if skip_case_id and case['Case ID'] == skip_case_id:
            skipped_case = case
            continue

        if case['Severity'].upper() == 'CRITICAL':
            critical_cases.append(case)
        elif case['Severity'].upper() == 'SERIOUS':
            serious_cases.append(case)
        elif case['Severity'].upper() == 'MODERATE':
            moderate_cases.append(case)
        elif case['Severity'].upper() == 'MILD':  # Handling for mild cases
            mild_cases.append(case)

    # Append the skipped case to the end of its severity category
    if skipped_case:
        severity = skipped_case['Severity'].upper()
        if severity == 'CRITICAL':
            critical_cases.append(skipped_case)
        elif severity == 'SERIOUS':
            serious_cases.append(skipped_case)
        elif severity == 'MODERATE':
            moderate_cases.append(skipped_case)
        elif severity == 'MILD':
            mild_cases.append(skipped_case)

    # Reassemble the cases list
    recs = critical_cases + serious_cases + moderate_cases + mild_cases

    confirmed = session.get('confirm', [])
    display_instructions = True
    if confirmed:
        print(len(confirmed))
        display_instructions = False
        print(display_instructions)


    recs, unmatched_results = update_facility_lists(recs, confirmed)



    return render_template('main.html', recs=recs, confirmed=confirmed, unmatched_results=unmatched_results, display_instructions=display_instructions)



@app.route('/bed_counts')
def show_bed_counts():
    beds = session.get('bd',{})
    # print(beds)
    return render_template('bed_counts.html', bed_counts=beds)




# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
