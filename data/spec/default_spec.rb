require 'spec_helper'

describe package('httpd') do
  it { should be_installed }
end

describe file('/path/to/file') do
  it { should exist }
  it { should be_file }
  its(:content) { should match(/ServerName www.example.jp/) }
  its(:content) { should match 'ServerName www.example.jp' }
  multi_line_string = <<~"EOS"
  line 1 {
    line 2 {
      line 3
    }
  }
  EOS
  its(:content) { should match multi_line_string }
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

describe port(80) do
  it { should be_listening }
  it { should be_listening.with('tcp') }
end

describe command('apachectl -V') do
  its(:stdout) { should match(/Apache/) }
  multi_line_string = <<~"EOS"
  line 1 {
    line 2 {
      line 3
    }
  }
  EOS
  its(:stdout) { should match multi_line_string }
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
