from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from forms import UploadForm, ModelForm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib 
import os
import subprocess
import uuid
import logging


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
    """Versionne un fichier avec DVC et le pousse sur Google Drive"""
    try:
        # Ajouter le fichier à DVC
        add_result = subprocess.run(
            ['dvc', 'add', file_path],
            check=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        logging.info(f"DVC add output: {add_result.stdout}")
        
        # Pousser les changements
        push_result = subprocess.run(
            ['dvc', 'push'],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        logging.info(f"DVC push output: {push_result.stdout}")
        
        # Commit les métadonnées DVC dans Git
        subprocess.run(
            ['git', 'add', f'{file_path}.dvc', '.gitignore'],
            check=True
        )
        subprocess.run(
            ['git', 'commit', '-m', f'DVC: Add {file_path} versioning'],
            check=True
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"DVC error (add/push): {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False

def dvc_pull(file_path):
    """Récupère un fichier versionné depuis Google Drive"""
    try:
        pull_result = subprocess.run(
            ['dvc', 'pull', file_path],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        logging.info(f"DVC pull output: {pull_result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"DVC pull error: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
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

            # Sauvegarder le fichier
            csv_filename = f"data/{uuid.uuid4()}.csv"
            df.to_csv(csv_filename, index=False)

            # Versionner avec DVC
            if not dvc_add_and_push(csv_filename):
                flash("Error versioning data with DVC.", 'error')
                return render_template('index.html', form=form)

            session['data_path'] = csv_filename
            flash('File uploaded and versioned successfully!', 'success')
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

    # Récupérer les données versionnées
    data_path = session['data_path']
    if not dvc_pull(data_path):
        flash("Error retrieving versioned data with DVC.", 'error')
        return redirect(url_for('index'))

    # Préparer les colonnes pour le formulaire
    columns = list(pd.read_csv(data_path).columns)
    form.target_column.choices = [(col, col) for col in columns]

    if form.validate_on_submit():
        target_column = form.target_column.data
        model_name = form.model.data

        # Entraîner le modèle (ceci définit model_path et score)
        model_path, score = train_model(data_path, target_column, model_name)

        # Vérifier si l'entraînement a réussi
        if model_path and score is not None:
            # Versionner le modèle avec DVC
            if not dvc_add_and_push(model_path):
                flash('Model could not be versioned.', 'error')
                return render_template('train.html', form=form, columns=columns)
            
            # Stocker les résultats en session
            session['model_path'] = model_path
            session['score'] = score
            return redirect(url_for('results'))
        else:
            flash('Model training failed.', 'error')

    return render_template('train.html', form=form, columns=columns)

@app.route('/results')
def results():
    if 'model_path' not in session:
        flash('Please train a model first.', 'error')
        return redirect(url_for('index'))

    model_path = session['model_path']
    score = session['score']

    return render_template('results.html', model_path=model_path, score=score)

@app.route('/download_model')
def download_model():
    if 'model_path' not in session:
        flash('Please train a model first.', 'error')
        return redirect(url_for('index'))

    model_path = session['model_path']
    return send_file(model_path, as_attachment=True)
    
if __name__ == '__main__':
    app.run(debug=True)