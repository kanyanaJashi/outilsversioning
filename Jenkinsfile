pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/kanyanaJashi/outilsversioning.git'
            }
        }

        stage('List Repository Contents') {
            steps {
                sh 'ls -l' // List files and directories in the workspace
            }
        }

        stage('Show Requirements.txt Content') {
            steps {
                sh 'cat requirements.txt' // Display the content of requirements.txt
            }
        }

        stage('Run Flask App (Simple)') {
            steps {
                script {
                    def pythonInterpreter = tool 'Python 3' // Ensure you have a Python 3 tool configured in Jenkins
                    if (!pythonInterpreter) {
                        error("Python 3 tool not configured in Jenkins.")
                    }
                    env.PATH = "${pythonInterpreter}/bin:${env.PATH}"
                }
                sh 'pip install -r requirements.txt' // Install dependencies
                sh 'python app.py &' // Run the Flask app in the background (&)
                echo 'Flask app started in the background. Check your application logs or access it if it exposes a port.'
                // Note: This is a very basic way to run the app.
                // For proper testing and deployment, you'd likely need a more robust approach.
                // You might want to run tests against the running app in a subsequent stage.
            }
        }

        stage('Cleanup (Optional)') {
            steps {
                sh 'pkill -f app.py' // Attempt to stop the Flask app
                echo 'Attempted to stop the Flask app.'
            }
            when {
                always()
            }
        }
    }

    tools {
        python 'Python 3' // Define a Python tool named 'Python 3' in Jenkins Global Tool Configuration
    }
}
