#!/usr/bin/env python3
"""
批量更新HTML文件中的CDN引用为本地引用
"""
import os
import re
import glob

def update_html_file(filepath):
    """更新单个HTML文件中的引用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. 替换Font Awesome CDN引用
    content = re.sub(
        r'<link[^>]*href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]*"[^>]*>',
        '<link href="assets/css/font-awesome.min.css" rel="stylesheet">',
        content
    )

    # 2. 替换Google Fonts CDN引用
    content = re.sub(
        r'<link[^>]*href="https://fonts\.googleapis\.com/css[^"]*"[^>]*>',
        '<link href="assets/css/fonts.css" rel="stylesheet">',
        content
    )

    # 3. 替换Tailwind CSS CDN引用
    content = re.sub(
        r'<script[^>]*src="https://cdn\.tailwindcss\.com"[^>]*></script>',
        '<script src="assets/js/tailwindcss.js"></script>',
        content
    )

    # 4. 如果文件内容有变化，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # 获取所有HTML文件
    html_files = glob.glob('*.html')

    updated_count = 0
    skipped_count = 0

    print(f"Found {len(html_files)} HTML files to process...\n")

    for filepath in html_files:
        filename = os.path.basename(filepath)
        if update_html_file(filepath):
            print(f"✓ Updated: {filename}")
            updated_count += 1
        else:
            print(f"  Skipped: {filename} (no changes needed)")
            skipped_count += 1

    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Updated: {updated_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
