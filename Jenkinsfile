pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/kanyanaJashi/outilsversioning.git'
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    def pythonInterpreter = tool 'Python 3' // Ensure you have a Python 3 tool configured in Jenkins
                    if (!pythonInterpreter) {
                        error("Python 3 tool not configured in Jenkins.")
                    }
                    env.PATH = "${pythonInterpreter}/bin:${env.PATH}"
                }
                sh 'pip install -r requirements.txt' // Assuming you have a requirements.txt file
                sh 'pip install pytest pytest-cov' // For running tests and generating coverage (optional)
                sh 'pip install pandas scikit-learn' // Ensure necessary libraries for model testing are installed
            }
        }

        
