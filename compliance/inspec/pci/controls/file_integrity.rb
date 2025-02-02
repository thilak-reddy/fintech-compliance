control 'pci-5' do
  impact 1.0
  title 'File Integrity Monitoring'
  desc 'Verify critical files have not been modified unexpectedly'

  describe file('/app/app.py') do
    its('md5sum') { should eq '{{expected_hash}}' }  # Replace with actual hash
    its('mode') { should cmp '0644' }
    its('owner') { should eq 'app_user' }
  end

  describe command('find /app -type f -mtime -1 -ls') do
    its('stdout') { should_not match /authorized_keys|id_rsa|\.env/ }
  end
end 