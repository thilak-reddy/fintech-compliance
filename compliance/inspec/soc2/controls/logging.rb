control 'soc2-2' do
  impact 1.0
  title 'Logging and Monitoring'
  
  describe file('/app/logs') do
    it { should be_directory }
    its('mode') { should cmp '0755' }
  end
  
  describe command('docker logs pci-test-app') do
    its('stdout') { should match /\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\]/ }
  end
end 