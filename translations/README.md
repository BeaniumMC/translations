# Translations

The files are named like this: `<project>/<language>/<path>.json`. (ex: `server/fr/main.json`)  

View the original sources in the [`/sources`](/sources) folder.  

## File format

It is important to format the JSON correctly before creating a PR.  
You can use [jsonlint.com](https://jsonlint.com/) to check the file content before contributing.  

```json
{
    "key": "value",
    "some.translation.key": "some string"
}
```

**Important**  

- Do not leave empty or unknown strings in the translations!
- Always include double quotes around text! ("like this")
- Remember to always include the replacement symbols! (%s, %d, %1$s, %2$d)
- Do not use color codes with the paragraph symbol - §, only use ampersand - &!
