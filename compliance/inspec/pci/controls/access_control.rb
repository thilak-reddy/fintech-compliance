control 'pci-4' do
  impact 1.0
  title 'Verify Access Control Settings'
  
  describe file('/app/config') do
    its('mode') { should cmp '0600' }
    its('owner') { should eq 'app_user' }
  end
  
  describe command('docker ps --format "{{.Names}} {{.User}}"') do
    its('stdout') { should_not include 'root' }
  end
end 