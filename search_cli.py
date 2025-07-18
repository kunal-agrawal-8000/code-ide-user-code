#!/usr/bin/env python3
"""
Interactive search interface for finding Twitter clone repositories.
"""

import argparse
import sys
from search_twitter_clone import TwitterCloneSearcher


def main():
    parser = argparse.ArgumentParser(
        description="Search for Twitter clone repositories in the code IDE system"
    )
    parser.add_argument(
        "--user", "-u", 
        help="Search only in a specific user's directory (e.g., @kunal_me)"
    )
    parser.add_argument(
        "--keyword", "-k",
        help="Search for a specific keyword in addition to Twitter-related terms"
    )
    parser.add_argument(
        "--file-type", "-t",
        help="Filter by file type (e.g., .py, .js, .html)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output with file content"
    )
    
    args = parser.parse_args()
    
    # Create searcher instance
    searcher = TwitterCloneSearcher()
    
    # Add custom keyword if provided
    if args.keyword:
        searcher.twitter_keywords.append(args.keyword.lower())
    
    # Filter file types if specified
    if args.file_type:
        if not args.file_type.startswith('.'):
            args.file_type = '.' + args.file_type
        searcher.code_extensions = [args.file_type]
    
    print("🔍 Searching for Twitter clone repositories...")
    print("=" * 60)
    
    # Search for results
    results = searcher.search_twitter_clones()
    
    # Filter by user if specified
    if args.user:
        results = [r for r in results if r['username'] == args.user]
    
    # Display results
    if not results:
        print("❌ No Twitter clone repositories found.")
        if args.user:
            print(f"   (searched in user: {args.user})")
        if args.keyword:
            print(f"   (searched for keyword: {args.keyword})")
        if args.file_type:
            print(f"   (searched in file type: {args.file_type})")
        return
    
    print(f"✅ Found {len(results)} files with Twitter-related content:")
    print()
    
    for i, result in enumerate(results, 1):
        print(f"{i}. 👤 User: {result['username']}")
        if result['user_details']:
            print(f"   📁 Space UUID: {result['user_details'].get('space_uuid', 'N/A')}")
        print(f"   📄 File: {result['file_path']}")
        print(f"   🏷️  Type: {result['file_type']}")
        print(f"   🎯 Matches: {len(result['matches'])}")
        
        if args.verbose:
            print(f"   📝 Content preview:")
            # Show first few matches with context
            for match in result['matches'][:5]:
                print(f"      Line {match['line_number']}: {match['line_content'][:80]}...")
                print(f"      🔍 Keyword: {match['keyword']}")
                print()
            
            if len(result['matches']) > 5:
                print(f"      ... and {len(result['matches']) - 5} more matches")
        
        print("─" * 50)
    
    # Show summary
    print(f"\n📊 Summary:")
    print(f"   • Total files found: {len(results)}")
    print(f"   • Total matches: {sum(len(r['matches']) for r in results)}")
    
    # Show users with Twitter clones
    users_with_clones = set(r['username'] for r in results)
    print(f"   • Users with Twitter clones: {', '.join(sorted(users_with_clones))}")


if __name__ == "__main__":
    main()