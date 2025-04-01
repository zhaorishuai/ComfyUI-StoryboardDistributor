#!/usr/bin/env python3

from storyboard_distributor import StoryboardDistributor

# 创建测试实例
distributor = StoryboardDistributor()

# 定义一个包含多个场景的测试分镜文本
test_text = """
Star (6 year old girl)
Style: red dot bow hair clip + light blue bib + yellow rain boots.

[SCENE-1] Picture: The magic forest in the morning is shrouded in gray fog.
Character action: Starlet crouches at the entrance of the forest.

[SCENE-2] Scene: Through the thorn bushes, encounter the "fog maze tree".
Action: Starlet opens the way with scissors in a cloth bag.

[SCENE-3] Scene: Gem returns, forest returns color, sunlight penetrates leaves.
Action: Little star claps with purr, bow is blown by wind.

[SCENE-5] Scene: Through the thorn bushes, encounter the "fog maze tree".
Action: Starlet opens the way with scissors in a cloth bag.

[SCENE-9] Final scene: Credits and acknowledgments.
"""

# 启用调试模式处理文本
frames = distributor.distribute_scenes(test_text, debug_mode=True)

# 显示结果
print("\n测试结果:")
print("=" * 80)

for i, frame in enumerate(frames):
    print(f"分镜 {i+1}:")
    print("-" * 40)
    if frame:
        print(frame)
    else:
        print("<空>")
    print()

# 测试边缘情况
print("\n测试边缘情况:")
print("=" * 80)

# 空文本
print("\n1. 空文本:")
frames = distributor.distribute_scenes("", debug_mode=True)
print("结果:", ["<空>" if not f else "有内容" for f in frames])

# 没有场景标记的文本
print("\n2. 没有场景标记:")
frames = distributor.distribute_scenes("这只是一段没有场景标记的前言文本。", debug_mode=True)
print("结果:", ["<空>" if not f else "有内容" for f in frames])

# 无效的场景编号
print("\n3. 无效的场景编号:")
frames = distributor.distribute_scenes("[SCENE-0] 无效场景\n[SCENE-10] 另一个无效场景", debug_mode=True)
print("结果:", ["<空>" if not f else "有内容" for f in frames])

# 不添加前言
print("\n4. 不添加前言:")
frames = distributor.distribute_scenes(test_text, add_preface_to_all=False, debug_mode=True)
print("结果:", ["<空>" if not f else "有内容" for f in frames])

print("\n测试完成。") 