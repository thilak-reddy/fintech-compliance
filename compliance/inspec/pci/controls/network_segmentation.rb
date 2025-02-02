control 'pci-7' do
  impact 1.0
  title 'Network Segmentation Verification'
  
  describe docker_container('pci-test-app') do
    its('NetworkMode') { should_not eq 'host' }
    its('Ports') { should_not include '22/tcp' }
  end

  describe command('netstat -tulpn') do
    its('stdout') { should_not match /.*:22\s/ }
    its('stdout') { should_not match /.*:3389\s/ }
  end
end 