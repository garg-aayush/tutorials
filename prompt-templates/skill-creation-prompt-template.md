# Skill Creation Prompt Template

Use this prompt to create custom skills with Claude. Replace the bracketed sections with your specific needs.

---

## Prompt to Claude:

I need help creating a new skill called **[SKILL_NAME]**.

### Core Functionality
The skill should support the following capabilities:
- [Capability 1]
- [Capability 2]
- [Capability 3]

### Example Use Cases
Here are specific examples of how I'll use this skill:

1. "[Example request 1]"
   - Input: [describe input]
   - Expected output: [describe output]

2. "[Example request 2]"
   - Input: [describe input]
   - Expected output: [describe output]

3. "[Example request 3]"
   - Input: [describe input]
   - Expected output: [describe output]

### Key Requirements
- Use **uv** with inline script metadata (PEP 723) for dependency management
- Use **absolute paths** throughout (e.g., `/mnt/skills/user/[SKILL_NAME]/`)
- Include explicit guidance to **NOT change directories** with `cd` commands
- All scripts should be runnable with `uv run` from any directory
- Output files should go directly to `/mnt/user-data/outputs/`
- Provide clear workflow guidelines and examples

### Technical Details
[Optional - add any specific technical requirements:]
- Programming language: [Python/Bash/etc.]
- Key libraries needed: [list libraries]
- File formats to support: [list formats]
- Special considerations: [any other requirements]

### Additional Context
[Optional - add any other relevant information about your use case]

---

Please follow this process:
1. Confirm you understand the requirements and ask any clarifying questions
2. Initialize the skill structure using the skill-creator tools
3. Create the necessary scripts with uv inline metadata
4. Write clear SKILL.md documentation with absolute paths and "no cd" guidance
5. Test the skill to ensure it works correctly
6. Package the skill into a distributable .skill file
7. Be ready to iterate based on my feedback

---

## Example: Image Editor Skill (for reference)

### Core Functionality
The skill should support:
- Format conversions (JPEG, PNG, TIFF, HEIC, WebP)
- Basic edits (rotate, resize, flip)
- Color adjustments (brightness, contrast, saturation)
- Transparency handling

### Example Use Cases
1. "Convert this JPEG to PNG"
2. "Replace the transparency channel by white color in this image"
3. "Rotate this image 90 degrees and increase brightness by 20%"
4. "Resize to 800x600 keeping the aspect ratio constant"

### Key Requirements
- Use uv with inline script metadata
- Use absolute paths (e.g., `/mnt/skills/user/image-editor/scripts/edit_image.py`)
- Never use `cd` commands
- Support chaining multiple operations in one command
- Clear documentation with concrete examples

---

## Tips for Success

### Be Specific with Examples
- Provide 3-5 concrete examples of how you'll use the skill
- Include actual input/output descriptions
- Think about edge cases or special scenarios

### Iterate and Refine
After the initial skill is created, consider:
- Are all paths absolute?
- Is the documentation clear about not using `cd`?
- Are examples using realistic file paths?
- Does it use uv for dependency management?
- Can it be run from any directory?
- Are error messages helpful?

### Common Improvements to Request
Based on the image-editor skill iteration:
1. "Use uv instead of manual pip install"
2. "Change all paths to absolute paths"
3. "Add explicit warning not to use cd commands"
4. "Update examples to show full absolute paths"
5. "Test the script works from any directory"

---

## Quick Start Template

**Minimal prompt:**

```
I need a skill for [BRIEF DESCRIPTION].

Examples of how I'll use it:
- "[Example 1]"
- "[Example 2]"
- "[Example 3]"

Requirements:
- Use uv with inline script metadata
- Use absolute paths throughout
- Add clear "do NOT cd" guidance
- Make it runnable from any directory

Please create this skill following best practices.
```

---

## After Creation Checklist

Before finalizing the skill, verify:
- [ ] Uses uv with PEP 723 inline script metadata
- [ ] All paths are absolute (script, input, output)
- [ ] SKILL.md has "do NOT cd" warning prominently displayed
- [ ] Examples show realistic absolute paths
- [ ] Workflow guidelines emphasize absolute path usage
- [ ] Tested from different directories (should always work)
- [ ] Dependencies auto-install on first run
- [ ] Clear documentation with multiple examples
- [ ] Packaged as .skill file successfully

---

## Example Directory Structure

```
skill-name/
├── SKILL.md (with absolute path guidance)
└── scripts/
    └── main_script.py (with uv inline metadata)
```

Keep it simple! Only add `references/` or `assets/` directories if truly needed.
