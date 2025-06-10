import os
import re
import img2pdf
import ebooklib
from ebooklib import epub
from PIL import Image
import io
import logging

class ComicsConverter:
    def __init__(self, comics_dir):
        """
        初始化漫画转换器
        
        Args:
            comics_dir: 漫画目录路径
        """
        self.comics_dir = comics_dir
        self.chapters = []
        self._scan_chapters()
        
    def _scan_chapters(self):
        """
        扫描所有章节目录
        """
        # 获取所有章节目录
        if not os.path.exists(self.comics_dir):
            raise FileNotFoundError(f"漫画目录不存在: {self.comics_dir}")
            
        # 获取所有章节目录
        chapter_dirs = [d for d in os.listdir(self.comics_dir) 
                      if os.path.isdir(os.path.join(self.comics_dir, d))]
        
        # 提取章节编号并排序
        def extract_chapter_num(chapter_name):
            match = re.match(r'第(\d+)回', chapter_name)
            if match:
                return int(match.group(1))
            return float('inf')  # 无法解析的放到最后
        
        # 按章节编号排序
        chapter_dirs.sort(key=extract_chapter_num)
        self.chapters = chapter_dirs
        
    def _get_chapter_images(self, chapter_dir):
        """
        获取章节中的所有图片，并按顺序排序
        
        Args:
            chapter_dir: 章节目录名
            
        Returns:
            排序后的图片路径列表
        """
        chapter_path = os.path.join(self.comics_dir, chapter_dir)
        images = [f for f in os.listdir(chapter_path) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        # 按文件名中的序号排序
        def extract_image_num(image_name):
            match = re.match(r'(\d+)_', image_name)
            if match:
                return int(match.group(1))
            return 0
        
        images.sort(key=extract_image_num)
        return [os.path.join(chapter_path, img) for img in images]
    
    def convert_to_pdf(self, output_path=None):
        """
        将漫画转换为PDF文件
        
        Args:
            output_path: 输出PDF文件路径，默认为漫画目录名.pdf
            
        Returns:
            输出的PDF文件路径
        """
        if output_path is None:
            comics_name = os.path.basename(self.comics_dir)
            output_path = f"{comics_name}.pdf"
        
        print(f"开始转换为PDF: {output_path}")
        
        # 收集所有图片路径
        all_images = []
        for chapter in self.chapters:
            print(f"处理章节: {chapter}")
            chapter_images = self._get_chapter_images(chapter)
            all_images.extend(chapter_images)
        
        if not all_images:
            print("没有找到图片文件")
            return None
        
        # 转换为PDF
        try:
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(all_images))
            print(f"PDF转换完成: {output_path}")
            return output_path
        except Exception as e:
            print(f"PDF转换失败: {e}")
            return None
    
    def convert_to_epub(self, output_path=None):
        """
        将漫画转换为EPUB文件
        
        Args:
            output_path: 输出EPUB文件路径，默认为漫画目录名.epub
            
        Returns:
            输出的EPUB文件路径
        """
        if output_path is None:
            comics_name = os.path.basename(self.comics_dir)
            output_path = f"{comics_name}.epub"
        
        print(f"开始转换为EPUB: {output_path}")
        
        # 创建EPUB书籍
        book = epub.EpubBook()
        comics_name = os.path.basename(self.comics_dir)
        
        # 设置元数据
        book.set_identifier(f"comic-{comics_name}")
        book.set_title(comics_name)
        book.set_language('zh-CN')
        
        # 创建CSS样式
        style = 'body { text-align: center; }\nimg { max-width: 100%; }'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", 
                             media_type="text/css", content=style)
        book.add_item(nav_css)
        
        # 创建章节
        chapters = []
        toc = []
        spine = ['nav']
        
        for i, chapter_dir in enumerate(self.chapters):
            print(f"处理章节: {chapter_dir}")
            chapter_images = self._get_chapter_images(chapter_dir)
            
            # 为每个章节创建一个HTML文件
            chapter = epub.EpubHtml(title=chapter_dir, file_name=f'chapter_{i+1}.xhtml', lang='zh-CN')
            chapter.content = f'<h1>{chapter_dir}</h1>\n'
            
            # 添加章节中的每张图片
            for j, img_path in enumerate(chapter_images):
                try:
                    # 读取图片并转换为EPUB兼容格式
                    img = Image.open(img_path)
                    # 统一使用jpeg格式，避免格式识别问题
                    img_format = 'jpeg'
                    
                    # 转换图片到内存中
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format=img_format.upper())
                    img_data = img_buffer.getvalue()
                    
                    # 添加图片到EPUB
                    img_item_name = f"images/{chapter_dir.replace(' ', '_')}_{j+1}.{img_format}"
                    img_item = epub.EpubItem(
                        uid=f"image_{i+1}_{j+1}",
                        file_name=img_item_name,
                        media_type=f"image/{img_format}",
                        content=img_data
                    )
                    book.add_item(img_item)
                    
                    # 在章节中添加图片引用
                    chapter.content += f'<div><img src="{img_item_name}" alt="Page {j+1}"/></div>\n'
                    
                except Exception as e:
                    print(f"处理图片失败 {img_path}: {e}")
            
            book.add_item(chapter)
            chapters.append(chapter)
            toc.append(epub.Link(f'chapter_{i+1}.xhtml', chapter_dir, f'chapter{i+1}'))
            spine.append(chapter)
        
        # 添加导航
        book.toc = toc
        book.spine = spine
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # 生成EPUB文件
        try:
            epub.write_epub(output_path, book, {})
            print(f"EPUB转换完成: {output_path}")
            return output_path
        except Exception as e:
            print(f"EPUB转换失败: {e}")
            return None

def main():
    # 漫画目录路径
    comics_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "白鹤三绝")
    
    # 创建转换器
    converter = ComicsConverter(comics_dir)
    
    # 转换为PDF
    pdf_path = converter.convert_to_pdf()
    
    # 转换为EPUB
    epub_path = converter.convert_to_epub()
    
    print("\n转换结果:")
    if pdf_path:
        print(f"PDF文件: {pdf_path}")
    if epub_path:
        print(f"EPUB文件: {epub_path}")

if __name__ == "__main__":
    main()