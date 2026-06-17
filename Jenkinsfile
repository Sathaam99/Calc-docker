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
        CONTAINER_PORT = '5050'
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
                    echo "Stopping and removing existing container (if any)..."
                    // The || true prevents the pipeline from failing if this is the first deployment
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """

                    echo "Starting new container on port ${HOST_PORT}..."
                    // -d runs it in the background (detached)
                    sh "docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }
    
    post {
        success {
            echo "Deployment Successful! Calculator API is live at http://192.168.1.2:${HOST_PORT}/calculate"

            sh '''
            #Test Addition
            curl "http://192.168.1.2:5050/calculate?op=add&a=10&b=5"
            
            #Test Division
            curl "http://192.168.1.2:5050/calculate?op=div&a=20&b=4"
            
            #Test Health Check
            curl "http://192.168.1.2:5050/health"
            '''
        }
        failure {
            echo "Deployment Failed. Check the Jenkins build logs for details."
        }
    }
}
