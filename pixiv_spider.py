import re
import urllib.request
import urllib.parse

rootURL = 'http://www.pixiv.net'
searchURL = 'http://www.pixiv.net/search.php?'
cookie = 'p_ab_id=2; login_ever=yes; _ga=GA1.2.1518701190.1446977842; a_type=0; hide_premium_promotion_modal2=1458463553; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; PHPSESSID=6695864_fabeb70e54ede0bbdc1ad6abfc3e1f73; __utmt=1; __utma=235335808.1518701190.1446977842.1458530497.1458537101.98; __utmb=235335808.6.10.1458537101; __utmc=235335808; __utmz=235335808.1446977842.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=6695864=1'


class Spider:
    searchURL = searchURL

    def __init__(self, keyword, threshold, from_page=1, page_count=10):
        self.keyword = urllib.parse.quote(keyword)
        self.threshold = threshold
        self.from_page = from_page
        self.page_count = page_count
        self.searchURL += (u'&word=' + self.keyword + u'&p=')

    def run(self):
        for i in range(self.from_page, self.from_page + self.page_count):
            url = self.searchURL + str(i)

            print("page : " + str(i))

            page = get_page(url)
            image_item_list = get_image_item_list(page)

            for image_item in image_item_list:
                book_mark_group = get_bookmark_count(image_item)
                if book_mark_group is not None:
                    book_mark_count = int(book_mark_group.groups()[0])
                    if book_mark_count >= self.threshold:
                        print(rootURL + get_illust(image_item).groups()[0])


def get_page(url):
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie)
    resp = urllib.request.urlopen(req)

    page = resp.read().decode('utf-8')

    return page


def get_image_item_list(page):
    pattern = r'<li class="image-item">.*?</li>'
    return re.findall(pattern, page)


def get_bookmark_count(image_item):
    pattern = r'<i class="_icon sprites-bookmark-badge"></i>(\d*)</a>'
    return re.search(pattern, image_item)


def get_illust(image_item):
    pattern = r'<a href="(/member_illust.php.*?)"'
    return re.search(pattern, image_item)
