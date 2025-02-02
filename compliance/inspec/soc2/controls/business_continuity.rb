control 'soc2-7' do
  impact 1.0
  title 'Business Continuity Testing'

  describe json('/app/backup/last_test.json') do
    its(['recovery_time']) { should be < 240 } # 4 hours in minutes
    its(['success']) { should eq true }
    its(['data_integrity_check']) { should eq true }
  end
end 