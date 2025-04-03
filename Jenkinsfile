pipeline {
    agent any
    
    environment {
        PROJECT_DIR = 'ml-web-app'
        PYTHON = 'python3'
        // Pour DVC avec Google Drive
        GDRIVE_CREDS = credentials('gdrive-service-account') 
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/kenkleven/outilsversioning.git'
                
                // Configurer DVC
                sh '''
                mkdir -p ~/.config/dvc
                echo "$GDRIVE_CREDS" > ~/.config/dvc/gdrive-creds.json
                dvc remote modify dvcexam --local gdrive_service_account_json_file_path ~/.config/dvc/gdrive-creds.json
                dvc pull
                '''
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                virtualenv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pip install pytest pytest-cov
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/ --cov=app --cov-report=xml:coverage.xml -v
                '''
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }
        
        stage('Integration Test - Model Training') {
            steps {
                sh '''
                . venv/bin/activate
                python tests/train_test_model.py
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'models/test_model_*.joblib', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'training_report.json', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            // Nettoyage
            sh 'rm -rf venv'
        }
    }
}