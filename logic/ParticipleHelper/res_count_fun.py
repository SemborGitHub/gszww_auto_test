import jieba


def lcut_for_search_fun(strs):
    # 搜索引擎模式分词
    result2 = jieba.lcut_for_search(strs)
    return result2


# 分词在html源码中的数量进行判断
def terms_count_in_html(html_text, terms_list):
    result_list = []
    for terms in terms_list:
        if terms in html_text:
            result_list.append(terms)
    percent = len(result_list)/len(terms_list)
    print(result_list)
    print(terms_list)
    return float(percent)


if __name__ == '__main__':
    result = lcut_for_search_fun('注册安全工程师注册管理')
    print(result)
