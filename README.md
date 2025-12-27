# 超星/学习通 图片下载与PDF合成工具

这是一个 Python 脚本，用于从指定的 URL 批量下载图片并将其合并为 PDF 文件。

## 功能
- 自动遍历下载图片
- 显示下载进度条
- 自动将下载的图片合并为 PDF
- 完成后自动清理临时文件

## 使用方法

1. 安装依赖：
   ```bash
   pip install -r requirements.txt

2. 运行脚本：
   bash
   python download_images.py
   
3. 根据提示输入：
   图片的基础 URL（去掉最后数字.png的url地址）
   ppt总页数
   保存的 PDF 文件名
   
## 注意事项
   请勿用于侵犯版权的用途（本来就是期末老师没给开放下载权限自己写着玩的）
   
## 兼容性说明 (Compatibility)
   本项目已在 Linux (Ubuntu/CentOS) 环境下测试通过。
    - 由于使用了 Python 标准路径处理，理论上支持 Windows/macOS，但未经过充分测试。
    - 如果在 Windows 下遇到路径报错（比如 `\` 和 `/` 的问题），欢迎提交 Issue 或 PR。

## 环境要求
    - Python 3.x
    - 运行于拥有写入权限的目录（脚本会创建临时文件夹）
