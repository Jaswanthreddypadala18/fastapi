
pipeline {
    agent any

    environment {
        APP_NAME = "fastapi-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Jaswanthreddypadala18/fastapi.git'
            }
        }

        stage('Build') {
            steps {
                sh 'pip install -r Requirements.txt'
                sh 'pip install pytest'
                sh 'python --version'
                echo 'Building is done'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest'
                echo 'Testing done'
            }
        }

        stage('Run') {
            steps {
                sh 'uvicorn main:app --host 0.0.0.0 --port 8000 &'
                echo 'App is running'
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



