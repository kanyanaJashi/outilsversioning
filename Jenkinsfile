pipeline {
    agent {
        label 'master' // Spécifiez explicitement un agent
    }
    
    environment {
        PROJECT_DIR = 'ml-web-app'
        PYTHON = 'python' // Sur Windows, utilisez 'python' au lieu de 'python3'
        GDRIVE_CREDS = credentials('gdrive-service-account')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/kenkleven/outilsversioning.git'
                
                // Configurer DVC pour Windows
                bat '''
                    mkdir "%USERPROFILE%\\.config\\dvc"
                    echo %GDRIVE_CREDS% > "%USERPROFILE%\\.config\\dvc\\gdrive-creds.json"
                    dvc remote modify myremote --local gdrive_service_account_json_path "%USERPROFILE%\\.config\\dvc\\gdrive-creds.json"
                    dvc pull
                '''
            }
        }
        
        stage('Setup') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
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
    }
    
    post {
        always {
            bat 'rmdir /s /q venv' // Nettoyage sous Windows
        }
    }
}