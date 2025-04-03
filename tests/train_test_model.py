import os
import json
from app import train_model

def test_model_training():
    # Utiliser un petit dataset de test
    test_data = "tests/test_data.csv"
    report = {}
    
    try:
        # Tester chaque type de modèle
        for model_type in ['linear_regression', 'svm_classification', 'random_forest_classification']:
            model_path, score = train_model(test_data, 'target', model_type)
            
            assert model_path is not None
            assert isinstance(score, float)
            
            report[model_type] = {
                'status': 'success',
                'score': score,
                'model_path': model_path
            }
            
            # Vérifier que le modèle existe
            assert os.path.exists(model_path)
    except Exception as e:
        report['error'] = str(e)
        raise
    finally:
        with open('training_report.json', 'w') as f:
            json.dump(report, f)

if __name__ == '__main__':
    test_model_training()