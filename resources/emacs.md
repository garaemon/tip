* Run external script and get output as string.

  ```lisp
  (with-temp-buffer
    (shell-command command-string (current-buffer))
    (buffer-substring-no-properties (point-min) (point-max)))
  ```
* Split string with specified character.

  Use `\\` to escape special character.
  ```lisp
  (split-string "foo bar") ;; => ("foo" "bar")
  (split-string "foo bar" "a") ;; => ("foo b" "r")
  (split-string "1.2.3" "\\.") ;; => ("1" "2" "3")
  ```
