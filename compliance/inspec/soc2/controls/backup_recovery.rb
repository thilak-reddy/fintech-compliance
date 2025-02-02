control 'soc2-3' do
  impact 1.0
  title 'Backup and Recovery'
  
  describe file('/app/backup') do
    it { should be_directory }
  end
  
  describe command('find /app/backup -mtime -1 -name "*.backup"') do
    its('exit_status') { should eq 0 }
  end
end 