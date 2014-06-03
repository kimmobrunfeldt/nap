# Developer documentation

To get started, install requirements with *pip*:

    pip install -r requirements.txt
    pip install -r requirements-dev.txt

## Basic tasks

Makefile contains all useful tasks:

    clean - execute all clean tasks
    clean-build - remove build artifacts
    clean-pyc - remove Python file artifacts
    clean-coverage - remove coverage artifacts
    lint - check style with flake8
    test - run tests quickly with the default Python
    test-all - run tests on every Python version with tox
    coverage - check code coverage quickly with the default Python
    release - package and upload a release
    dist - package

Example usage `make test`

## Making a release

By default, `release` task makes a *patch* release.

* Commit your changes
* Run `make release`

    It will automatically update dev version to newer release version, push code and tags

* Checkout the tag you created and run `make pypi` to release the tag to PyPi

You can also specify *bump* parameter to `release` task:

  make release bump=major

Valid values: `major`, `minor`, `patch`.

* Add release notes to GitHub

## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

### Types of Contributions

#### Report Bugs

Report bugs at https://github.com/kimmobrunfeldt/nap/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

#### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

#### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

#### Write Documentation

nap could always use more documentation, whether as part of the
official nap docs, in docstrings, or even on the web in blog posts,
articles, and such.

#### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/kimmobrunfeldt/nap/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

### Get Started!

Ready to contribute? Here's how to set up `nap` for
local development.

1. [Fork](https://github.com/kimmobrunfeldt/nap/fork) the `nap` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/nap.git

3. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

4. When you're done making changes, check that your changes pass style and unit
   tests, including testing other Python versions with tox::

    $ tox

To get tox, just pip install it.

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 2.6, 2.7, and 3.3, and for PyPy.
   Check https://travis-ci.org/kimmobrunfeldt/nap
   under pull requests for active pull requests or run the ``tox`` command and
   make sure that the tests pass for all supported Python versions.


### Tips

To run a subset of tests::

     $ py.test test/test_nap.py
