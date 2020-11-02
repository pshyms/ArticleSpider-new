
# 对于爬取到比较长的URL进行MD5编码，得到固定长度的URL长度
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()


# 直接执行时会调用下面语句，import调用时不会执行，主要用于代码测试
if __name__ == "__main__":
    print(get_md5("https://cnblogs.com"))
