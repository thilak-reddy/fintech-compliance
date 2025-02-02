pipeline {
    agent any
    
    environment {
        CHEF_LICENSE = "accept"  // Required for InSpec
    }
    
    stages {
        stage('Copy Files') {
            steps {
                // Adjust the source path as needed.
                sh '''
                cp -r /Users/thilak_reddy/Desktop/fintech-compliance ./
                '''
            }
        }
        
        stage('Run Application') {
            steps {
                // Change directory into the application folder and run the app.
                // The output is redirected to a log file (app.log) which InSpec will examine.
                dir('fintech-compliance/app') {
                    sh 'python app.py > app.log'
                }
            }
        }
        
        stage('Compliance Checks') {
            steps {
                dir('fintech-compliance') {
                    // Run PCI-DSS compliance tests and generate a JSON report.
                    sh 'inspec exec compliance/inspec/pci --no-color --reporter json:pci_report.json'
                    
                    // Run SOC2 compliance tests and generate a JSON report.
                    sh 'inspec exec compliance/inspec/soc2 --no-color --reporter json:soc2_report.json'
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
            // Optionally add notifications here.
        }
        failure {
            echo "Compliance checks failed. Aborting deployment and notifying teams."
            // Optionally add notifications or remediation triggers here.
        }
        always {
            sh 'ls -l fintech-compliance/*.json || echo "No reports found"'
            archiveArtifacts artifacts: '**/*_report.json'
            cleanWs()
        }
    }
}
