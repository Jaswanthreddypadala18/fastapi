pipeline {

    agent any
    





    environment {
        APP_NAME = "fastapi-app"
        DATABASE_URL = "mysql+pymysql://root:Jaswanth09@127.0.0.1:3306/candidates"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Jaswanthreddypadala18/fastapi.git'
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m pip install pytest flake8'
                sh 'python3 --version'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=fastapi-app \
                    -Dsonar.sources=. \
                    
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline Completed"
        }
        success {
            echo "Build Success"
        }
        failure {
            echo "Build Failed"
        }
    }
}



