# Translation Examples

This directory contains example files for testing the translator skill.

## Files

- **sample.html**: A sample HTML document with formatting that can be used to test translation while preserving HTML structure.

## Testing the Skill

### Test HTML Translation to Spanish:
```bash
python .agent/skills/translator/scripts/translate.py .agent/skills/translator/examples/sample.html --lang es --out .agent/skills/translator/examples/sample_es.html
```

### Test HTML Translation to Portuguese:
```bash
python .agent/skills/translator/scripts/translate.py .agent/skills/translator/examples/sample.html --lang pt --out .agent/skills/translator/examples/sample_pt.html
```

### Test HTML Translation to English:
```bash
python .agent/skills/translator/scripts/translate.py .agent/skills/translator/examples/sample.html --lang en --out .agent/skills/translator/examples/sample_en.html
```

## Expected Behavior

The translated files should:
1. Maintain all HTML tags and attributes
2. Preserve inline styles
3. Translate only the text content
4. Keep the same file structure as the original
