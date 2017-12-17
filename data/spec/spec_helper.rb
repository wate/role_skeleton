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

spec_dir = File.dirname(__FILE__)
role_dir = File.dirname(spec_dir)

test_vars = {}
var_file = File.join(role_dir, 'defaults', 'main.yml')
if File.exist?(var_file)
  merge_vars = YAML.load_file(var_file)
  test_vars.merge!(merge_vars) if merge_vars.is_a?(Hash)
end

molecule_config = YAML.load_file(File.join(role_dir, 'molecule.yml'))
if molecule_config.key?('ansible') && molecule_config['ansible'].key?('group_vars')
  if molecule_config['ansible']['group_vars'].key?('all')
    test_vars.merge!(molecule_config['ansible']['group_vars']['all'])
  end
end

var_file = File.join(role_dir, 'vars', 'main.yml')
if File.exist?(var_file)
  merge_vars = YAML.load_file(var_file)
  test_vars.merge!(merge_vars) if merge_vars.is_a?(Hash)
end

set_property test_vars

RSpec.configure do |config|
  config.color = true
  config.tty = true
  config.formatter = :documentation
end
