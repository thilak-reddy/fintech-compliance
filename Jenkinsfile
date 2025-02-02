pipeline {
    agent any
    
    environment {
        CHEF_LICENSE = "accept"  // Required for InSpec
        DOCKER_IMAGE = "compliance-test-image"
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                // Install required packages
                sh '''
                    # Install Docker if not present
                    if ! which docker > /dev/null 2>&1; then
                        curl -fsSL https://get.docker.com -o get-docker.sh
                        sh get-docker.sh
                    fi
                    
                    # Install ChefDK/InSpec
                    which inspec || curl -L https://omnitruck.chef.io/install.sh | sudo bash -s -- -P chef-workstation
                '''
            }
        }

        stage('Copy Files') {
            steps {
                // Adjust the source path as needed.
                sh '''
                cp -r /Users/thilak_reddy/Desktop/fintech-compliance ./
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('fintech-compliance/app') {
                    sh '''
                        docker build -t ${DOCKER_IMAGE} .
                        docker run -d --name pci-test-app ${DOCKER_IMAGE}
                    '''
                }
            }
        }
        
        stage('Run Application Tests') {
            steps {
                // Wait for application to start and generate logs
                sh 'sleep 10'
                sh 'docker logs pci-test-app > app.log'
            }
        }
        
        stage('Compliance Checks') {
            steps {
                dir('fintech-compliance') {
                    script {
                        def pciResult
                        def soc2Result
                        
                        // Run PCI-DSS compliance tests with error handling
                        try {
                            pciResult = sh(script: '''
                                inspec exec compliance/inspec/pci \
                                    --no-color \
                                    --reporter json:pci_report.json \
                                    --target docker://pci-test-app
                            ''', returnStatus: true)
                            
                            if (pciResult != 0) {
                                echo "PCI-DSS compliance checks failed with exit code: ${pciResult}"
                                currentBuild.result = 'FAILURE'
                            }
                            
                            // Run SOC2 compliance tests with error handling
                            soc2Result = sh(script: '''
                                inspec exec compliance/inspec/soc2 \
                                    --no-color \
                                    --reporter json:soc2_report.json \
                                    --target docker://pci-test-app
                            ''', returnStatus: true)
                            
                            if (soc2Result != 0) {
                                echo "SOC2 compliance checks failed with exit code: ${soc2Result}"
                                currentBuild.result = 'FAILURE'
                            }
                        } catch (Exception e) {
                            echo "Error during compliance checks: ${e.getMessage()}"
                            currentBuild.result = 'FAILURE'
                            throw e
                        }
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                echo "Deploying the application as compliance checks passed..."
                // Add your deployment commands here.
            }
        }
    }
    
    post {
        success {
            echo "Compliance checks passed and deployment succeeded!"
            archiveArtifacts artifacts: '**/pci_report.json,**/soc2_report.json', allowEmptyArchive: true
        }
        failure {
            echo "Compliance checks failed. Aborting deployment and notifying teams."
            archiveArtifacts artifacts: '**/pci_report.json,**/soc2_report.json', allowEmptyArchive: true
            // Add notification logic here if needed
            // script {
            //     def reports = findFiles(glob: '**/*_report.json')
            //     reports.each { report ->
            //         echo "Contents of ${report.name}:"
            //         sh "cat ${report.path}"
            //     }
            // }
        }
        always {
            sh '''
                docker stop pci-test-app || true
                docker rm pci-test-app || true
                docker rmi ${DOCKER_IMAGE} || true
            '''
            cleanWs()
        }
    }
}