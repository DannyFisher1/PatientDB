
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
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def base():
    
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    
        # Process the file using get_data function
        data_df = get_data(filepath)
        # Process the DataFrame to get the desired information using get_info
        results = get_info(data_df)
        if isinstance(results, pd.DataFrame):
            session['results'] = results.to_dict('records')
        else:
            session['results'] = results 
        counts = cf.facility_amounts(results)
        critical = cf.is_critical(results)
        case_outcomes, updated_bed_counts = get_crit_facilities(results)
        if isinstance(counts, pd.DataFrame):
            session['counts'] = counts.to_dict('records')
        else:
            session['counts'] = counts 
        if isinstance(case_outcomes, pd.DataFrame):
            session['case_outcomes'] = case_outcomes.to_dict('records')
        else:
            session['case_outcomes'] = case_outcomes 

        if isinstance(critical, pd.DataFrame):
            session['critical'] = critical.to_dict('records') 
        else:
            session['critical'] = critical
        

        for result in results:
            if 'Bed Typed Needed' in result:
                result['Bed Typed Needed'] = ', '.join(result['Bed Typed Needed'])
            if 'Specialties Needed' in result:
                result['Specialties Needed'] = ', '.join(result['Specialties Needed'])
            if 'Common Recommended Facilities' in result:
                result['Common Recommended Facilities'] = ', '.join(result['Common Recommended Facilities'])
        return render_template('results.html', results=results, counts= counts, critical = critical)

    else:
        return jsonify({'error': 'File not allowed'}), 400
    
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
@app.route('/crit')
def crit():
    if 'case_outcomes' not in session or not session['case_outcomes']:
        flash("No data available. Please ensure file data is uploaded correctly.", "warning")
        return redirect(url_for('upload_file'))
    case_outcomes = session['case_outcomes']
    print(case_outcomes)
    return render_template('critical.html', case_outcomes= case_outcomes)
#    case_outcomes, updated_bed_counts = get_crit_facilities(results)

if __name__ == '__main__':
    app.run(debug=True)
