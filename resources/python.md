- Check python code syntax by flake8

  ```
  flake8 foo.py
  flake8 .
  ```
- Ignore multiple files from flake8 in `tox.ini`.

  Do not use spaces between commas.
  ```
  [flake8]
  exclude = foo.py,bar.py.piyo.py
  ```
