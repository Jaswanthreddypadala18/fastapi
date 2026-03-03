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
                sh 'python3 -m pip install pytest'
                sh 'python3 --version'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $APP_NAME .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop fastapi-container || true
                docker rm fastapi-container || true
                docker run -d --name fastapi-container -p 80:8000 $APP_NAME
                '''
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









