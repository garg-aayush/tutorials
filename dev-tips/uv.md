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
