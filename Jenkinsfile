pipeline {
    agent {
        // Spécifiez explicitement un agent avec le label approprié
        label 'windows-agent' // ou 'master' si votre nœud principal est Windows
    }

    environment {
        PROJECT_DIR = 'ml-web-app'
        PYTHON = 'python' // Windows utilise 'python'
        GDRIVE_CREDS = credentials('gdrive-service-account')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // Méthode plus fiable pour le checkout
                
                script {
                    // Configuration spécifique Windows
                    def credsPath = "${env.USERPROFILE}\\.config\\dvc\\gdrive-creds.json"
                    bat """
                        mkdir "${env.USERPROFILE}\\.config\\dvc"
                        echo ${GDRIVE_CREDS} > "${credsPath}"
                        dvc remote modify myremote --local gdrive_service_account_json_path "${credsPath}"
                        dvc pull
                    """
                }
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    python -m venv venv || exit /b
                    call venv\\Scripts\\activate || exit /b
                    pip install -r requirements.txt || exit /b
                    pip install pytest pytest-cov || exit /b
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest tests/ --cov=app --cov-report=xml:coverage.xml -v
                '''
                post {
                    always {
                        junit '**/test-reports/*.xml'
                        publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                    }
                }
            }
        }

    stages {
        stage('Nettoyage') {
            steps {
                // Solution robuste avec script
                script {
                    try {
                        bat 'if exist venv rmdir /s /q venv'
                    } catch (e) {
                        echo "Nettoyage échoué : ${e}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Alternative plus sûre pour le post
                if (isUnix()) {
                    sh 'rm -rf venv || true'
                } else {
                    bat 'if exist venv rmdir /s /q venv || exit 0'
                }
            }
        }
    }
}
}