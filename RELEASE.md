Pypi
====

Preparation:
* increment version in `setup.py`
* add new changelog section in `CHANGES.rst`
* commit/push all changes

Commands for releasing on pypi-waikato (requires twine >= 1.8.0):

```
  rm -r dist src/wai.annotations.egg-info 
  python setup.py clean
  python setup.py sdist
  twine upload dist/*
```


Github
======

Steps:
* start new release (version: `vX.Y.Z`)
* enter release notes, i.e., significant changes since last release
* upload `wai.annotations-X.Y.Z.tar.gz` previously generated with `setup.py`
* publish

