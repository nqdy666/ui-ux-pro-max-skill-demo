#!/usr/bin/env python3
"""
将除index.html外的所有HTML文件移动到pages目录，
并更新静态资源引用路径
"""
import os
import re
import shutil
import glob

def update_html_resource_paths(filepath, is_in_pages_dir=False):
    """更新HTML文件中的静态资源引用路径"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if is_in_pages_dir:
        # 在pages目录中的文件，需要将assets/改为../assets/
        content = re.sub(
            r'(href|src)="assets/',
            r'\1="../assets/',
            content
        )
        # 更新返回首页的链接
        content = re.sub(
            r'href="index.html"',
            'href="../index.html"',
            content
        )
        # 更新其他页面链接（从pages目录中的文件指向其他页面）
        content = re.sub(
            r'href="([^"]+\.html)"',
            lambda m: f'href="{m.group(1)}"' if m.group(1).startswith('http') or m.group(1).startswith('../') else f'href="{m.group(1)}"',
            content
        )
    else:
        # 在根目录中的文件（index.html），需要更新指向pages目录中文件的链接
        # 将直接指向其他html文件的链接改为指向pages/目录
        html_files = [os.path.basename(f) for f in glob.glob('pages/*.html')]
        for html_file in html_files:
            pattern = rf'href="{re.escape(html_file)}"'
            replacement = f'href="pages/{html_file}"'
            content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # 获取所有HTML文件（排除index.html）
    html_files = [f for f in glob.glob('*.html') if os.path.basename(f) != 'index.html']

    print(f"Found {len(html_files)} HTML files to move to pages directory...\n")

    # 第一步：先更新根目录中文件的链接（在移动文件之前）
    print("Step 1: Updating index.html links...")
    if os.path.exists('index.html'):
        if update_html_resource_paths('index.html', is_in_pages_dir=False):
            print("  ✓ Updated index.html")
        else:
            print("  - No changes needed for index.html")

    # 第二步：移动文件并更新引用
    print("\nStep 2: Moving files and updating resource paths...")
    moved_count = 0
    updated_count = 0

    for filepath in html_files:
        filename = os.path.basename(filepath)
        dest_path = os.path.join('pages', filename)

        # 先更新文件内容
        if update_html_resource_paths(filepath, is_in_pages_dir=True):
            updated_count += 1
            print(f"  ✓ Updated paths: {filename}")
        else:
            print(f"  - No path updates: {filename}")

        # 移动文件
        try:
            shutil.move(filepath, dest_path)
            moved_count += 1
            print(f"  ✓ Moved: {filename} -> pages/{filename}")
        except Exception as e:
            print(f"  ✗ Error moving {filename}: {e}")

    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Files moved: {moved_count}")
    print(f"  Files updated: {updated_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
