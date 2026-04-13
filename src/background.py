# 背景管理模块
import os
import logging
import yaml
from src.paths import get_background_dir

logger = logging.getLogger(__name__)

def check_background_data():
    """检查背景管理数据的合理性"""
    background_dir = get_background_dir()
    valid = True
    success = []
    failure = []
    
    # 检查背景目录
    if not os.path.exists(background_dir):
        failure.append(f"背景目录不存在: {background_dir}")
        valid = False
        return valid, success, failure
    
    # 检查背景目录下的所有yaml文件
    for file_name in os.listdir(background_dir):
        if file_name.endswith('.yaml'):
            background_file = os.path.join(background_dir, file_name)
            try:
                with open(background_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                file_valid = True
                
                # 检查必要字段
                for field in ['名称', '说明']:
                    if field not in data:
                        failure.append(f"{background_file} - 缺少必要字段: {field}")
                        valid = False
                        file_valid = False
                
                # 检查名称与文件名一致
                expected_name = file_name.replace('.yaml', '')
                if data.get('名称') != expected_name:
                    failure.append(f"{background_file} - 名称 '{data.get('名称')}' 与文件名 '{expected_name}' 不一致")
                    valid = False
                    file_valid = False
                
                if file_valid:
                    success.append(f"{background_file} - 检查通过")
            except Exception as e:
                failure.append(f"{background_file} - 检查失败: {e}")
                valid = False
    
    return valid, success, failure

def create_background(name, description):
    """创建新的背景信息"""
    background_dir = get_background_dir()
    background_file = os.path.join(background_dir, f"{name}.yaml")
    
    # 检查背景是否已存在
    if os.path.exists(background_file):
        print(f"✗ 背景已存在: {name}")
        return False
    
    # 创建新背景文件
    new_background = {
        "名称": name,
        "说明": description
    }
    
    # 写回文件
    try:
        with open(background_file, 'w', encoding='utf-8') as f:
            yaml.dump(new_background, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 背景创建成功: {name}")
        return True
    except Exception as e:
        print(f"✗ 背景创建失败: {e}")
        return False

def edit_background(name, updates):
    """编辑现有背景信息"""
    background_dir = get_background_dir()
    background_file = os.path.join(background_dir, f"{name}.yaml")
    
    # 检查文件是否存在
    if not os.path.exists(background_file):
        print(f"✗ 背景文件不存在: {background_file}")
        return False
    
    # 读取现有数据
    try:
        with open(background_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 更新背景信息
        data.update(updates)
        
        # 写回文件
        with open(background_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 背景编辑成功: {name}")
        return True
    except Exception as e:
        print(f"✗ 背景编辑失败: {e}")
        return False

def display_background(name):
    """展示背景信息"""
    background_dir = get_background_dir()
    background_file = os.path.join(background_dir, f"{name}.yaml")
    
    # 检查文件是否存在
    if not os.path.exists(background_file):
        print(f"✗ 背景文件不存在: {background_file}")
        return False
    
    # 读取背景数据
    try:
        with open(background_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        print(f"\n背景: {data.get('名称', '未知')}")
        print(f"说明: {data.get('说明', '无')}")
        if '类别' in data:
            print(f"类别: {', '.join(data.get('类别', []))}")
        if '详情' in data:
            print(f"详情: {data.get('详情', '无')}")
        print("\n背景信息展示:")
        print("┌────────────────────────────────────────┐")
        print(f"│ 背景: {data.get('名称', '未知'):^40} │")
        print("├────────────────────────────────────────┤")
        print(f"│ 说明: {data.get('说明', '无'):^40} │")
        print("└────────────────────────────────────────┘")
        
        return True
    except Exception as e:
        print(f"✗ 背景展示失败: {e}")
        return False

def list_backgrounds():
    """列出所有背景信息"""
    background_dir = get_background_dir()
    backgrounds = []
    
    # 检查目录是否存在
    if not os.path.exists(background_dir):
        print(f"✗ 背景目录不存在: {background_dir}")
        return []
    
    # 读取背景目录下的所有yaml文件
    try:
        for file_name in os.listdir(background_dir):
            if file_name.endswith('.yaml'):
                background_file = os.path.join(background_dir, file_name)
                with open(background_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                backgrounds.append(data)
        
        if backgrounds:
            print("\n所有背景信息:")
            for i, background in enumerate(backgrounds, 1):
                print(f"{i}. {background.get('名称', '未知')}")
                print(f"   说明: {background.get('说明', '无')}")
        else:
            print("\n没有找到背景信息")
        
        return backgrounds
    except Exception as e:
        print(f"✗ 读取背景文件失败: {e}")
        return []

