Generate a commit message for the staged changes, wait for user approval or edits, and then execute the commit.

## Rules

- **Input Validation**: Check if there are staged changes. If not, STOP and ask the user to stage changes first.

- **Phase 1: Draft & Review (MANDATORY START)**
  1. **Analyze**: Review the staged changes to understand the context.
  2. **Generate Message**: Create a **single-line** commit message using **present tense** and **active voice**.
     - *Constraint*: Reference the key files changed (or the module name if many files are changed).
  3. **STOP & Ask**: Present the proposed message clearly.
     - Ask: "Proposed Message: `[The Message]`"
     - Ask: "Shall I commit with this message, or would you like to provide a different one?"

- **Phase 2: Execution (ONLY after confirmation)**
  - **If User Approves**: Execute `git commit -m "The Message"`.
  - **If User Edits**: Use the *exact* text provided by the user and execute `git commit -m "User Message"`.

- **Style Guidelines**:
  - No newlines in the message.
  - Concise and descriptive.