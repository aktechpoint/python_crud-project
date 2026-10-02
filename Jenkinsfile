pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['dev', 'staging'],
            description: 'Select deployment environment'
        )

        booleanParam(
            name: 'RUN_MIGRATIONS',
            defaultValue: true,
            description: 'Run Django database migrations'
        )
    }

    environment {
        APP_DIR = '/opt/django-app'
        PYTHON = '/usr/local/bin/python3.11'
        VENV = '/opt/django-app/venv'

        GIT_URL = 'https://github.com/aktechpoint/python_crud-project.git'
        GIT_BRANCH = 'main'

        SERVICE_NAME = 'django-app'
    }

    stages {

        stage('git Checkout') {
            steps {
                echo "Deploying ${params.DEPLOY_ENV} environment"

                git branch: "${GIT_BRANCH}",
                    url: "${GIT_URL}"
            }
        }

        stage('Prepare Application') {
            steps {
                sh '''
                    set -e

                    sudo mkdir -p ${APP_DIR}

                    sudo cp -r . ${APP_DIR}/

                    sudo chown -R jenkins:jenkins ${APP_DIR}
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    set -e

                    if [ ! -d "${VENV}" ]; then
                        ${PYTHON} -m venv ${VENV}
                    fi

                    ${VENV}/bin/python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -e

                    ${VENV}/bin/python -m pip install --upgrade pip

                    ${VENV}/bin/pip install -r ${APP_DIR}/requirements.txt
                '''
            }
        }

        stage('Django Check') {
            steps {
                sh '''
                    set -e

                    cd ${APP_DIR}

                    ${VENV}/bin/python manage.py check
                '''
            }
        }

        stage('Database Migration') {
            when {
                expression {
                    return params.RUN_MIGRATIONS
                }
            }

            steps {
                sh '''
                    set -e

                    cd ${APP_DIR}

                    ${VENV}/bin/python manage.py migrate --noinput
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                sh '''
                    set -e

                    cd ${APP_DIR}

                    ${VENV}/bin/python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Restart Django') {
            steps {
                sh '''
                    set -e
        
                    echo "Restarting Django application..."
        
                    sudo -n /usr/local/bin/restart-django-app.sh
        
                    echo "Django service restarted and is active."
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    set -e

                    curl -f http://127.0.0.1:8000/health/ || \
                    curl -f http://127.0.0.1:8000/

                    echo "Django application is healthy"
                '''
            }
        }
    }

    post {
        success {
            echo "Django deployment completed successfully."
        }

        failure {
            echo "Django deployment failed."
        }

        always {
            echo "Cleaning Jenkins workspace..."
            cleanWs()
        }
    }
}
