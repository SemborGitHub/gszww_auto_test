import jieba


def lcut_for_search_fun(strs):
    # 搜索引擎模式分词
    result2 = jieba.lcut_for_search(strs)
    return result2


if __name__ == '__main__':
    result = lcut_for_search_fun('注册安全工程师注册管理')
    print(result)
