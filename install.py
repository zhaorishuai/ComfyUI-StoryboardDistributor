#!/usr/bin/env python3

import os
import sys
import importlib.util
import platform

def check_environment():
    """检查环境是否具备所有必需的模块并且兼容。"""
    print("正在检查 ComfyUI-StoryboardDistributor 的环境...")
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("警告: 此插件已在 Python 3.8+ 上测试。使用较旧版本可能会遇到问题。")
    
    # 检查是否在 ComfyUI 文件夹中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    
    if not os.path.basename(parent_dir) == "custom_nodes":
        print("警告: 此插件未安装在 'custom_nodes' 目录中。")
        print(f"当前安装路径: {current_dir}")
    
    # 检查是否安装了 ComfyUI
    comfy_ui_installed = False
    comfy_paths = [
        os.path.join(grandparent_dir, "comfy"),
        os.path.join(grandparent_dir, "comfy_extras"),
    ]
    
    for path in comfy_paths:
        if os.path.exists(path):
            comfy_ui_installed = True
            break
    
    if comfy_ui_installed:
        print("已找到 ComfyUI 安装。")
    else:
        print("警告: 无法找到 ComfyUI 安装。")
    
    # 检查必需模块
    print("\n正在检查必需模块:")
    all_modules_available = True
    
    # 我们只使用标准库模块，所以不需要额外检查
    print("  re: 可用 (标准库)")
    
    return all_modules_available

def main():
    """运行安装检查的主函数。"""
    print(f"ComfyUI-StoryboardDistributor 安装检查")
    print(f"平台: {platform.system()} {platform.release()}")
    print("-" * 50)
    
    environment_ready = check_environment()
    
    print("\n安装状态:")
    if environment_ready:
        print("✅ 准备就绪！所有需求已满足。")
        print("\n现在您可以重启 ComfyUI 并使用 StoryboardDistributor 节点。")
        print("它将出现在节点菜单的 'storyboard' > '分镜分配器 (Storyboard Distributor)' 中")
    else:
        print("❌ 发现一些问题。请检查上面的警告。")
    
    print("\n要获取更多信息，请访问: https://github.com/yourusername/ComfyUI-StoryboardDistributor")

if __name__ == "__main__":
    main() 