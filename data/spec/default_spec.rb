require 'spec_helper'

describe package('httpd') do
  it { should be_installed }
end

describe file('/path/to/file') do
  it { should exist }
  it { should be_file }
  its(:content) { should match(/ServerName www.example.jp/) }
  it { should contain 'ServerName www.example.jp' }
  it { should contain('rspec').from(/^group :test do/).to(/^end/) }
  it { should contain('rspec').after(/^group :test do/) }
  it { should contain('rspec').before(/^end/) }
  it { should be_directory }
  it { should be_readable }
  it { should be_writable }
  it { should be_symlink }
  it { should be_linked_to '/etc/redhat-release' }
  it { should be_executable }
  it { should be_mode 440 }
end

describe service('ntpd') do
  it { should be_enabled }
  it { should be_running }
end

describe command('apachectl -V') do
  its(:stdout) { should match(/Apache/) }
  its(:stdout) { should contain('Prefork') }
  its(:stdout) { should contain('Prefork').from(/^Server MPM/).to(/^Server compiled/) }
  its(:stdout) { should contain('conf/httpd.conf').after('SERVER_CONFIG_FILE') }
  its(:stdout) { should contain(' Apache/2.2.29').before('Server built') }
  its(:stderr) { should match(/apachectl: command not found/) }
  its(:exit_status) { should eq 0 }
end

describe user('apache') do
  it { should exist }
  it { should belong_to_group 'apache' }
  it { should belong_to_primary_group 'apache' }
  it { should have_uid 0 }
  it { should have_home_directory '/root' }
  it { should have_login_shell '/bin/bash' }
  it { should have_authorized_key 'ssh-rsa ABCDEFGHIJKLMNOPQRSTUVWXY..... foo@bar.local' }
end

describe group('wheel') do
  it { should exist }
  it { should have_gid 0 }
end

describe process('memcached') do
  its(:user) { should eq 'memcached' }
  its(:args) { should match(/-c 32000\b/) }
  its(:count) { should eq 1 }
  it { should be_running }
end
