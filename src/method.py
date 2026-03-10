# 方法管理模块
import os
import yaml

def list_pending_methods():
    """罗列所有待处理方法及其关联的流程"""
    pending_methods = []
    method_names = set()
    
    # 扫描所有需求目录，查找待处理方法相关的用户故事
    requirement_dir = "c:/Users/fly_d/IdeaProjects/t-pm/需求"
    
    for root, _, files in os.walk(requirement_dir):
        for file in files:
            if file.endswith('.yaml') and '用户故事' in root:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    # 检查是否是待处理方法相关的用户故事
                    if '名称' in data and '待处理方法' in data['名称'] and data['名称'] not in method_names:
                        method_names.add(data['名称'])
                        # 处理流程，确保它是一个列表
                        process = data.get('流程', [])
                        if isinstance(process, str):
                            # 如果流程是字符串，按行分割
                            process = []
                            # 直接读取文件内容，逐行处理
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            in_process = False
                            for line in lines:
                                stripped_line = line.strip()
                                if stripped_line == '流程:':
                                    in_process = True
                                elif in_process and stripped_line and not stripped_line.startswith('-') and not stripped_line.startswith('结果:'):
                                    # 处理流程行
                                    if stripped_line[0].isdigit() and '.' in stripped_line:
                                        # 提取数字后的内容
                                        parts = stripped_line.split('.', 1)
                                        if len(parts) > 1:
                                            process.append(parts[1].strip())
                                    else:
                                        process.append(stripped_line)
                                elif in_process and (stripped_line.startswith('结果:') or stripped_line == ''):
                                    in_process = False
                        elif isinstance(process, list):
                            # 如果流程是列表，确保每个元素都是字符串
                            process = [str(item).strip() for item in process if str(item).strip()]
                        
                        method_info = {
                            '名称': data.get('名称', ''),
                            '说明': data.get('说明', ''),
                            '流程': process
                        }
                        pending_methods.append(method_info)
                except Exception as e:
                    print(f"✗ {file_path} - 读取失败: {e}")
    
    return pending_methods

def create_method(name, description, process):
    """创建新的方法"""
    # 方法文件存储在模块的方法目录中
    method_dir = "c:/Users/fly_d/IdeaProjects/t-pm/模块/方法管理/方法"
    file_name = f"{name}.yaml"
    file_path = os.path.join(method_dir, file_name)
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"✗ 方法文件已存在: {file_path}")
        return False
    
    # 构建方法数据
    method_data = {
        '名称': name,
        '说明': description,
        '流程': process
    }
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(method_data, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 方法创建成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 方法创建失败: {e}")
        return False

def edit_method(name, updates):
    """编辑现有方法"""
    method_dir = "c:/Users/fly_d/IdeaProjects/t-pm/模块/方法管理/方法"
    file_name = f"{name}.yaml"
    file_path = os.path.join(method_dir, file_name)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"✗ 方法文件不存在: {file_path}")
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
        print(f"✓ 方法编辑成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 方法编辑失败: {e}")
        return False

def apply_method(method_name, target_context):
    """应用方法到特定上下文"""
    method_dir = "c:/Users/fly_d/IdeaProjects/t-pm/模块/方法管理/方法"
    file_name = f"{method_name}.yaml"
    file_path = os.path.join(method_dir, file_name)
    
    # 检查方法文件是否存在
    if not os.path.exists(file_path):
        print(f"✗ 方法文件不存在: {file_path}")
        return False
    
    # 读取方法数据
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            method_data = yaml.safe_load(f)
        
        print(f"\n应用方法: {method_data.get('名称', '未知')}")
        print(f"说明: {method_data.get('说明', '无')}")
        print(f"应用到: {target_context}")
        print("\n执行流程:")
        
        process = method_data.get('流程', [])
        if isinstance(process, list):
            for i, step in enumerate(process, 1):
                print(f"{i}. {step}")
        else:
            print("流程格式不正确")
            return False
        
        print("\n方法应用完成！")
        return True
    except Exception as e:
        print(f"✗ 方法应用失败: {e}")
        return False

def list_methods():
    """列出所有方法"""
    method_dir = "c:/Users/fly_d/IdeaProjects/t-pm/模块/方法管理/方法"
    methods = []
    
    if not os.path.exists(method_dir):
        print(f"✗ 方法目录不存在: {method_dir}")
        return []
    
    for file in os.listdir(method_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(method_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                methods.append({
                    '名称': data.get('名称', '未知'),
                    '文件': file
                })
            except Exception as e:
                print(f"✗ 读取方法文件失败: {file_path} - {e}")
    
    if methods:
        print("\n所有方法:")
        for i, method in enumerate(methods, 1):
            print(f"{i}. {method['名称']} ({method['文件']})")
    else:
        print("\n没有找到方法文件")
    
    return methods

def check_method_data():
    """检查方法管理数据的合理性"""
    method_dir = "c:/Users/fly_d/IdeaProjects/t-pm/模块/方法管理/方法"
    valid = True
    success = []
    failure = []
    
    if not os.path.exists(method_dir):
        failure.append(f"方法目录不存在: {method_dir}")
        return False, success, failure
    
    # 检查方法目录下的所有yaml文件
    for file in os.listdir(method_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(method_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # 检查必要字段
                if '名称' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 名称")
                    failure.append("  修复建议: 添加 '名称' 字段，例如: 名称: 方法名称")
                    valid = False
                if '说明' not in data:
                    failure.append(f"{file_path} - 缺少字段: 说明")
                    failure.append("  修复建议: 添加 '说明' 字段，描述方法的功能")
                if '流程' not in data:
                    failure.append(f"{file_path} - 缺少字段: 流程")
                    failure.append("  修复建议: 添加 '流程' 字段，描述方法的执行步骤")
                
                success.append(f"{file_path} - 检查通过")
            except yaml.YAMLError as e:
                failure.append(f"{file_path} - YAML格式错误: {e}")
                failure.append("  修复建议: 检查YAML格式是否正确，确保缩进和语法正确")
                valid = False
            except Exception as e:
                failure.append(f"{file_path} - 检查失败: {e}")
                failure.append("  修复建议: 检查文件是否存在，权限是否正确")
                valid = False
    
    return valid, success, failure

