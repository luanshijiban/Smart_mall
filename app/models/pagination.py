class Pagination:
    """替代原 Record_Bean 的分页功能"""
    
    def __init__(self, items, page=1, per_page=10):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = len(items)
        
    @property
    def pages(self):
        """总页数"""
        if self.per_page == 0 or self.total == 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page
        
    @property
    def has_prev(self):
        """是否有上一页"""
        return self.page > 1

    @property
    def has_next(self):
        """是否有下一页"""
        return self.page < self.pages
        
    def get_page_items(self):
        """获取当前页的数据"""
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end] 