control 'pci-3' do
  impact 1.0
  title 'Verify TLS Configuration'
  desc 'Ensure secure TLS version and cipher suites are in use'
  
  describe ssl(port: 443).protocols('tls1.2') do
    it { should be_enabled }
  end
  
  describe ssl(port: 443).protocols('tls1.0', 'tls1.1') do
    it { should_not be_enabled }
  end
end 