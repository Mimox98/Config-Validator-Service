pipeline {
    agent any

    environment {
        IMAGE_NAME = 'config-validator'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                script {
                    docker.image("${IMAGE_NAME}:${IMAGE_TAG}").inside {
                        sh 'pytest app/tests/ -v --tb=short'
                    }
                }
            }
        }

        stage('Validate Configs') {
            steps {
                echo 'Validating configuration files...'
                script {
                    docker.image("${IMAGE_NAME}:${IMAGE_TAG}").inside {
                        sh 'python scripts/validate_configs.py'
                    }
                }
            }
        }

        //After tests pass, the successful build is tagged as 'latest' so it can be easily deployed
        stage('Tag Image') {
            steps {
                echo 'Tagging Docker image...'
                script {
                    docker.image("${IMAGE_NAME}:${IMAGE_TAG}").tag("${IMAGE_NAME}:latest")
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f'
        }
        success {
            echo '✓ Pipeline completed successfully!'
        }
        failure {
            echo '✗ Pipeline failed. Check logs for details.'
        }
    }
}