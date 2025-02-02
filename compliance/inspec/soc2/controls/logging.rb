control 'soc2-2' do
  impact 1.0
  title 'Logging and Monitoring'
  
  describe file('/app/logs') do
    it { should be_directory }
    its('mode') { should cmp '0755' }
  end
end 