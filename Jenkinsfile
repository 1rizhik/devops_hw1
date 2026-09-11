pipeline {
    agent any

    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
        IMAGE_NAME   = "1rizhik/devops_hw1"
        IMAGE_TAG    = "jenkins-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== Checkout ==='
                checkout scm
                sh 'git log --oneline -3'
            }
        }

        stage('Setup Python venv') {
            steps {
                echo '=== Setup Python venv ==='
                sh '''
                    python3 -m venv .venv-jenkins
                    . .venv-jenkins/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                echo '=== Run pytest ==='
                sh '''
                    . .venv-jenkins/bin/activate
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                echo '=== Build Docker image ==='
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '=== Push to Docker Hub ==='
                sh '''
                    echo "$DOCKER_CREDS_PSW" | docker login -u "$DOCKER_CREDS_USR" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                    docker logout
                '''
            }
        }

                stage('Functional test') {
            steps {
                echo '=== Run functional tests ==='
                sh '''
                    docker rm -f jenkins-test-api 2>/dev/null || true
                    docker run -d --name jenkins-test-api -p 5001:5000 ${IMAGE_NAME}:latest

                    echo "--- Waiting for API ---"
                    for i in $(seq 1 30); do
                        if curl -s -f http://localhost:5001/health > /dev/null 2>&1; then
                            echo "API is up after ${i}s"
                            break
                        fi
                        echo "Attempt ${i}/30 - API not ready yet"
                        sleep 1
                    done

                    echo "--- /health ---"
                    curl -f http://localhost:5001/health || { docker logs jenkins-test-api; exit 1; }

                    echo "--- /predict authentic ---"
                    curl -f -X POST http://localhost:5001/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [2.3718, 7.4908, 0.015989, -1.7414]}' || { docker logs jenkins-test-api; exit 1; }

                    echo "--- /predict fake ---"
                    curl -f -X POST http://localhost:5001/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [-1.4446, 2.1438, -0.47241, -1.6677]}' || { docker logs jenkins-test-api; exit 1; }

                    echo "--- Container logs ---"
                    docker logs jenkins-test-api

                    docker stop jenkins-test-api
                    docker rm jenkins-test-api
                '''
            }
        }

    post {
        always {
            sh 'docker logout 2>/dev/null || true'
        }
        success {
            echo '=== Pipeline SUCCESS ==='
        }
        failure {
            echo '=== Pipeline FAILED ==='
        }
    }
}