control 'soc2-7' do
  impact 1.0
  title 'Business Continuity Testing'
  
  describe file('/app/backup/last_test.json') do
    it { should exist }
    its('mtime') { should be > Time.now - 90*24*60*60 } # 90 days
  end

  describe json('/app/backup/last_test.json') do
    its(['recovery_time']) { should be < 240 } # 4 hours in minutes
    its(['success']) { should eq true }
    its(['data_integrity_check']) { should eq true }
  end
end 