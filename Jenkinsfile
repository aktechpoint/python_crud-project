
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        DOCKERHUB_USER = ''
        IMAGE_NAME = 'abhishek625/testpy:tagname'

        DEPLOY_HOST = '15.252.239.24'
        DEPLOY_USER = 'deploy'
        CONTAINER_NAME = 'django-app'
        HOST_PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu

                    test -f manage.py
                    test -f Dockerfile
                    test -f requirements.txt

                    docker build \
                      -t "${IMAGE_NAME}:${BUILD_NUMBER}" \
                      -t "${IMAGE_NAME}:latest" .
                '''
            }
        }

        stage('Django System Check') {
            steps {
                sh '''
                    docker run --rm \
                      -e DJANGO_SECRET_KEY=ci-temporary-secret \
                      -e DJANGO_DEBUG=False \
                      -e DJANGO_ALLOWED_HOSTS=localhost \
                      "${IMAGE_NAME}:${BUILD_NUMBER}" \
                      python manage.py check
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_TOKEN'
                    )
                ]) {
                    sh '''
                        set -eu

                        echo "$DH_TOKEN" | docker login \
                          --username "$DH_USER" \
                          --password-stdin

                        docker push "${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker push "${IMAGE_NAME}:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Remote Ubuntu') {
            steps {
                sshagent(credentials: ['deploy-server-key']) {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub-creds',
                            usernameVariable: 'DH_USER',
                            passwordVariable: 'DH_TOKEN'
                        )
                    ]) {
                        sh '''
                            set -eu

                            # Authenticate on the deployment server.
                            printf '%s' "$DH_TOKEN" |
                              ssh -o BatchMode=yes \
                                "$DEPLOY_USER@$DEPLOY_HOST" \
                                "docker login -u '$DH_USER' --password-stdin"

                            # Pull the exact image produced by this build.
                            ssh "$DEPLOY_USER@$DEPLOY_HOST" \
                              "docker pull '$IMAGE_NAME:$BUILD_NUMBER' &&
                               docker logout"

                            # Replace the running container.
                            ssh "$DEPLOY_USER@$DEPLOY_HOST" "
                              docker rm -f '$CONTAINER_NAME' 2>/dev/null || true
                              docker run -d \
                                --name '$CONTAINER_NAME' \
                                --restart unless-stopped \
                                --env-file /opt/django-app/.env \
                                -p '$HOST_PORT:8000' \
                                '$IMAGE_NAME:$BUILD_NUMBER'
                            "
                        '''
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eu

                    for i in $(seq 1 20); do
                      if curl -fsS \
                        "http://${DEPLOY_HOST}:${HOST_PORT}/health/"; then
                        echo "Django deployment verified"
                        exit 0
                      fi
                      sleep 3
                    done

                    echo "Health check failed"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful: ${IMAGE_NAME}:${BUILD_NUMBER}"
        }

        failure {
            echo 'Pipeline failed. Review Console Output and remote container logs.'
        }

        always {
            sh '''
                docker image rm \
                  "${IMAGE_NAME}:${BUILD_NUMBER}" \
                  "${IMAGE_NAME}:latest" 2>/dev/null || true
            '''
        }
    }
}
