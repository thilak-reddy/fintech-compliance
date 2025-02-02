control 'pci-6' do
  impact 1.0
  title 'Password Policy Compliance'
  
  describe parse_config_file('/app/config/password_policy.json') do
    its(['minimum_length']) { should cmp >= 8 }
    its(['require_special_chars']) { should eq true }
    its(['require_numbers']) { should eq true }
    its(['max_age_days']) { should cmp <= 90 }
    its(['history_count']) { should cmp >= 4 }
  end

  describe command('grep -r "password_expiry" /app/config') do
    its('stdout') { should match /password_expiry.*=.*90/ }
  end
end 