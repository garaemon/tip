- Find files which have specific suffix

  ```
  find . -name "*.md"
  ```
- Replace specific keyword under some directories

  ```
  find . -type f -print0 | xargs -0 sed -i -e ¡Ès/foo/bar/g"
  ```
