control 'pci-4' do
  impact 1.0
  title 'Verify Access Control Settings'
  describe command('docker ps --format "{{.Names}} {{.User}}"') do
    its('stdout') { should_not include 'root' }
  end
end 