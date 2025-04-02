from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from forms import UploadForm, ModelForm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib  # For saving and loading models
import os
import subprocess
import uuid # For generating unique filenames


app = Flask(__name__)
app.config['SECRET_KEY'] = 'babanyangoma'


def train_model(data_path, target_column, model_name):
    """
    Trains a machine learning model.

    Args:
        data_path (str): Path to the CSV training data.
        target_column (str): Name of the target column.
        model_name (str): Name of the model to train.

    Returns:
        tuple: (model_path, score) or (None, None)
    """
    data = pd.read_csv(data_path) 
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = None
    score = None

    if model_name == 'linear_regression':
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = mean_squared_error(y_test, y_pred)
    elif model_name == 'svm_classification':
        model = SVC()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)
    elif model_name == 'random_forest_classification':
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)

    if model:
        model_filename = f"models/{uuid.uuid4()}.joblib"
        joblib.dump(model, model_filename)
        return model_filename, score
    else:
        return None, None
    
    

def dvc_add_and_push(file_path):
    """Adds a file to DVC and pushes it to remote storage."""
    try:
        subprocess.run(['dvc', 'add', file_path], check=False, capture_output=True,text=True,timeout=60)
        subprocess.run(['dvc', 'push'], check=False,capture_output=True,text=True,timeout=120)
        return True
    except subprocess.CalledProcessError as e:
        print(f"DVC error: {e}")
        return False

def dvc_pull(file_path):
    """Pulls a file from DVC remote storage."""
    try:
        subprocess.run(['dvc', 'pull', file_path], check=False,capture_output=True,text=True,timeout=120)
        return True
    except subprocess.CalledProcessError as e:
        print(f"DVC error: {e}")
        return False

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

            csv_filename = f"data/{uuid.uuid4()}.csv"
            df.to_csv(csv_filename, index=False)

            if not dvc_add_and_push(csv_filename):
                flash("Error versioning data with DVC.", 'error')
                return render_template('index.html', form=form)

            session['data_path'] = csv_filename 
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('train'))
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
    return render_template('index.html', form=form)


@app.route('/train', methods=['GET', 'POST'])
def train():
    form = ModelForm()
    if 'data_path' not in session:
        flash('Please upload data first.', 'error')
        return redirect(url_for('index'))

    data_path = session['data_path']

    if not dvc_pull(data_path):
        flash("Error retrieving data with DVC.", 'error')
        return redirect(url_for('index'))

    columns = list(pd.read_csv(data_path).columns) 
    form.target_column.choices = [(col, col) for col in columns]

    if form.validate_on_submit():
        target_column = form.target_column.data
        model_name = form.model.data

        model_path, score = train_model(data_path, target_column, model_name) 

        if model_path:
            if not dvc_add_and_push(model_path):
                flash('Model could not be saved and versioned.', 'error')
                return render_template('train.html', form=form, columns=columns)

            session['model_path'] = model_path 
            session['score'] = score
            return redirect(url_for('results'))
        else:
            flash('Model training failed.', 'error')

    return render_template('train.html', form=form, columns=columns)



if __name__ == '__main__':
    app.run(debug=True)