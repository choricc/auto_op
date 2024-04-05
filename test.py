import concurrent.futures
import time
from gooey import Gooey, GooeyParser
import sys


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True,
       language='chinese')
def main():
    parser = GooeyParser(description="测试")
    parser.add_argument('--token', type=str, help='f12获取token')
    parser.add_argument('--pool', type=str, widget="Dropdown", choices=['江苏',
                                                                        '甘肃',
                                                                        '河北',
                                                                        '天津',
                                                                        '山西',
                                                                        '内蒙古',
                                                                        '广西',
    args = parser.parse_args(sys.argv[1:])

def task(n):
    print(f"开始任务 {n}")
    time.sleep(n)
    print(f"结束任务 {n}")
    return n

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(task, i): i for i in range(10)}

        for future in concurrent.futures.as_completed(futures):
        print(f"任务 {futures[future]} 完成，结果：{future.result()}")


if __name__ == "__main__":
    sys.exit(main())
