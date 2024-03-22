# Import necessary libraries
from flask import Flask, flash, jsonify, redirect, request, render_template, session, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from cases import get_info
import cases_func as cf
from convert_patient_data import get_data
from sort_patients import get_crit_facilities
import os
import pandas as pd
import load_balance as lb

app = Flask(__name__)
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
    return render_template('upload.html')

# Function to process uploaded file
def process_file(filepath):
    data_df = get_data(filepath)
    results = get_info(data_df)
    recs = get_crit_facilities(results)
    session['results'] = results if not isinstance(results, pd.DataFrame) else results.to_dict('records')
    session['recs'] = recs if not isinstance(recs, pd.DataFrame) else recs.to_dict('records')

# Route to display results
@app.route('/initial', methods=['GET'])
def display_initial_results():
    if 'results' not in session:
        flash('Please upload data first.', 'warning')
        return redirect(url_for('base'))
    results = session['results']
    matched_results = [result for result in results if result.get('Common Recommended Facilities')]
    unmatched_results = [result for result in results if not result.get('Common Recommended Facilities')]
    return render_template('results.html', matched_results=matched_results, unmatched_results=unmatched_results)


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


from flask import session, render_template
import pandas as pd

@app.route('/results', methods=['GET'])
def display_results():
    recs = session.get('recs', [])
    confirmed = session.get('confirm', [])
    

    for rec in recs:
        rec['is_confirmed'] = any(int(rec['Case ID']) == int(conf['case_id']) for conf in confirmed)
        for conf in confirmed:
            if int(rec['Case ID']) == int(conf['case_id']):
                rec['confirmed_facility'] = conf['facility']
                rec['mode'] = conf['mode']
                rec['time'] = conf['time']
                break

        # Initialize a list to hold facilities to be removed
        facilities_to_remove = []

        for facility in rec['Facilities']:
            for bed_type in rec['Bed Types Needed']:
                if not lb.check_beds(facility, bed_type):
                    # Mark the facility for removal and exit the loop for this facility
                    facilities_to_remove.append(facility)
                    print(f'Not available: {facility} {bed_type}')
                    break  # No need to check other bed types for this facility

    # Remove the marked facilities from rec['Facilities']
    rec['Facilities'] = [facility for facility in rec['Facilities'] if facility not in facilities_to_remove]

                

    return render_template('critical.html', recs=recs, confirmed=confirmed)


@app.route('/bed_counts')
def show_bed_counts():
    beds = session.get('bd',{})
    print(beds)
    return render_template('bed_counts.html', bed_counts=beds)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
