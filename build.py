from pybuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('copy_resources')


default_task = ['analyze', 'publish']

name = 'github-licker'
version = '0.0.2'
summary = 'Licker - Your Github License Checker for Organisational Repositories.'
description = """
    Using the Github API v3 including the [Licenses API](https://developer.github.com/v3/licenses/) developer preview,
    Licker is able to check licenses of all repositories in your Github organisation. It helps especially identifying
    repos without license file.
    """
authors = [Author('Jan Brennenstuhl', 'jan@brennenstuhl.me')]
url = 'https://github.com/jbspeakr/github-licker'
license = 'Apache License 2.0'


@init
def set_properties(project):
    project.set_property("verbose", True)

    project.depends_on("docopt")

    project.set_property("flake8_include_test_sources", True)
    project.set_property('coverage_break_build', False)

    project.set_property("install_dependencies_upgrade", True)

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.set_property('dir_dist_scripts', 'scripts')

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3 :: Only'
    ])