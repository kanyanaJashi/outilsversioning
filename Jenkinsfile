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

        stage('Run Source Code Tests') {
            steps {
                sh 'pytest .' // Run tests from the root directory
                junit 'junit.xml' // Assuming pytest generates a junit.xml report
            }
            post {
                always {
                    junit 'junit.xml'
                }
            }
        }

        stage('Test Trained Model') {
            steps {
                script {
                    def pythonInterpreter = tool 'Python 3' // Ensure you have a Python 3 tool configured in Jenkins
                    if (!pythonInterpreter) {
                        error("Python 3 tool not configured in Jenkins.")
                    }
                    env.PATH = "${pythonInterpreter}/bin:${env.PATH}"
                }
                sh 'python Model/test_model.py data/your_test_data.csv model.pkl model_test_report.xml'
                junit 'model_test_report.xml'
            }
            post {
                always {
                    junit 'model_test_report.xml'
                }
            }
        }
    }

    tools {
        python 'Python 3' // Define a Python tool named 'Python 3' in Jenkins Global Tool Configuration
    }
}
