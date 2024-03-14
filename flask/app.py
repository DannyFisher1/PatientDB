from flask import Flask, flash, redirect, request, render_template, session, url_for
from werkzeug.utils import secure_filename
from cases import get_info
import cases_func as cf
from convert_patient_data import get_data
from sort_patients import get_crit_facilities
import load_balance as lb
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'json'}
app.secret_key = 'changethis'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.before_request
def make_session_not_permanent():
    session.permanent = False


@app.route('/', methods=['GET'])
def base():
    return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    session.clear()
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('base'))
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_file(filepath)  # Processes and stores data in session
            return redirect(url_for('display_results'))
    return render_template('upload.html')


def process_file(filepath):
    data_df = get_data(filepath)
    results = get_info(data_df)
    counts = cf.facility_amounts(results)
    critical = cf.is_critical(results)
    case_outcomes, beds, recs = get_crit_facilities(results)
    session['results'] = results if not isinstance(results, pd.DataFrame) else results.to_dict('records')
    session['counts'] = counts if not isinstance(counts, pd.DataFrame) else counts.to_dict('records')
    session['critical'] = critical if not isinstance(critical, pd.DataFrame) else critical.to_dict('records')
    session['case_outcomes'] = case_outcomes if not isinstance(case_outcomes, pd.DataFrame) else case_outcomes.to_dict('records')
    session['beds'] = beds if not isinstance(beds, pd.DataFrame) else beds.to_dict('records')
    session['recs'] = recs if not isinstance(recs, pd.DataFrame) else recs.to_dict('records')


@app.route('/results', methods=['GET'])
def display_results():
    if 'results' not in session:
        flash('Please upload data first.', 'warning')
        return redirect(url_for('base'))

    results = session['results']
    matched_results = [result for result in results if result.get('Common Recommended Facilities')]


    unmatched_results = [result for result in results if not result.get('Common Recommended Facilities')]

    return render_template('results.html', matched_results=matched_results, unmatched_results=unmatched_results)


@app.route('/stats', methods=['GET'])
def display_counts():
    if 'counts' not in session or 'critical' not in session or not session['counts'] or not session['critical']:
        flash("No data available. Please ensure file data is uploaded correctly.", "warning")
        return redirect(url_for('upload_file'))

    counts = session['counts']
    critical = session['critical']

    return render_template('counts.html', counts=counts, critical=critical)


@app.route('/critical', methods=['GET'])
def display_critical():
    # Check if necessary data is in session
    if 'case_outcomes' not in session or 'beds' not in session or 'recs' not in session or not session['case_outcomes'] or not session['beds'] or not session['recs']:
        flash("No data available. Please ensure file data is uploaded correctly.", "warning")
        return redirect(url_for('upload_file'))

    # Extract data from session
    case_outcomes = session['case_outcomes']
    beds = session['beds']
    recs = session['recs']

    # This part seems to be preparation for another part of your app,
    # converting initial bed data structure for use in the template
    initial_bed_data_raw = lb.data
    initial_bed_data = {}
    bed_types = initial_bed_data_raw['Bed Type']

    for facility, counts in initial_bed_data_raw.items():
        if facility != 'Bed Type':  # Assuming 'Bed Type' is a key that doesn't represent a facility
            initial_bed_data[facility] = {bed_types[i]: count for i, count in enumerate(counts)}

    # Sorting cases by travel time for display; assumes 'Travel Time' is ground travel time
    sorted_cases = sorted(case_outcomes, key=lambda x: int(x['Travel Time']) if x['Assigned'] else float('inf'))

    # No need for facility mapping since we are using actual facility names
    # Pass sorted cases, initial bed data, beds, and recommendations (recs) to the template
    return render_template('critical.html', sorted_cases=sorted_cases, initial_bed_data=initial_bed_data, beds=beds, recs=recs)

if __name__ == "__main__":
    app.run(debug=True)