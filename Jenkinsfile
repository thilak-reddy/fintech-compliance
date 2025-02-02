pipeline {
    agent any
    environment {
        IMAGE_NAME = 'pci-test-app'
        CONTAINER_NAME = 'pci-test-app'
    }
    stages {
        stage('Setup Local Files') {
            steps {
                sh 'rm -rf *'
                sh 'rsync -av --exclude=".git" /Users/thilak_reddy/Desktop/fintech-compliance/ .'
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build --no-cache -t ${IMAGE_NAME} app/"
            }
        }

        stage('Run Application Container') {
            steps {
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8443:8443 ${IMAGE_NAME}"
                    sleep(time: 10, unit: 'SECONDS')
                    sh "docker logs ${CONTAINER_NAME}"
                }
            }
        }

        stage('Verify PCI Profile Structure') {
            steps {
                sh 'ls -la ${WORKSPACE}/compliance/inspec/pci'
            }
        }

        stage('Run PCI Compliance Tests') {
            steps {
                script {
                    sh """
                    echo 'Checking container logs...'
                    docker logs ${CONTAINER_NAME}

                    docker run --rm --platform linux/amd64 -e CHEF_LICENSE=accept \\
                      -v ${WORKSPACE}/compliance/inspec/pci:/profile \\
                      -v /var/run/docker.sock:/var/run/docker.sock \\
                      chef/inspec exec /profile --no-color --reporter json:/pci_report.json --target docker://${CONTAINER_NAME}

                    mv pci_report.json ${WORKSPACE}/compliance_logs/pci_report.json
                    """
                }
            }
        }

        stage('Run SOC2 Compliance Tests') {
            steps {
                script {
                    sh """
                    docker run --rm --platform linux/amd64 -e CHEF_LICENSE=accept \\
                      -v ${WORKSPACE}/compliance/inspec/soc2:/profile \\
                      -v /var/run/docker.sock:/var/run/docker.sock \\
                      chef/inspec exec /profile --no-color --reporter json:/soc2_report.json --target docker://${CONTAINER_NAME}

                    mv soc2_report.json ${WORKSPACE}/compliance_logs/soc2_report.json
                    """
                }
            }
        }
    }
    post {
        always {
            sh "docker logs ${CONTAINER_NAME} > compliance_logs/docker_logs.txt || true"
            sh "docker rm -f ${CONTAINER_NAME} || true"
            archiveArtifacts artifacts: 'compliance_logs/docker_logs.txt, compliance_logs/pci_report.json, compliance_logs/soc2_report.json', allowEmptyArchive: true
        }

        success {
            script {
                sh """
                cd /Users/thilak_reddy/Desktop/fintech-compliance/
                git add .
                git commit -m "test"
                git push
                """
            }
        }
    }
}
