import json
import os
import shutil

def copy_images_from_json_direct(json_file_path, base_source_dir, output_dir="YouCook2/image_path"):
    """
    读取JSON文件中的 'image_path'，并直接将图片从原始本地位置复制到指定的目标目录。

    参数：
        json_file_path (str): 包含图片路径的JSON文件的路径。
        base_source_dir (str): 图片原始存放的根目录（例如：'./my_original_images/'）。
                               JSON中的路径会与此目录拼接。
        output_dir (str): 图片将被复制到的目标目录，默认为 'YouCook2/image_path'。
    """
    # 确保目标目录存在，如果不存在则创建
    os.makedirs(output_dir, exist_ok=True)
    print(f"确保目标目录存在: {output_dir}")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 如果JSON是单个字典，将其放入列表中以便统一处理
        if not isinstance(data, list):
            data = [data]

        copied_count = 0
        skipped_count = 0
        
        for item in data:
            # 仅处理 'image_path' 中的路径
            if 'image_path' in item and isinstance(item['image_path'], list):
                for path in item['image_path']:
                    full_source_path = os.path.join(base_source_dir, path)
                    
                    # 构建目标文件路径，保持原始的子目录结构
                    # 例如：如果 full_source_path 是 'my_original_images/01lB162koHA/frame_00000.jpg'
                    # 那么 relative_path_in_json 是 '01lB162koHA/frame_00000.jpg'
                    relative_path_in_json = os.path.relpath(full_source_path, base_source_dir)
                    
                    # 构建目标子目录，例如 'YouCook2/image_path/01lB162koHA/'
                    dest_sub_dir = os.path.join(output_dir, os.path.dirname(relative_path_in_json))
                    
                    # 确保目标子目录存在
                    os.makedirs(dest_sub_dir, exist_ok=True)
                    
                    # 最终的目标文件路径
                    dest_file_path = os.path.join(dest_sub_dir, os.path.basename(full_source_path))

                    if not os.path.exists(full_source_path):
                        print(f"警告：源文件不存在，跳过：{full_source_path}")
                        skipped_count += 1
                        continue

                    if os.path.exists(dest_file_path):
                        print(f"目标文件已存在，跳过复制：{dest_file_path}")
                        copied_count += 1 # 依然算作已处理（无需再次复制）
                        continue

                    try:
                        print(f"正在复制：{full_source_path} 到 {dest_file_path}...")
                        shutil.copy2(full_source_path, dest_file_path) # copy2 会保留文件元数据
                        copied_count += 1
                        print(f"成功复制：{os.path.basename(full_source_path)}")

                    except Exception as e:
                        print(f"复制 {full_source_path} 到 {dest_file_path} 时出错：{e}")
            else:
                # 打印警告，如果某个条目缺少 'image_path' 或其格式不对
                print(f"警告：跳过一项，因为它缺少 'image_path' 键或其值不是列表：{item.get('id', '未知ID')}")

        print(f"\n处理完成。成功复制了 {copied_count} 个图片文件（包括已存在的），跳过了 {skipped_count} 个不存在的源文件。")

    except FileNotFoundError:
        print(f"错误：找不到JSON文件：{json_file_path}")
    except json.JSONDecodeError:
        print(f"错误：无法解析JSON文件内容。请检查文件格式。")
    except Exception as e:
        print(f"发生了一个意外错误：{e}")

json_file = 'youcook.json' # 替换为你的JSON文件名
    
# 替换为你的图片在本地的实际根目录！
# 例如，如果图片文件都放在一个名为 'original_images' 的文件夹中
base_images_source_directory = '../YouCook2/video_frames/' # 你的图片原始存放的根目录

# 你希望图片被复制到的目标目录
output_destination_directory = 'YouCook2/'

copy_images_from_json_direct(json_file, base_images_source_directory, output_destination_directory)
