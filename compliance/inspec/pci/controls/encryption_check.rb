control 'pci-2' do
    impact 1.0
    title 'Ensure transaction data is encrypted'
    
    describe command('docker logs pci-test-app') do
      # Looks for a Base64-like string following "Encrypted Transaction: "
      its('stdout') { should match /Encrypted Transaction: [A-Za-z0-9+\/=]+/ }
    end
  end
  