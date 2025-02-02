control 'soc2-4' do
    impact 1.0
    title 'No hardcoded credentials'
    
    describe command('grep -r "password" /app') do
      its('stdout') { should eq '' }
    end
  end