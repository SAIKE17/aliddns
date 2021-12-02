import pickle


class Tools:

    def string_to_dict(self, cookie):
        """
        将cookie字符串转换为字典
        :param cookie: str
        :return: dict
        """

        item_dict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            item_dict[key] = value
        return item_dict

    def save_cookies(self, cookies, filename):
        """
        将cookie保存到pickle
        :param cookies:
        :param filename:
        :return:
        """
        with open(filename, 'wb+') as f:
            pickle.dump(cookies, f)

    def load_cookies(self, filename):
        """
        读取pickle的cookies
        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            return None
            raise
        else:
            pass
        finally:
            pass
