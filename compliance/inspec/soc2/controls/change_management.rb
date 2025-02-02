control 'soc2-5' do
  impact 1.0
  title 'Change Management Controls'
  
  describe file('/app/CHANGELOG.md') do
    it { should exist }
    its('content') { should match /## \[\d+\.\d+\.\d+\]/ }
  end
end 