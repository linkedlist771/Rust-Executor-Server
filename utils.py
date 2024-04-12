import subprocess
import time
import tempfile
import os
from config import RUST_PROJECTS_SAVE_PATH, ROOT_DIR


if not os.path.exists(RUST_PROJECTS_SAVE_PATH):
    os.makedirs(RUST_PROJECTS_SAVE_PATH)

def create_and_run_rust_project(code: str) -> tuple[str, bool]:
    os.chdir(ROOT_DIR)
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.rs') as temp_file:
        # 将 Rust 代码写入临时文件
        temp_file.write(code.encode())
        temp_file_path = temp_file.name
    
    compile_error = False
    # 获取项目名称（时间戳）
    project_name = f'rust_project_{int(time.time())}'
    os.chdir(RUST_PROJECTS_SAVE_PATH)

    # 构建 cargo new 命令并执行
    subprocess.run(['cargo', 'new', project_name], check=True)

    # 将 Rust 代码从临时文件复制到新创建的项目中
    with open(f'{project_name}/src/main.rs', 'w') as main_rs:
        with open(temp_file_path, 'r') as code_file:
            main_rs.write(code_file.read())

    # 进入项目目录
    os.chdir(project_name)
    try:
        # 编译并运行项目，捕获输出
        result = subprocess.run(['cargo', 'run'], capture_output=True, text=True, check=True)
        output = result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        # 处理命令失败的情况
        output = e.stdout + e.stderr
        compile_error = True

    # 清理：删除临时文件
    os.remove(temp_file_path)

    # 打印并返回结果
    return output, compile_error

if __name__ == '__main__':
    rust_code = """// From is now included in `std::prelude`, so there is no need to introduce it into the current scope
    // use std::convert::From;

    #[derive(Debug)]
    struct Number {
        value: i32,
    }

    impl From<i32> for Number {
        // IMPLEMENT `from` method
        fn from (item: i32) -> Self {
            Number { value: item }
        }
        
    }

    // FILL in the blanks
    fn main() {
        let num = Number{value: 30};
        assert_eq!(num.value, 30);

        let num: Number = 30.into();
        assert_eq!(num.value, 30);

        println!("Success!");
    }
    """
    output = create_and_run_rust_project(rust_code)
    print("Received Output:\n", output)
