import os
import re
import time
import requests
from bs4 import BeautifulSoup
import json

class ComicsSpider:
    def __init__(self, base_url, save_dir='comics'):
        """初始化爬虫
        
        Args:
            base_url: 漫画首页URL
            save_dir: 保存漫画的目录
        """
        self.base_url = base_url
        self.domain = 'https://www.antbyw.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def get_html(self, url):
        """获取页面HTML内容
        
        Args:
            url: 页面URL
            
        Returns:
            页面HTML内容
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求异常: {e}")
            return None
    
    def parse_image_urls(self, html):
        """从HTML中解析图片URL列表
        
        Args:
            html: 页面HTML内容
            
        Returns:
            图片URL列表和章节名称
        """
        try:
            # 提取章节名称
            chapter_name_match = re.search(r'<h3 class="uk-heading-line uk-text-center"><span>([^<]+)</span></h3>', html)
            chapter_name = chapter_name_match.group(1) if chapter_name_match else "未知章节"
            
            # 提取图片URL数组
            urls_match = re.search(r'let urls = (\[[^\]]+\])', html)
            if urls_match:
                urls_str = urls_match.group(1)
                # 将字符串转换为Python列表
                urls = json.loads(urls_str)
                return urls, chapter_name
            else:
                print("未找到图片URL数组")
                return [], chapter_name
        except Exception as e:
            print(f"解析图片URL异常: {e}")
            return [], "未知章节"
    
    def get_next_page_url(self, html):
        """从HTML中解析下一页URL
        
        Args:
            html: 页面HTML内容
            
        Returns:
            下一页URL，如果没有下一页则返回None
        """
        try:
            # 查找下一章链接
            next_page_match = re.search(r'<a\s+href="\./plugin\.php\?id=jameson_manhua&amp;a=read&amp;zjid=([0-9]+)&amp;kuid=[0-9]+"\s+class="uk-button">\s*下一章', html)
            if next_page_match:
                next_zjid = next_page_match.group(1)
                next_url = f"{self.domain}/plugin.php?id=jameson_manhua&a=read&zjid={next_zjid}&kuid=162365"
                return next_url
            else:
                # 尝试另一种下一章链接格式
                next_page_match = re.search(r'<a\s+href="\./plugin\.php\?id=jameson_manhua&amp;a=read&amp;zjid=([0-9]+)&amp;kuid=([0-9]+)"\s+class="uk-button">\s*下一章', html)
                if next_page_match:
                    next_zjid = next_page_match.group(1)
                    next_kuid = next_page_match.group(2)
                    next_url = f"{self.domain}/plugin.php?id=jameson_manhua&a=read&zjid={next_zjid}&kuid={next_kuid}"
                    return next_url
                
                # 检查JavaScript中的下一页链接
                next_js_match = re.search(r'if\(next\)\{\s*location\.href = \'\./plugin\.php\?id=jameson_manhua&a=read&zjid=\'\+next', html)
                if next_js_match:
                    # 尝试找到next变量的值
                    next_var_match = re.search(r'var next\s*=\s*["\']?([0-9]+)["\']?', html)
                    if next_var_match:
                        next_zjid = next_var_match.group(1)
                        next_url = f"{self.domain}/plugin.php?id=jameson_manhua&a=read&zjid={next_zjid}&kuid=162365"
                        return next_url
                
                print("未找到下一页链接")
                return None
        except Exception as e:
            print(f"解析下一页URL异常: {e}")
            return None
    
    def download_image(self, url, save_path):
        """下载图片
        
        Args:
            url: 图片URL
            save_path: 保存路径
            
        Returns:
            是否下载成功
        """
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"下载图片失败，状态码: {response.status_code}, URL: {url}")
                return False
        except Exception as e:
            print(f"下载图片异常: {e}, URL: {url}")
            return False
    
    def crawl(self):
        """开始爬取漫画"""
        current_url = self.base_url
        page_count = 1
        
        while current_url:
            print(f"正在爬取第{page_count}页: {current_url}")
            html = self.get_html(current_url)
            
            if not html:
                print(f"获取页面内容失败: {current_url}")
                break
            
            image_urls, chapter_name = self.parse_image_urls(html)
            
            if not image_urls:
                print(f"未找到图片: {current_url}")
                break
            
            # 创建章节目录
            chapter_dir = os.path.join(self.save_dir, chapter_name)
            if not os.path.exists(chapter_dir):
                os.makedirs(chapter_dir)
            
            # 下载图片
            for i, img_url in enumerate(image_urls):
                # 提取文件名或使用索引作为文件名
                file_name = os.path.basename(img_url).split('.')[0] + '.jpg'
                save_path = os.path.join(chapter_dir, f"{i+1:03d}_{file_name}")
                
                if not os.path.exists(save_path):
                    print(f"下载图片 {i+1}/{len(image_urls)}: {img_url}")
                    success = self.download_image(img_url, save_path)
                    if not success:
                        print(f"下载图片失败: {img_url}")
                    # 添加延迟，避免请求过快
                    time.sleep(0.5)
                else:
                    print(f"图片已存在，跳过: {save_path}")
            
            # 获取下一页URL
            next_url = self.get_next_page_url(html)
            if next_url == current_url:
                print("检测到重复URL，停止爬取")
                break
            
            current_url = next_url
            page_count += 1
            # 添加页面间延迟，避免请求过快
            time.sleep(1)

def main():
    # 漫画首页URL
    # base_url = "https://www.antbyw.com/plugin.php?id=jameson_manhua&a=read&zjid=1105076&kuid=162365"
    # 番外篇URL
    base_url = "https://www.antbyw.com/plugin.php?id=jameson_manhua&a=read&kuid=162365&zjid=1105053"

    # 保存目录
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "白鹤三绝——番外篇")
    
    spider = ComicsSpider(base_url, save_dir)
    spider.crawl()

if __name__ == "__main__":
    main()