control 'pci-1' do
    impact 1.0
    title 'Prevent PAN in logs'
    
    describe command('docker logs pci-test-app') do
      its('stdout') { should_not match /\d{4}-\d{4}-\d{4}-\d{4}/ }
    end
  end
  