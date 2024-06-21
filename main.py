import os
import subprocess


def generate_summary(root_dir: str, exclude_dirs: list[str], include_extensions: list[str], output_file: str,
                     output_dir: str, target_files: list[str]):
    """
    指定されたディレクトリ内のファイルをマークダウン形式で出力する。

    Args:
        root_dir: ルートディレクトリ
        exclude_dirs: 除外するディレクトリリスト
        include_extensions: 含めるファイル拡張子リスト
        output_file: 出力ファイル名
        output_dir: 出力フォルダ
        target_files: 取得対象のファイル名リスト
    """
    # ディレクトリ構造を tree コマンドで取得
    tree_output = subprocess.check_output(
        ["tree", "-N", "-I", "__pycache__|*.pyc", root_dir], encoding='utf-8')

    # ファイル情報を取得
    file_paths = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # 除外ディレクトリのチェック
            if any(dir in root for dir in exclude_dirs):
                continue

            # .pycファイルの除外
            if file.endswith(".pyc"):
                continue

            # 拡張子のチェック
            if any(file.endswith(ext) for ext in include_extensions):
                file_paths.append(file_path)
                continue

            # ターゲットファイルのチェック
            if file in target_files:
                file_paths.append(file_path)

    # マークダウン形式で出力
    output_content = f"""
## ディレクトリ構造

{tree_output}

## ファイル一覧

"""

    for file_path in file_paths:
        # ファイルを開いて中身を取得
        with open(file_path, 'r') as f:
            try:
                file_content = f.read()
            except UnicodeDecodeError:
                print(f"UnicodeDecodeError: {file_path}")
                continue

        output_content += f"""
```{file_path.replace(root_dir, "")}
{file_content.replace("```", "``````")}
```
"""
    # ファイル出力
    with open(os.path.join(output_dir, output_file), 'w') as f:
        f.write(output_content)


if __name__ == "__main__":
    root_dir = "~/project/noricha/Summarizer"  # ルートディレクトリを指定
    exclude_dirs = ["venv", ".git"]  # 除外するディレクトリ
    include_extensions = [".md", ".yaml", ".yml",
                          ".txt", ".py", ".html"]  # 含めるファイル拡張子
    output_file = "summary.md"
    output_dir = "/Users/main/Desktop"  # 出力フォルダを指定
    target_files = ["README.md", "requirements.txt",
                    "config.yaml", "Dockerfile"]  # 取得対象のファイル名を指定
    generate_summary(root_dir, exclude_dirs, include_extensions,
                     output_file, output_dir, target_files)
    print("Summary generated successfully!")
