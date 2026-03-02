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
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Run') {
            steps {
                sh 'nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &'
                echo 'App is running'
            }
        }
    }

    post {
        always {
            echo "Pipeline Completed"
        }
    }
}
    









