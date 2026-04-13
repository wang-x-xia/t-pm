# 流程管理模块
import os
import logging
import yaml
from src.paths import get_process_dir

logger = logging.getLogger(__name__)

def check_process_data():
    """检查流程管理数据的合理性"""
    from src.paths import get_background_dir
    process_dir = get_process_dir()
    background_dir = get_background_dir()
    valid = True
    success = []
    failure = []
    
    # 收集所有已有背景名称，用于交叉验证
    all_backgrounds = set()
    if os.path.exists(background_dir):
        for f in os.listdir(background_dir):
            if f.endswith('.yaml'):
                all_backgrounds.add(f.replace('.yaml', ''))
    
    required_fields = ['名称', '背景', '输入', '方法', '结果']
    
    # 检查流程目录下的所有yaml文件
    for file in os.listdir(process_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(process_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                file_valid = True
                
                # 检查必要字段
                for field in required_fields:
                    if field not in data:
                        failure.append(f"{file_path} - 缺少必要字段: {field}")
                        valid = False
                        file_valid = False
                
                # 检查名称与文件名一致
                expected_name = file.replace('.yaml', '')
                if data.get('名称') != expected_name:
                    failure.append(f"{file_path} - 名称 '{data.get('名称')}' 与文件名 '{expected_name}' 不一致")
                    valid = False
                    file_valid = False
                
                # 检查背景引用是否存在
                if '背景' in data and data['背景']:
                    bg = data['背景']
                    # 背景可能是字符串或引用名称
                    if isinstance(bg, str) and bg in all_backgrounds:
                        pass  # 引用有效
                    elif isinstance(bg, str):
                        logger.warning(f"{file_path} - 背景 '{bg}' 未找到对应的背景文件（可能是内联描述）")
                
                # 检查方法字段是列表
                if '方法' in data:
                    if not isinstance(data['方法'], list):
                        failure.append(f"{file_path} - 方法字段应该是列表")
                        valid = False
                        file_valid = False
                
                if file_valid:
                    success.append(f"{file_path} - 检查通过")
            except Exception as e:
                failure.append(f"{file_path} - 检查失败: {e}")
                valid = False
    
    return valid, success, failure

def create_process(name, background, inputs, method, result):
    """创建新的流程"""
    process_dir = get_process_dir()
    file_name = f"{name}.yaml"
    file_path = os.path.join(process_dir, file_name)
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"✗ 流程文件已存在: {file_path}")
        return False
    
    # 构建流程数据
    process_data = {
        '名称': name,
        '背景': background,
        '输入': inputs,
        '方法': method,
        '结果': result
    }
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(process_data, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 流程创建成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 流程创建失败: {e}")
        return False

def edit_process(name, updates):
    """编辑现有流程"""
    process_dir = get_process_dir()
    file_name = f"{name}.yaml"
    file_path = os.path.join(process_dir, file_name)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"✗ 流程文件不存在: {file_path}")
        return False
    
    # 读取现有数据
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 更新数据
        data.update(updates)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 流程编辑成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 流程编辑失败: {e}")
        return False

def visualize_process(name):
    """可视化展示流程"""
    process_dir = get_process_dir()
    file_name = f"{name}.yaml"
    file_path = os.path.join(process_dir, file_name)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"✗ 流程文件不存在: {file_path}")
        return False
    
    # 读取流程数据
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 可视化展示
        print(f"\n流程: {data.get('名称', '未知')}")
        print(f"背景: {data.get('背景', '无')}")
        print(f"输入: {data.get('输入', '无')}")
        print(f"方法: {data.get('方法', '无')}")
        print(f"结果: {data.get('结果', '无')}")
        print("\n流程可视化:")
        print("┌────────────────────────────────────────┐")
        print(f"│ 流程: {data.get('名称', '未知'):^40} │")
        print("├────────────────────────────────────────┤")
        print(f"│ 背景: {data.get('背景', '无'):^40} │")
        print("├────────────────────────────────────────┤")
        print(f"│ 输入: {data.get('输入', '无'):^40} │")
        print("├────────────────────────────────────────┤")
        print(f"│ 方法: {data.get('方法', '无'):^40} │")
        print("├────────────────────────────────────────┤")
        print(f"│ 结果: {data.get('结果', '无'):^40} │")
        print("└────────────────────────────────────────┘")
        return True
    except Exception as e:
        print(f"✗ 流程可视化失败: {e}")
        return False

def list_processes():
    """列出所有流程"""
    process_dir = get_process_dir()
    processes = []
    
    for file in os.listdir(process_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(process_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                processes.append({
                    '名称': data.get('名称', '未知'),
                    '文件': file
                })
            except Exception as e:
                print(f"✗ 读取流程文件失败: {file_path} - {e}")
    
    if processes:
        print("\n所有流程:")
        for i, process in enumerate(processes, 1):
            print(f"{i}. {process['名称']} ({process['文件']})")
    else:
        print("\n没有找到流程文件")
    
    return processes

