#!/usr/bin/env python3
import requests
import os
import shutil
from PIL import Image
import sys

def download_images(base_url, total_pages, temp_dir="temp_images"):
    """
    第一步：批量下载图片
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # 修改为 Linux 下的 User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    print(f"[*] 开始下载，共 {total_pages} 页...")

    for i in range(1, total_pages + 1):
        url = f"{base_url}{i}.png"
        save_path = os.path.join(temp_dir, f"{i}.png")

        if os.path.exists(save_path):
            continue

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                # 使用 \r 实现单行刷新进度，Linux 终端常用
                sys.stdout.write(f"\r[*] 进度: [{i}/{total_pages}] 下载成功")
                sys.stdout.flush()
            else:
                print(f"\n[!] 第 {i} 页下载失败 (状态码: {response.status_code})")
        except Exception as e:
            print(f"\n[!] 第 {i} 页出错: {e}")
    print("\n[*] 下载完成。")

def images_to_pdf(temp_dir, output_pdf_name):
    """
    第二步：将图片合并为PDF
    """
    print("[*] 开始处理图片并转换 PDF...")
    
    image_files = []
    if not os.path.exists(temp_dir):
        print("[!] 目录不存在，无法转换")
        return

    for file in os.listdir(temp_dir):
        if file.endswith(".png"):
            image_files.append(file)
    
    # 排序
    image_files.sort(key=lambda x: int(x.split('.')[0]))

    if not image_files:
        print("[!] 没有找到图片，无法生成 PDF")
        return

    sources = []
    img_objects = [] 

    try:
        # 打开第一张图片
        first_img_path = os.path.join(temp_dir, image_files[0])
        first_img = Image.open(first_img_path)
        
        if first_img.mode == "RGBA":
            first_img = first_img.convert("RGB")
        
        img_objects.append(first_img)

        # 处理剩余图片
        for file in image_files[1:]:
            path = os.path.join(temp_dir, file)
            img = Image.open(path)
            if img.mode == "RGBA":
                img = img.convert("RGB")
            sources.append(img)
            img_objects.append(img)

        # 补全 .pdf 后缀
        if not output_pdf_name.endswith(".pdf"):
            output_pdf_name += ".pdf"

        print(f"[*] 正在写入 PDF 文件: {output_pdf_name} (这可能需要几秒钟)...")
        first_img.save(
            output_pdf_name, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=sources
        )
        print(f"[+] 转换成功！文件保存在当前目录下。")
        
    except Exception as e:
        print(f"[!] PDF 生成失败: {e}")
    finally:
        # 关闭文件句柄
        for img in img_objects:
            try:
                img.close()
            except:
                pass

if __name__ == "__main__":
    # 检查输入参数，如果没有通过管道或参数传入，则交互式输入
    try:
        base_url_input = input("请输入图片基础URL (例如以 / 结尾): ").strip()
        # 处理可能意外粘贴进去的引号
        base_url_input = base_url_input.replace("'", "").replace('"', "")
        
        total_pages_input = int(input("请输入总页数: "))
        pdf_name_input = input("请输入保存的文件名: ").strip()
        
        temp_folder = "temp_download_images_linux"
        
        # 1. 下载
        download_images(base_url_input, total_pages_input, temp_folder)
        
        # 2. 合并
        images_to_pdf(temp_folder, pdf_name_input)
        
        # 3. 清理
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
            print(f"[*] 临时文件夹已清理。")
            
    except KeyboardInterrupt:
        print("\n[!] 用户中断操作。")
        if os.path.exists("temp_download_images_linux"):
            shutil.rmtree("temp_download_images_linux")
        sys.exit(0)
    except ValueError:
        print("\n[!] 输入错误，页数必须是数字。")