from flask import Flask, flash, redirect, request, jsonify, render_template, send_from_directory, session, url_for
from werkzeug.utils import secure_filename
from cases import get_info
import cases_func as cf
from convert_patient_data import get_data
from sort_patients import get_crit_facilities
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
    case_outcomes,beds = get_crit_facilities(results)
    session['results'] = results if not isinstance(results, pd.DataFrame) else results.to_dict('records')
    session['counts'] = counts if not isinstance(counts, pd.DataFrame) else counts.to_dict('records')
    session['critical'] = critical if not isinstance(critical, pd.DataFrame) else critical.to_dict('records')
    session['case_outcomes'] = case_outcomes if not isinstance(case_outcomes, pd.DataFrame) else case_outcomes.to_dict('records')

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
    
    # Both 'counts' and 'critical' data are present; proceed to extract them
    counts = session['counts']
    critical = session['critical']

    # Render template with both counts and critical data
    return render_template('counts.html', counts=counts, critical=critical)

@app.route('/critical', methods=['GET'])
def display_critical():
    if 'case_outcomes' not in session or not session['case_outcomes']:
        flash("No data available. Please ensure file data is uploaded correctly.", "warning")
        return redirect(url_for('upload_file'))
    case_outcomes = session['case_outcomes']
    print(case_outcomes)
    return render_template('critical.html', case_outcomes= case_outcomes)

if __name__ == '__main__':
    app.run(debug=True)
