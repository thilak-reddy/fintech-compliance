control 'soc2-6' do
  impact 1.0
  title 'Incident Response Procedures'
  
  describe file('/app/docs/incident_response.md') do
    it { should exist }
    its('content') { should match /Emergency Contacts/ }
    its('content') { should match /Incident Classification/ }
    its('content') { should match /Response Procedures/ }
  end

  describe directory('/app/logs/incidents') do
    it { should exist }
    its('mode') { should cmp '0750' }
  end
end 