Analyze the provided error logs, runtime issues, and given context to resolve the issue.

## Rules

- **Input Validation**: If no error message or context files are provided, STOP and ask the user to provide specific logs and reference relevant files.
- **Analysis & Strategy**: Briefly explain the root cause based on the stack trace and the execution command provided. State your plan before editing.
- **Direct Execution**: IMMEDIATELY after the explanation, use your file editing capabilities to modify the code. Do not wait for permission if the solution is clear.
- **Scope of Change**: Strictly limit edits to the code causing the error. Do not refactor unrelated code or change code style unless it causes the crash.
- **No Hallucinations**: 
  - If the error originates in a **User Files** not in context, request that file. 
  - If the error is in a **System Files** or **External Library Files**, do not request the file. Instead, try to fix the invocation or parameters within the user's code based on standard library usage. If you cannot fix it, make the user aware of the issue and ask them to fix it.
- **Commentary**: If the logic is non-obvious, add a one-line comment explaining the fix (e.g., `// Fixed: Handle undefined prop`).