pipeline {
    agent any
    
    environment {
        DOCKER_BUILDKIT = '1'
    }
    
    stages {
        stage('Security Scan') {
            steps {
                // Scan for secrets and security issues
                sh 'git secrets --scan'
                sh 'bandit -r .'
            }
        }
        
        stage('Build') {
            steps {
                // Build with security flags
                sh '''
                    docker build \
                    --no-cache \
                    --security-opt=no-new-privileges \
                    -t fintech-app .
                '''
            }
        }
        
        stage('Compliance Check') {
            steps {
                // Run compliance checks
                sh 'python3 compliance-check.py --pci --soc2'
                
                // Run InSpec tests for both PCI and SOC2
                sh '''
                    inspec exec compliance/inspec/pci \
                    --target docker://fintech-app \
                    --reporter cli json:compliance_logs/pci_results.json
                '''
                sh '''
                    inspec exec compliance/inspec/soc2 \
                    --target docker://fintech-app \
                    --reporter cli json:compliance_logs/soc2_results.json
                '''
                
                // Check backup and recovery
                sh 'python3 -c "import app.app; app.app.setup_backup()"'
                
                // Verify SSL/TLS configuration
                sh 'openssl s_client -connect localhost:8443 -tls1_2'
            }
        }
        
        stage('Security Tests') {
            steps {
                // Run security tests
                sh 'pytest tests/security/'
                
                // Check for hardcoded credentials
                sh 'inspec exec compliance/inspec/soc2/controls/no_hardcoded_creds.rb'
                
                // Verify file permissions
                sh '''
                    find . -type f -name "*.json" -exec stat -f "%Sp %N" {} \\;
                    find . -type f -name "*.key" -exec stat -f "%Sp %N" {} \\;
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                // Deploy with security configurations
                sh '''
                    docker-compose up -d \
                    --force-recreate \
                    --no-deps \
                    --remove-orphans
                '''
                
                // Verify deployment
                sh 'curl -k https://localhost:8443/health'
            }
        }
    }
    
    post {
        always {
            // Archive compliance and security logs
            archiveArtifacts artifacts: '''
                compliance_logs/*.txt,
                compliance_logs/*.json,
                app/logs/incidents/*.log
            '''
            
            // Clean up sensitive data
            sh '''
                docker-compose down
                find . -type f -name "*.key" -delete
                find . -type f -name "*.env" -delete
            '''
        }
        
        // failure {
        //     // Alert on failures
        //     // emailext (
        //     //     subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
        //     //     body: "Check the build log for details: ${env.BUILD_URL}",
        //     //     recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        //     // )
        // }
    }
}