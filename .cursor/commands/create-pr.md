Analyze the staged changes, commits, and provided context to generate a PR draft. Wait for user approval, then execute the creation command.

## Rules

- **Phase 1: Draft & Review (MANDATORY START)**
  1. **Analyze**: Look at the staged files, commits and `@Diff`.
  2. **Generate Content**: Create a PR Title (Conventional Commits) and a Body based on the structure below.
  3. **List Files**: Explicitly list the files that will be included in this PR.
      - If **< 5 files** changed: List them all.
      - If **> 7 files** changed: Do **NOT** list every file. Instead, summarize them by directory or file type (e.g., "4 files in `/api`", "3 CSS files"). *Always* explicitly mention high-impact config files (e.g., `requirements.txt`, `package.json`).
  4. **STOP**: Present the Title, Body, and File Summary to the user. **Ask**: "Does this draft look correct? Should I proceed with creating the PR?"

- **Phase 2: Execution (ONLY after confirmation)**
  - If the user approves, use the terminal to run: 
    `gh pr create --title "<Generated Title>" --body "<Generated Body>"`
  - If the user requests changes, regenerate the draft first.

- **Content Structure for Draft**:
  1.  **Summary**: A high-level explanation of *what* changed and *why*.
  2.  **Key Changes**: 
      - Focus on logic changes.
      - **Grouping**: If many files are touched, group the bullet points by **functionality** rather than file name (e.g., "Refactored Error Handling in all service modules" instead of listing 10 files).
  3.  **Type of Change**: (Bug fix, New feature, Breaking change, Refactor).
  4.  **Testing Instructions**: Brief steps on verify. **Only add this section if the user explicitly asks for it**.

- **Tone & Accuracy**: Use active voice. Do not hallucinate features. Focus on technical logic.