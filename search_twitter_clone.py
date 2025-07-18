#!/usr/bin/env python3
"""
Search for Twitter clone repositories in the code IDE user code system.
This script searches through user directories and file contents to find 
Twitter-related projects.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any


class TwitterCloneSearcher:
    """Search for Twitter clone repositories and files."""
    
    def __init__(self, root_directory: str = "."):
        self.root_directory = Path(root_directory)
        self.twitter_keywords = [
            "twitter", "tweet", "clone", "social", "post", "follow", 
            "timeline", "user", "profile", "hashtag", "mention", "retweet"
        ]
        self.code_extensions = [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css"]
        
    def search_twitter_clones(self) -> List[Dict[str, Any]]:
        """Search for Twitter clone projects."""
        results = []
        
        # Search through all user directories
        for user_dir in self.root_directory.iterdir():
            if user_dir.is_dir() and user_dir.name.startswith("@"):
                user_results = self._search_user_directory(user_dir)
                if user_results:
                    results.extend(user_results)
        
        return results
    
    def _search_user_directory(self, user_dir: Path) -> List[Dict[str, Any]]:
        """Search within a specific user directory."""
        results = []
        username = user_dir.name
        
        # Get user details if available
        user_details = self._get_user_details(user_dir)
        
        # Search for files with Twitter-related content
        for file_path in user_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.code_extensions:
                matches = self._search_file_content(file_path)
                if matches:
                    results.append({
                        "username": username,
                        "user_details": user_details,
                        "file_path": str(file_path.relative_to(self.root_directory)),
                        "matches": matches,
                        "file_type": file_path.suffix
                    })
        
        return results
    
    def _get_user_details(self, user_dir: Path) -> Dict[str, Any]:
        """Get user details from UserDetails.json if available."""
        details_files = list(user_dir.rglob("UserDetails.json"))
        if details_files:
            try:
                with open(details_files[0], 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}
    
    def _search_file_content(self, file_path: Path) -> List[Dict[str, Any]]:
        """Search for Twitter-related content in a file."""
        matches = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    for keyword in self.twitter_keywords:
                        if keyword in line_lower:
                            matches.append({
                                "line_number": line_num,
                                "line_content": line.strip(),
                                "keyword": keyword,
                                "context": self._get_line_context(lines, line_num - 1)
                            })
        except Exception:
            # Skip files that can't be read
            pass
        
        return matches
    
    def _get_line_context(self, lines: List[str], line_index: int, context_lines: int = 2) -> List[str]:
        """Get context lines around a match."""
        start = max(0, line_index - context_lines)
        end = min(len(lines), line_index + context_lines + 1)
        return lines[start:end]
    
    def display_results(self, results: List[Dict[str, Any]]) -> None:
        """Display search results in a formatted way."""
        if not results:
            print("No Twitter clone repositories found.")
            return
        
        print(f"Found {len(results)} files with Twitter-related content:")
        print("=" * 60)
        
        for result in results:
            print(f"\nUser: {result['username']}")
            if result['user_details']:
                print(f"Space UUID: {result['user_details'].get('space_uuid', 'N/A')}")
            print(f"File: {result['file_path']}")
            print(f"Type: {result['file_type']}")
            print(f"Matches: {len(result['matches'])}")
            
            # Show first few matches
            for match in result['matches'][:3]:
                print(f"  Line {match['line_number']}: {match['line_content']}")
                print(f"    Keyword: {match['keyword']}")
            
            if len(result['matches']) > 3:
                print(f"  ... and {len(result['matches']) - 3} more matches")
            print("-" * 40)


def main():
    """Main function to run the Twitter clone search."""
    searcher = TwitterCloneSearcher()
    
    print("Searching for Twitter clone repositories...")
    results = searcher.search_twitter_clones()
    
    searcher.display_results(results)
    
    # Also search for files with "twitter" in the name
    print("\n" + "=" * 60)
    print("Searching for files with 'twitter' in filename...")
    
    twitter_files = []
    for file_path in Path(".").rglob("*twitter*"):
        if file_path.is_file():
            twitter_files.append(str(file_path))
    
    if twitter_files:
        print(f"Found {len(twitter_files)} files with 'twitter' in filename:")
        for file_path in twitter_files:
            print(f"  {file_path}")
    else:
        print("No files found with 'twitter' in filename.")


if __name__ == "__main__":
    main()