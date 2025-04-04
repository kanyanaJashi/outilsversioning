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
     agent any // Exécute le pipeline sur n'importe quel agent Jenkins disponible
 
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
                 checkout scm // Récupère le code source du dépôt GitHub
             }
         }
 
         stage('Setup') {
         stage('Install Dependencies') {
             steps {
                 bat '''
                     python -m venv venv || exit /b
                     call venv\\Scripts\\activate || exit /b
                     pip install -r requirements.txt || exit /b
                     pip install pytest pytest-cov || exit /b
                 '''
                 // Adaptez cette commande en fonction de votre langage et gestionnaire de paquets
                 sh 'pip install -r requirements.txt' // Exemple pour un projet Python
                 // ou
                 // sh 'npm install' // Exemple pour un projet Node.js
             }
         }
 
         stage('Unit Tests') {
         stage('Run Unit Tests') {
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
                 // Adaptez cette commande pour exécuter vos tests unitaires
                 sh 'python -m unittest discover -s tests' // Exemple pour un projet Python utilisant unittest
                 // ou
                 // sh 'npm test' // Exemple pour un projet Node.js utilisant un framework de test comme Jest ou Mocha
                 junit 'test-reports/*.xml' // Si vos tests génèrent des rapports JUnit (adaptez le chemin)
             }
             post {
                 always {
                     junit 'test-reports/*.xml' // Publie les résultats des tests même en cas d'échec
                 }
             }
         }
 
          stage('Nettoyage') {
         stage('Upload Test Data') {
             steps {
                 // Simulez l'upload de données de test ici.
                 // Dans un scénario réel, cela pourrait impliquer de copier des fichiers,
                 // de télécharger depuis un stockage cloud, etc.
                 sh 'echo "Simulating upload of test data..."'
                 sh 'mkdir -p test_data'
                 sh 'touch test_data/test_data.csv' // Crée un fichier de données de test factice
             }
         }
 
         stage('Train Model on Test Data') {
             steps {
                 // Adaptez cette commande pour exécuter l'entraînement de votre modèle
                 // en utilisant les données de test uploadées.
                 sh 'python train_model.py test_data/test_data.csv model.pkl' // Exemple
             }
         }
 
         stage('Test Model') {
             steps {
                 // Solution robuste avec script
                 // Adaptez cette commande pour exécuter des tests sur le modèle entraîné
                 sh 'python test_model.py model.pkl test_data/test_data.csv test_results.txt' // Exemple
                 // Vous devrez peut-être parser le fichier de résultats pour déterminer le succès/échec
                 script {
                     try {
                         bat 'if exist venv rmdir /s /q venv'
                     } catch (e) {
                         echo "Nettoyage échoué : ${e}"
                     def testResults = readFile('test_results.txt').trim()
                     if (testResults.contains('SUCCESS')) {
                         echo "Model testing successful."
                     } else {
                         error "Model testing failed: ${testResults}"
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
             echo "Pipeline finished."
             // Vous pouvez ajouter d'autres actions ici, comme l'envoi de notifications par email
         }
         success {
             echo "Tests passed successfully!"
         }
         failure {
             echo "Tests failed!"
         }
     }
 }
 }
