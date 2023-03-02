#project('ante50', 'cython',
project('ante50',
  version : '0.1',
  default_options : ['warning_level=3'])

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())

configure_file(
  input: meson.project_name() + '.in',
  output: meson.project_name(),
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

ante50_sources = [
  '__init__.py',
  'main.py'
]

install_data(ante50_sources)

#exe = executable('ante50', 'ante50.c',
  #install : true)

#test('basic', exe)
