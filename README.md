# Twitter Clone Search Tool

This tool helps you search for existing Twitter clone repositories in the code IDE user code system.

## Features

- 🔍 Search through all user directories for Twitter-related content
- 📁 Filter by specific user
- 🏷️ Filter by file type
- 🎯 Custom keyword search
- 📝 Detailed content preview
- 📊 Summary statistics

## Usage

### Basic Search
```bash
python search_cli.py
```

### Search for a specific user
```bash
python search_cli.py --user @kunal_me
```

### Search with verbose output
```bash
python search_cli.py --verbose
```

### Search for specific file types
```bash
python search_cli.py --file-type .py
python search_cli.py --file-type html
```

### Search with custom keywords
```bash
python search_cli.py --keyword "flask"
```

### Combined options
```bash
python search_cli.py --user @kunal_me --file-type .py --verbose
```

## Search Keywords

The tool automatically searches for these Twitter-related keywords:
- twitter
- tweet
- clone
- social
- post
- follow
- timeline
- user
- profile
- hashtag
- mention
- retweet

## File Types Supported

- `.py` - Python files
- `.js` - JavaScript files
- `.ts` - TypeScript files
- `.jsx` - React JSX files
- `.tsx` - React TypeScript files
- `.html` - HTML files
- `.css` - CSS files

## Example Output

```
🔍 Searching for Twitter clone repositories...
============================================================
✅ Found 2 files with Twitter-related content:

1. 👤 User: @kunal_me
   📁 Space UUID: 89561075-db87-48ca-a7a9-957051c16615
   📄 File: @kunal_me/twitter_clone_backend.py
   🏷️  Type: .py
   🎯 Matches: 144

2. 👤 User: @kunal1122
   📁 Space UUID: 754be4c1-a76f-473d-bfdb-93d66f674444
   📄 File: @kunal1122/twitter_clone_frontend.html
   🏷️  Type: .html
   🎯 Matches: 109

📊 Summary:
   • Total files found: 2
   • Total matches: 253
   • Users with Twitter clones: @kunal1122, @kunal_me
```

## Files

- `search_twitter_clone.py` - Core search functionality
- `search_cli.py` - Command-line interface
- `README.md` - This documentation

## Requirements

- Python 3.6+
- No external dependencies required