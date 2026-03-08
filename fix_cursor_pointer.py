#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复HTML文件，添加cursor-pointer类和hover效果
"""

import os
import re
from pathlib import Path

def fix_html_file(filepath):
    """修复单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 为按钮添加cursor-pointer
    # 匹配<button ...>但不包含cursor-pointer的
    content = re.sub(
        r'<button\s+([^>]*?)(?<!cursor-pointer\s)(?<!cursor-pointer)(class="[^"]*")([^>]*)>',
        lambda m: f'<button {m.group(1)}{m.group(2)} cursor-pointer{m.group(3)}>',
        content
    )
    
    # 2. 为style-card添加cursor-pointer和hover效果
    content = re.sub(
        r'class="([^"]*style-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-lg transition-all duration-200"',
        content
    )
    
    # 3. 为glass-card添加cursor-pointer和hover效果
    content = re.sub(
        r'class="([^"]*glass-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-lg hover:opacity-90 transition-all duration-200"',
        content
    )
    
    # 4. 为ai-card添加cursor-pointer和hover效果
    content = re.sub(
        r'class="([^"]*ai-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-lg transition-all duration-200"',
        content
    )
    
    # 5. 为bento-card添加cursor-pointer和hover效果
    content = re.sub(
        r'class="([^"]*bento-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-xl transition-all duration-200"',
        content
    )
    
    # 6. 为链接添加transition-colors duration-200（如果还没有）
    content = re.sub(
        r'<a\s+([^>]*?)class="([^"]*)"([^>]*?)(?<!transition-colors)(?<!duration-200)>(?!.*transition-colors)',
        lambda m: f'<a {m.group(1)}class="{m.group(2)} transition-colors duration-200"{m.group(3)}>',
        content
    )
    
    # 7. 为data-card添加cursor-pointer
    content = re.sub(
        r'class="([^"]*data-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-md transition-all duration-200"',
        content
    )
    
    # 8. 为zen-card添加cursor-pointer
    content = re.sub(
        r'class="([^"]*zen-card[^"]*)"',
        lambda m: f'class="{m.group(1)} cursor-pointer hover:shadow-lg transition-all duration-200"',
        content
    )
    
    # 如果内容有变化，保存文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    base_dir = Path('d:\\AIWorkspaces\\nav-static-ui-pro-max')
    html_files = list(base_dir.glob('*.html'))
    
    fixed_count = 0
    for html_file in html_files:
        if fix_html_file(html_file):
            fixed_count += 1
            print(f"✅ 已修复: {html_file.name}")
        else:
            print(f"⏭️  跳过: {html_file.name}")
    
    print(f"\n总共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
