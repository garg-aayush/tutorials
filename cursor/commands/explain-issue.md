Analyze the provided error logs, runtime issues, and given context to explain the root cause and suggest a solution without editing files.

## Rules

- **Input Validation**: If no error message or context files are provided, STOP and ask the user to provide specific logs and reference relevant files.
- **Root Cause Analysis**: Identify and explain the specific cause of the error. Break down *why* the crash occurred based on the stack trace, context, and the execution command.
- **Passive Mode**: Do **NOT** edit any files. Your goal is strictly to explain the issue and suggest a solution without editing files.
- **Solution Presentation**: It should contain the specific root couse and the proposed solution and why it works.