import csv
import os

class SchoolSelector:
    def __init__(self, filename='school.csv', on_select_callback=None):
        self.all_schools = []  # 存储所有学校
        self.filtered_schools = []  # 存储过滤后的学校
        self.on_select_callback = on_select_callback  # 选择学校的回调函数
        self.load_schools(filename)
        self.page_size = 10
        self.current_page = 1
        self.current_search = None  # 当前搜索词
    
    def load_schools(self, filename):
        if not os.path.exists(filename):
            print(f"错误：文件 {filename} 不存在")
            return
        
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:  # 确保每行至少有ID和名称
                    self.all_schools.append({
                        'id': row[0],
                        'name': row[1],
                        'code': row[2] if len(row) > 2 else ''
                    })
        self.filtered_schools = self.all_schools.copy()  # 初始时显示所有学校
    
    def display_page(self):
        total_pages = max(1, (len(self.filtered_schools) + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))
        
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.filtered_schools))
        
        print("\n" + "="*50)
        print(f"学校列表 (第 {self.current_page}/{total_pages} 页, 共 {len(self.filtered_schools)} 所)")
        if self.current_search:
            print(f"搜索词: {self.current_search}")
        print("="*50)
        
        for i in range(start_idx, end_idx):
            school = self.filtered_schools[i]
            print(f"{i+1}. [{school['id']}] {school['name']}")
        
        print("\n操作选项:")
        print("n: 下一页 | p: 上一页 | g <页码>: 跳转到页")
        print("s <关键词>: 搜索 | c: 清除搜索 | q: 退出")
        print("输入编号选择学校")
        print("="*50)
    
    def search_schools(self, search_term):
        self.current_search = search_term.lower()
        self.filtered_schools = [s for s in self.all_schools 
                               if self.current_search in s['name'].lower() 
                               or self.current_search in s['id'].lower()]
        self.current_page = 1
    
    def clear_search(self):
        self.current_search = None
        self.filtered_schools = self.all_schools.copy()
        self.current_page = 1
    
    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_page()
            
            user_input = input("请输入操作或选择学校编号: ").strip().lower()
            
            if not user_input:
                continue
            
            if user_input == 'q':
                print("再见！")
                break
            elif user_input == 'n':
                self.current_page += 1
            elif user_input == 'p':
                self.current_page = max(1, self.current_page - 1)
            elif user_input == 'c':
                self.clear_search()
            elif user_input.startswith('g '):
                try:
                    page = int(user_input[2:])
                    self.current_page = max(1, page)
                except ValueError:
                    print("无效的页码")
                    input("\n按回车键继续...")
            elif user_input.startswith('s '):
                search_term = user_input[2:]
                if search_term:
                    self.search_schools(search_term)
                else:
                    self.clear_search()
            else:
                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(self.filtered_schools):
                        selected = self.filtered_schools[choice-1]
                        print(f"\n您选择了: [{selected['id']}] {selected['name']}")
                        print(f"学校代码: {selected['code']}")
                        
                        # 如果有回调函数，则调用它
                        if self.on_select_callback:
                            self.on_select_callback(selected['id'], selected['name'], selected['code'])
                            
                        input("\n按回车键继续...")
                    else:
                        print("编号超出范围")
                        input("\n按回车键继续...")
                except ValueError:
                    print("无效输入")
                    input("\n按回车键继续...")

# 示例回调函数
def on_select_callback(school_id, school_name, school_code):
    print("\n=== 回调函数被调用 ===")
    print(f"ID: {school_id}")
    print(f"名称: {school_name}")
    print(f"代码: {school_code}")
    print("=====================")

if __name__ == "__main__":
    # 使用示例回调函数初始化选择器
    selector = SchoolSelector(on_select_callback=on_select_callback)
    selector.run()