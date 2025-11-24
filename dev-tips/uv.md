# uv related tips
## Links:
- [uv documentation](https://docs.astral.sh/uv/)
- [uv cheatsheet](https://mathspp.com/blog/uv-cheatsheet)

## Tips
- Use `uv run --env-file .env` to load environment variables directly from your .env file
    - No need for `from dotenv import load_dotenv` and `load_dotenv()`
    - instead use `uv run --env-file .env`
- Use `uv run --with <package>` to execute a package on the fly without adding it to your dependencies.
    ```
    uv run --with openai pandas python my_script.py
    uv run --with pytest pytest tests/
    ```
- Use `uv cache` to inspect and manage uv’s cache
  - `uv cache dir` to show the directory of the cache
  - `uv cache prune` to clean only unused or stale environments instead of wiping everything
    - Helps reclaim space without rebuilding actively used environments
  - `uv cache clean` removes everything in the cache (please be careful with this)

-  Define dependencies directly in your script using uv’s inline metadata block
  - Allows running standalone scripts without a separate `requirements.txt` and keeps dependencies near the code that uses them
  ```python
  #!/usr/bin/env python3
  # /// script
  # requires-python = ">=3.10"
  # dependencies = [
  #     "pillow>=10.0.0",
  #     "google-genai>=1.0.0",
  # ]
  # ///
  "Python code..."
  ```

- format the files using ruff or black
  ```
  uv run --with ruff ruff format path/to/file.py
  uv run --with ruff ruff format .
  ```
- use uv's built-in formatter (Ruff under the hood)
  ```
  uv format # formats the files
  uv format --check # checks the files that need to be formatted
  uv format --diff # shows the differences between the files and the formatted files (without actually formatting them)
  ```
