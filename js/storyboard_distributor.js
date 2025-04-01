import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI.StoryboardDistributor",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 只修改我们自己的节点类型
        if (nodeData.name !== "StoryboardDistributor") {
            return;
        }

        // 自定义节点外观
        nodeType.category = "storyboard";
        nodeType.color = "#c1facf"; // 浅绿色背景
        nodeType.bgcolor = "#ade6bb"; // 深绿色标题栏
        
        // 默认为节点创建更大的尺寸
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
            
            // 设置最小默认尺寸
            this.size = [400, 280]; 
            
            // 添加自定义标题
            this.title = "分镜分配器 (Storyboard Distributor)";
            
            return r;
        };

        // 重写原始的绘制函数
        const origDraw = nodeType.prototype.draw;
        nodeType.prototype.draw = function (ctx) {
            // 首先调用原始绘制方法
            origDraw.apply(this, arguments);

            // 在节点渲染后添加自定义绘制内容
            if (this.flags.collapsed) return;

            // 获取节点尺寸
            const nodeWidth = this.size[0];
            const nodeHeight = this.size[1];
            
            // 在底部绘制一个小信息标签
            ctx.fillStyle = "rgba(0,0,0,0.5)";
            ctx.font = "12px Arial";
            ctx.fillText("分镜1-9自动分配 ● 标记: [SCENE-1] 到 [SCENE-9]", 10, nodeHeight - 8);
            
            // 绘制一个小图标或图形
            ctx.fillStyle = "#3d7e4a";
            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                for (let j = 0; j < 3; j++) {
                    ctx.roundRect(nodeWidth - 80 + (i * 22), 45 + (j * 22), 18, 18, 3);
                }
            }
            ctx.fill();
            
            // 绘制连接框架的线条
            ctx.strokeStyle = "#3d7e4a";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            
            // 水平线
            for (let j = 1; j < 3; j++) {
                ctx.moveTo(nodeWidth - 80, 55 + (j * 22));
                ctx.lineTo(nodeWidth - 22, 55 + (j * 22));
            }
            
            // 垂直线
            for (let i = 1; i < 3; i++) {
                ctx.moveTo(nodeWidth - 80 + (i * 22), 45);
                ctx.lineTo(nodeWidth - 80 + (i * 22), 89);
            }
            
            ctx.stroke();
        };

        // 重写getExtraMenuOptions以添加自定义菜单项
        const getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
        nodeType.prototype.getExtraMenuOptions = function (_, options) {
            if (getExtraMenuOptions) {
                getExtraMenuOptions.apply(this, arguments);
            }

            // 添加帮助菜单选项
            options.push({
                content: "帮助",
                callback: () => {
                    alert(
                        "分镜分配器使用说明:\n\n" +
                        "● 功能说明:\n" +
                        "  将包含多个场景的文本自动分配到9个输出节点\n\n" +
                        "● 使用方法:\n" +
                        "  1. 将分镜文本输入到storyboard_text字段\n" +
                        "  2. 确保每个场景标记为 [SCENE-X] 格式，其中X是1到9之间的数字\n" +
                        "  3. 节点会自动将内容分配到对应的9个输出\n\n" +
                        "● 例如:\n" +
                        "  [SCENE-1] 第一个场景描述...\n" +
                        "  [SCENE-2] 第二个场景描述...\n" +
                        "  [SCENE-3] 第三个场景描述..."
                    );
                },
            });
            
            // 添加示例分镜文本
            options.push({
                content: "插入示例文本",
                callback: () => {
                    // 查找storyboard_text控件
                    if (this.widgets && this.widgets.length > 0) {
                        const textWidget = this.widgets.find(w => w.name === "storyboard_text");
                        if (textWidget) {
                            textWidget.value = 
                            "角色：小星（6岁女孩）\n" +
                            "风格：红色圆点蝴蝶结发夹 + 浅蓝色围裙 + 黄色雨靴\n\n" +
                            "[SCENE-1] 魔法森林在早晨被灰雾笼罩。\n" +
                            "角色动作：小星蹲在森林入口处，拾起一块发光的碎片。\n\n" +
                            "[SCENE-2] 穿过荆棘丛，遇见"迷雾迷宫树"。\n" +
                            "动作：小星用布袋里的剪刀开路，同伴记录路线。\n\n" +
                            "[SCENE-3] 宝石归来，森林恢复色彩，阳光穿透树叶。\n" +
                            "动作：小星开心鼓掌，蝴蝶结被风吹动，雨靴上布满彩虹露珠。";
                            textWidget.callback(textWidget.value);
                        }
                    }
                },
            });
        };
    },
}); 