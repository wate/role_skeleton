require 'serverspec'
require 'net/ssh'
require 'yaml'

host = ENV['TARGET_HOST']
ssh_config_files = ['./.vagrant/ssh-config'] + Net::SSH::Config.default_files
options = Net::SSH::Config.for(host, ssh_config_files)
options[:user] ||= 'vagrant'
options[:keys].push("#{Dir.home}/.vagrant.d/insecure_private_key")

set :backend, :ssh
set :host, host
set :ssh_options, options

def e(value)
  Regexp.escape(value.is_a?(String) ? value : value.to_s)
end

spec_dir = File.dirname(__FILE__)
role_dir = File.dirname(spec_dir)

test_vars = {}

var_file = File.join(role_dir, 'defaults', 'main.yml')
test_vars.merge!(YAML.load_file(var_file)) if File.exist?(var_file)

group_names = ['all']

var_file = File.join(role_dir, '.molecule', 'facts', host + '.yml')
if File.exist?(var_file)
  test_vars.merge!(YAML.load_file(var_file))
  if test_vars.key?('group_names')
    group_names = test_vars['group_names'].unshift('all')
  end
end

group_names.each do |name|
  var_file = File.join(role_dir, '.molecule', 'group_vars', name)
  test_vars.merge!(YAML.load_file(var_file)) if File.exist?(var_file)
end

var_file = File.join(role_dir, 'vars', 'main.yml')
test_vars.merge!(YAML.load_file(var_file)) if File.exist?(var_file)

set_property test_vars

RSpec.configure do |config|
  config.color = true
  config.tty = true
  config.formatter = :documentation
end
