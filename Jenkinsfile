node {
    try {
        stage('Checkout') {
            // Pull code from Git repository
            git branch: 'master',
                url: 'https://github.com/Hostname47/python-script'
        }
        
        stage('Setup Python Environment') {
            sh 'python3 --version'
            
            // Install requirements if requirements.txt exists
            sh '''
            if [ -f requirements.txt ]; then
                pip3 install -r requirements.txt
            fi
            '''
        }
        
        stage('Execute Python Script') {
            // Execute your Python script
            sh 'python3 script.py'
        }
        
        // Success message
        echo 'Python script executed successfully!'
        
    } catch (Exception e) {
        // Handle failures
        echo "Build failed: ${e.getMessage()}"
        currentBuild.result = 'FAILURE'
        throw e
        
    } finally {
        // Clean workspace after build (always runs)
        cleanWs()
    }
}
