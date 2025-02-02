control 'soc2-5' do
  impact 1.0
  title 'Change Management Controls'
  
  describe file('/app/CHANGELOG.md') do
    it { should exist }
    its('content') { should match /## \[\d+\.\d+\.\d+\]/ }
  end

  describe directory('/app/.git') do
    it { should exist }
  end

  describe command('git log --format="%h %ae %s" -n 10') do
    its('stdout') { should match /^[a-f0-9]+ [^@]+@[^@]+\s+/ }
  end
end 