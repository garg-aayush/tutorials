# Quick Skill Creation Prompt

Copy and customize this prompt to create a new skill:

---

I need help creating a new skill called **[SKILL_NAME]**.

**Core Functionality:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

**Example Use Cases:**
1. "[Example request 1]"
2. "[Example request 2]"
3. "[Example request 3]"

**Requirements:**
- Use **uv** with inline script metadata (PEP 723) for dependency management
- Use **absolute paths** throughout (e.g., `/mnt/skills/user/[SKILL_NAME]/`)
- Include explicit guidance to **NOT change directories** with `cd` commands
- All scripts should be runnable with `uv run` from any directory
- Provide clear workflow guidelines and examples

**Process:**
1. Confirm requirements and ask clarifying questions
2. Initialize skill structure
3. Create scripts with uv inline metadata
4. Write SKILL.md with absolute paths and "no cd" guidance
5. Test the skill
6. Package as .skill file
7. Iterate based on feedback

---

## Real Example: PDF Merger Skill

I need help creating a new skill called **pdf-merger**.

**Core Functionality:**
- Merge multiple PDFs into one
- Split PDF into separate pages
- Extract specific page ranges
- Reorder pages

**Example Use Cases:**
1. "Merge these 3 PDFs into a single document"
2. "Split this PDF into individual pages"
3. "Extract pages 5-10 from this PDF"
4. "Reorder pages: move page 3 to position 1"

**Requirements:**
- Use **uv** with inline script metadata (PEP 723) for dependency management
- Use **absolute paths** throughout (e.g., `/mnt/skills/user/pdf-merger/`)
- Include explicit guidance to **NOT change directories** with `cd` commands
- All scripts should be runnable with `uv run` from any directory
- Provide clear workflow guidelines and examples

**Process:**
1. Confirm requirements and ask clarifying questions
2. Initialize skill structure
3. Create scripts with uv inline metadata
4. Write SKILL.md with absolute paths and "no cd" guidance
5. Test the skill
6. Package as .skill file
7. Iterate based on feedback
