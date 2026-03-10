# 流程管理模块
import os
import yaml

def check_process_data():
    """检查流程管理数据的合理性"""
    process_dir = "c:/Users/fly_d/IdeaProjects/t-pm/流程"
    valid = True
    success = []
    failure = []
    
    # 检查流程目录下的所有yaml文件
    for file in os.listdir(process_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(process_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # 检查必要字段
                if '名称' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 名称")
                    valid = False
                if '背景' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 背景")
                    valid = False
                if '输入' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 输入")
                    valid = False
                if '方法' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 方法")
                    valid = False
                if '结果' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 结果")
                    valid = False
                
                success.append(f"{file_path} - 检查通过")
            except Exception as e:
                failure.append(f"{file_path} - 检查失败: {e}")
                valid = False
    
    return valid, success, failure

def create_process(name, background, inputs, method, result):
    """创建新的流程"""
    process_dir = "c:/Users/fly_d/IdeaProjects/t-pm/流程"
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
    process_dir = "c:/Users/fly_d/IdeaProjects/t-pm/流程"
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
    process_dir = "c:/Users/fly_d/IdeaProjects/t-pm/流程"
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
    process_dir = "c:/Users/fly_d/IdeaProjects/t-pm/流程"
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

