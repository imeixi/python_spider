#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
白鹤三绝漫画转换工具

将漫画图片合并为PDF或EPUB格式

使用方法：
    python convert_comics.py [--pdf] [--epub] [--output 输出路径]
    
参数：
    --pdf: 转换为PDF格式
    --epub: 转换为EPUB格式
    --output: 指定输出文件路径
    
如果不指定格式，默认同时生成PDF和EPUB
"""

import os
import sys
import argparse
from converter import ComicsConverter

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将漫画图片合并为PDF或EPUB格式')
    parser.add_argument('--pdf', action='store_true', help='转换为PDF格式')
    parser.add_argument('--epub', action='store_true', help='转换为EPUB格式')
    parser.add_argument('--output', '-o', help='指定输出文件路径（不包含扩展名）')
    
    args = parser.parse_args()
    
    # 漫画目录路径
    comics_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "白鹤三绝-番外篇")
    
    # 创建转换器
    converter = ComicsConverter(comics_dir)
    
    # 如果没有指定格式，默认两种都生成
    if not args.pdf and not args.epub:
        args.pdf = True
        args.epub = True
    
    # 设置输出路径
    output_base = args.output
    if output_base is None:
        output_base = os.path.basename(comics_dir)
    
    results = []
    
    # 转换为PDF
    if args.pdf:
        pdf_path = converter.convert_to_pdf(f"{output_base}.pdf")
        if pdf_path:
            results.append(f"PDF文件: {pdf_path}")
    
    # 转换为EPUB
    if args.epub:
        epub_path = converter.convert_to_epub(f"{output_base}.epub")
        if epub_path:
            results.append(f"EPUB文件: {epub_path}")
    
    # 输出结果
    if results:
        print("\n转换结果:")
        for result in results:
            print(result)
    else:
        print("\n转换失败，未生成任何文件")

if __name__ == "__main__":
    main()