pipeline {
    agent any

    // This triggers the pipeline automatically when code is pushed to GHE
    triggers {
        githubPush() 
    }

    environment {
        IMAGE_NAME = 'python-calculator-app'
        CONTAINER_NAME = 'calculator-container'
        HOST_PORT = '5050'
        CONTAINER_PORT = '5060'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your configured GitHub repo
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:latest..."
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy to Local Endpoint') {
            steps {
                script {
                    echo "Stopping and removing existing container..."
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """

                    echo "Starting new container..."
                    sh "docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                    
                    echo "Checking container application status..."
                    sh "sleep 3"
                    // This will print the actual Flask boot logs directly into your Jenkins console
                    sh "docker logs ${CONTAINER_NAME}"
                }
            }
        }
    }
    
   post {
        success {
            script {
                echo "Waiting 5 seconds for Flask application to initialize..."
                sh "sleep 5"
                
                echo "Testing the local endpoint with proxy bypass..."
                // Added --noproxy "*" to explicitly ignore any background corporate proxies
                sh "curl --noproxy '*' 'http://localhost:5050/calculate?op=add&a=10&b=5'"
            }
        }
        failure {
            echo "Deployment Failed. Check the Jenkins build logs for details."
        }
    }
}
