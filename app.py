from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from forms import UploadForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'babanyangoma'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            csv_file = form.data_file.data
            df = pd.read_csv(csv_file)

            if df.empty:
              flash('Uploaded file is empty.', 'error')
              return render_template('index.html', form=form)

            # Generate a unique filename for the uploaded CSV
            csv_filename = f"data/{uuid.uuid4()}.csv"
            df.to_csv(csv_filename, index=False)

            if not dvc_add_and_push(csv_filename):
                flash("Error versioning data with DVC.", 'error')
                return render_template('index.html', form=form)

            session['data_path'] = csv_filename  # Store ONLY the path
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('train'))
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)