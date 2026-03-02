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
                sh 'python3 -m pip install -r Requirements.txt'
                sh 'python3 -m pip install pytest'
                sh 'python3 --version'
                echo 'Building is done'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
                echo 'Testing done'
            }
        }

        stage('Run') {
            steps {
                sh 'nohup uvicorn main:app --host 0.0.0.0 --port 8000 &'
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






