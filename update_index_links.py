#!/usr/bin/env python3
"""
更新index.html中的链接，添加pages/前缀
"""
import re

def update_index_html():
    """更新index.html中的页面链接"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 将所有指向.html文件的链接添加pages/前缀
    # 但排除已经以pages/开头的链接和外部链接
    def replace_link(match):
        href = match.group(1)
        # 如果已经以pages/开头或者是外部链接，不修改
        if href.startswith('pages/') or href.startswith('http') or href.startswith('#'):
            return match.group(0)
        # 添加pages/前缀
        return f'href="pages/{href}"'

    content = re.sub(r'href="([^"]+\.html)"', replace_link, content)

    if content != original_content:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Updating index.html links...")
    if update_index_html():
        print("✓ Successfully updated index.html")
    else:
        print("- No changes needed for index.html")

if __name__ == "__main__":
    main()
