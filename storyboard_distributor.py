import re

class StoryboardDistributor:
    """
    一个自动将分镜内容分配给1-9个分镜节点的组件。
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """定义节点的输入类型。"""
        return {
            "required": {
                "storyboard_text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "scene_prefix": ("STRING", {"default": "[SCENE-"}),
                "scene_suffix": ("STRING", {"default": "]"}),
                "add_preface_to_all": ("BOOLEAN", {"default": True}),
                "debug_mode": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("frame1", "frame2", "frame3", "frame4", "frame5", "frame6", "frame7", "frame8", "frame9")
    FUNCTION = "distribute_scenes"
    CATEGORY = "storyboard"

    def distribute_scenes(self, storyboard_text, scene_prefix="[SCENE-", scene_suffix="]", add_preface_to_all=True, debug_mode=False):
        """
        将分镜文本中的场景分配到9个分镜帧中。
        每个场景应该使用[SCENE-N]格式标记，其中N是1到9之间的数字。
        """
        # 初始化所有帧为空字符串
        frames = [""] * 9

        # 如果分镜文本为空，返回空帧
        if not storyboard_text or storyboard_text.strip() == "":
            if debug_mode:
                print("警告：分镜文本为空。")
            return tuple(frames)

        # 通过场景标记分割文本
        pattern = re.escape(scene_prefix) + r'(\d+)' + re.escape(scene_suffix)
        
        # 查找文本中的所有场景标记
        scene_markers = re.findall(pattern, storyboard_text)
        
        if debug_mode:
            print(f"找到 {len(scene_markers)} 个场景标记: {scene_markers}")
        
        # 如果没有找到场景标记，将整个文本视为前言
        if not scene_markers:
            if debug_mode:
                print("未找到场景标记。将整个文本视为前言。")
            preface = storyboard_text.strip()
            if add_preface_to_all and preface:
                frames = [preface] * 9
            return tuple(frames)
        
        # 通过场景标记分割文本
        scenes = re.split(pattern, storyboard_text)
        
        # 第一个元素是第一个场景标记之前的任何文本
        preface = scenes[0].strip()
        
        if debug_mode:
            print(f"前言: {preface[:50]}..." if len(preface) > 50 else f"前言: {preface}")
            print(f"找到 {(len(scenes) - 1) // 2} 个场景需要处理")
        
        # 处理每个场景
        for i in range(1, len(scenes), 2):
            # 检查是否同时有场景编号和内容
            if i < len(scenes) and i+1 < len(scenes):
                try:
                    scene_num = int(scenes[i])
                    scene_content = scenes[i+1].strip()
                    
                    # 只处理1-9之间的场景
                    if 1 <= scene_num <= 9:
                        # 将场景标记添加回内容
                        full_content = f"{scene_prefix}{scene_num}{scene_suffix} {scene_content}"
                        frames[scene_num-1] = full_content
                        
                        if debug_mode:
                            print(f"添加场景 {scene_num} 内容: {scene_content[:30]}...")
                    else:
                        if debug_mode:
                            print(f"场景编号 {scene_num} 超出范围(1-9)，跳过")
                except ValueError:
                    if debug_mode:
                        print(f"无效的场景编号: {scenes[i]}")
        
        # 如果需要将前言添加到所有帧
        if add_preface_to_all and preface:
            for i in range(9):
                if frames[i]:
                    frames[i] = f"{preface}\n{frames[i]}"
                else:
                    frames[i] = preface

        if debug_mode:
            print(f"最终包含内容的帧数: {sum(1 for f in frames if f)}")
        
        return tuple(frames)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "StoryboardDistributor": StoryboardDistributor,
}

# 节点显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryboardDistributor": "分镜分配器 (Storyboard Distributor)",
} 