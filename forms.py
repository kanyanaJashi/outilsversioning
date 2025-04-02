from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField

class UploadForm(FlaskForm):
    data_file = FileField('Upload CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])

class ModelForm(FlaskForm):
    model = SelectField('Select Model', choices=[
        ('linear_regression', 'Linear Regression'),
        ('svm_classification', 'SVM Classification'),
        ('random_forest_classification', 'Random Forest Classification')
    ])
    target_column = SelectField('Select Target Column')